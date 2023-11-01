import os.path
from dotenv import dotenv_values
import subprocess

dotenv_path = '/app/.env'

env = dotenv_values(dotenv_path)

# Verify if the models are present
config_file = os.path.isfile('/app/ml_models/' + env['CONFIG_FILE'])
checkpoint = os.path.isfile('/app/ml_models/' + env['CHECKPOINT'])

def verify_ml_model ():
    if (not config_file or not checkpoint):
        command = ['sh', '/app/scripts/download_models.sh', env['CONFIG_FILE'][:-3]]
        process = subprocess.run(command, capture_output=True, text=True)
        return process.returncode
    else:
        return 0