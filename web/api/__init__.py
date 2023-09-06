from flask import Flask, render_template, jsonify
from flask_cors import CORS
from logging.handlers import RotatingFileHandler
import logging
from src.database import query
from src.model import get_total_classified, get_total_classified_images, get_total_classified_short_videos, get_total_classified_long_videos, get_total_classified_longest_videos
from src.model import get_total_unclassified, get_total_unclassified_images, get_total_unclassified_short_videos, get_total_unclassified_long_videos, get_total_unclassified_longest_videos
from src.model_batch import get_next_run, get_is_running, get_classification_data
from datetime import datetime
from decimal import Decimal

app = Flask(__name__, static_folder='../static', template_folder="../static")

cors = CORS(app)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/api/get-totals')
def getTotals():
   res = {
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
   return jsonify(res)
   
@app.route('/api/get-next-run')
def getNextRun():
   is_running_batch = get_is_running()
   v = get_total_unclassified_images().total
   unc_images = Decimal(v * 100 / is_running_batch.total_images) if v > 0.0 and is_running_batch.total_images > 0 else 0
   v = get_total_unclassified_short_videos().total
   unc_short = Decimal(v * 100 / is_running_batch.total_short_videos) if v > 0.0 and is_running_batch.total_short_videos > 0 else 0
   v = get_total_unclassified_long_videos().total
   unc_video = Decimal(v * 100 / is_running_batch.total_videos) if v > 0.0 and is_running_batch.total_videos > 0 else 0
   v = get_total_unclassified_longest_videos().total
   unc_long = Decimal(v * 100 / is_running_batch.total_long_videos) if v > 0.0 and is_running_batch.total_long_videos > 0 else 0

   median = 0
   median = median + 1 if unc_images > 0 else median
   median = median + 1 if unc_short > 0 else median
   median = median + 1 if unc_video > 0 else median
   median = median + 1 if unc_long > 0 else median
   a = unc_images + unc_short + unc_video
   not_processed = (unc_images + unc_short + unc_video + unc_long) / median if median > 0 else 0
   res = {
      "success": "true",
      "data": {
         "start_date": datetime.strptime(get_next_run().start_date, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y às %H:%M:%S'),
         "is_running": "true" if is_running_batch else "false",
         "pending_classification": int(not_processed)
      }
   }
   return jsonify(res)

@app.route('/api/get-classification-data')
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
def runNow():
   res = {}
   return jsonify(res)
if __name__ == "__main__":
   cors.run(debug=True)