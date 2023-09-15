from flask import Flask, render_template, jsonify, request
from flask_cors import cross_origin
from flask_sock import Sock
from src.classifier import Classifier
from src.model import get_total_classified, get_total_classified_images, get_total_classified_short_videos, test_connection
from src.model import get_total_classified_long_videos, get_total_classified_longest_videos
from src.model import get_total_unclassified, get_total_unclassified_images, get_total_unclassified_short_videos
from src.model import get_total_unclassified_long_videos, get_total_unclassified_longest_videos, get_last_picture_taken
from src.model_batch import get_is_running, get_classification_data
import time, os
from src.tasks import classify_task
from cron_descriptor import get_description
from src.utils import ssh_command, upload_script
from dotenv import dotenv_values, set_key
from pathlib import Path
from smb.SMBConnection import SMBConnection

app = Flask(__name__, static_folder='../static', template_folder="../static")

sock = Sock(app)

def get_not_processed():
   is_running_batch = get_is_running()
   if (is_running_batch is None):
      return {
         'is_running': "false",
         'pending_classification': 0
      }
   sum_of_totals = is_running_batch.total_images + is_running_batch.total_short_videos + is_running_batch.total_videos + is_running_batch.total_long_videos
   v2 = get_total_unclassified_short_videos().total
   v2 = v2 if v2 > 0 else 0
   v3 = get_total_unclassified_long_videos().total
   v3 = v3 / 2 if v3 > 0 else 0
   v4 = get_total_unclassified_longest_videos().total
   v4 = v4 / 5 if v4 > 0 else 0
   res = get_total_unclassified_images().total + v2 + v3 + v4
   res = res * 100 / sum_of_totals
   return {
      'is_running': "true" if is_running_batch else "false",
      'pending_classification': int(res)
   }

@app.route('/')
def index():
   return render_template('index.html')

@sock.route('/ws/get-totals')
def getTotals(ws):
   last_msg = None
   while True:
      data = ws.receive(timeout=0)
      msg = {
         "success": "true",
         "data": {
            "classified_total": get_total_classified().total,
            "classified_images": get_total_classified_images().total,
            "classified_short_videos": int(get_total_classified_short_videos().total),
            "classified_videos": int(get_total_classified_long_videos().total),
            "classified_long_videos": int(get_total_classified_longest_videos().total),
            "unclassified_total": get_total_unclassified().total,
            "unclassified_images": get_total_unclassified_images().total,
            "unclassified_short_videos": int(get_total_unclassified_short_videos().total),
            "unclassified_videos": int(get_total_unclassified_long_videos().total),
            "unclassified_long_videos": int(get_total_unclassified_longest_videos().total),
         }
      }
      if (msg != last_msg or data is not None):
         ws.send(msg)
         last_msg = msg
      time.sleep(1)

@sock.route('/ws/update-running-batch')
def update_running_batch(ws):
   dotenv_path = '/app/.env'
   env = dotenv_values(dotenv_path)
   schedule = get_description(env['CRONTAB'])
   last_msg = None
   while True:
      data = ws.receive(timeout=0)
      msg = get_not_processed()
      if (msg != last_msg or data is not None):
         last_msg = msg
         ws.send({
            "success": "true",
            "data": {
               "start_date": schedule,
               "is_running": msg['is_running'],
               "pending_classification": 100 - msg['pending_classification']
            }
         })
      time.sleep(1)

@app.route('/api/get-next-run')
def getNextRun():
   dotenv_path = '/app/.env'
   env = dotenv_values(dotenv_path)
   schedule = get_description(env['CRONTAB'])
   not_processed = get_not_processed()
   res = {
      "success": "true",
      "data": {
         "start_date": schedule,
         "is_running": not_processed['is_running'],
         "pending_classification": not_processed['pending_classification']
      }
   }
   return jsonify(res)

@app.route('/api/get-classification-data')
@cross_origin()
def getClassificationData():
   rows = get_classification_data()
   res = {
      'success': 'true',
      'data': {
         'labels': [],
         'values': [],
         'total': 0
      }
   }
   for r in rows:
      res['data']['labels'].append(r.label)
      res['data']['values'].append(r.value)
      res['data']['total'] = res['data']['total'] + r.value
   return jsonify(res)

@app.route('/api/run-now')
@cross_origin()
def runNow():
   is_running = get_is_running()
   
   if is_running:
      return {
         'success': 'true',
         'error': 'true',
         'error_msg': 'Already Running bruh!'
      }
   total = get_total_unclassified()
   if total.total == 0:
      return {
         'success': 'true',
         'error': 'true',
         'error_msg': 'There is nothing to classify! My work here is done (flies in training images)'
      }
   classifier = Classifier(0)
   validate = classifier.validate()
   if (validate['error'] is True):
      return jsonify(validate)
   else:
      classify_task.delay()
   
   return jsonify({
      'success': 'true',
      'classifying': 'true'
   })

@app.route('/api/get-config')
@cross_origin()
def get_config():
   dotenv_path = '/app/.env'
   env_vars = dotenv_values(dotenv_path)

   res = []
   for key, value in env_vars.items():
      res.append([key, value])

   return jsonify(dict(res))

@app.route('/api/save-config', methods=['POST'])
@cross_origin()
def save_config():
   dotenv_path = '/app/.env'
   for key, value in request.json.items():
      set_key(dotenv_path, key, value)
   # Restart celery so the schedule change works
   os.system("ps auxww | grep celery | grep -v \"grep\" | awk '{print $2}' | xargs kill -9")
   os.system("celery -A src.tasks worker -B -P solo -l info &")   
   return jsonify({
      'success': 'true',
      'saved': 'true'
   })

@app.route('/api/test-ssh', methods=['GET'])
@cross_origin()
def test_ssh():
   try:
      ssh_command("""
         ls
         exit
      """)
   except Exception as e:
      return jsonify({
         'error': 'true',
         'error_message': str(e),
         'is_connected': 'false'
      })

   return jsonify({
      'success': 'true',
      'error_message': '',
      'is_connected': 'true'
   })

@app.route('/api/test-postgres', methods=['GET'])
@cross_origin()
def test_postgres():
   try:
      test_connection()
   except Exception as e:
      return jsonify({
         'error': 'true',
         'error_message': str(e),
         'is_connected': 'false'
      })

   return jsonify({
      'success': 'true',
      'error_message': '',
      'is_connected': 'true'
   })

@app.route('/api/create-postgres-connection', methods=['GET'])
@cross_origin()
def create_postgres_connection():
   dotenv_path = '/app/.env'
   env = dotenv_values(dotenv_path)
   script = 'enable_postgres_connection.sh'
   upload_script(script)
   out = ssh_command("sudo sh {0} {1} '{2}'".format(script, env['PG_USERNAME'], env['PG_PASSWORD']), True)

   return jsonify({
      'stdout': out,
      # 'stderr': res['stderr']
   })

@app.route('/api/test-media-folder', methods=['GET'])
@cross_origin()
def test_media_folder():
   dotenv_path = '/app/.env'
   env = dotenv_values(dotenv_path)
   last_picture = get_last_picture_taken()
   full_path = env['MEDIA_FOLDER'] + last_picture.full_path
   file_exists = Path(full_path).exists()
   if file_exists:
      return jsonify({
         'success': 'true',
         'error_message': '',
         'is_connected': 'true'
      })
   else:
      return jsonify({
         'success': 'true',
         'error_message': "Can't find the last picture taken. Try mounting the folder. Notice you will need SSH+Postgres Connection",
         'is_connected': 'false'
      })

if __name__ == "__main__":
   sock.run(debug=True)