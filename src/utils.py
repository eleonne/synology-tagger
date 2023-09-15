import datetime, logging, os, paramiko, re, time
from dotenv import dotenv_values
from src.scp import SCPClient

def format_seconds(seconds):
    tdelta = datetime.timedelta(seconds=seconds)
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    fmt = "{days} dias {hours}h {minutes}m {seconds}s"
    return fmt.format(**d)

LOG_DIR = 'log_dir'
LOG_FORMATTER = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

def get_logger(log_name, log_dir = LOG_DIR):
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    logger = logging.getLogger(log_name)
    if logger.hasHandlers(): 
        logger.handlers = []
    logging.basicConfig(level = logging.DEBUG)
    log_handler = logging.FileHandler(os.path.join(log_dir, log_name))
    log_handler.setFormatter(LOG_FORMATTER)
    log_handler.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

    return logger

def ssh_command(cmd, sudo=False):
    dotenv_path = '/app/.env'
    env = dotenv_values(dotenv_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(env['SYNOLOGY_HOST'], port=env['SSH_PORT'], username=env['SSH_USERNAME'], password=env['SSH_PASSWORD'])
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    if sudo is True:
        stdin.write(env['SSH_PASSWORD'] + '\r\n')
        stdin.flush()
    lines = []
    for line in stdout:
        line = (re.compile(r'\x1b[^m]*m')).sub('', line.strip())
        lines.append(line)
    ssh.close()
    return (re.compile(r'\x1b[^m]*m')).sub('', lines[-1].strip())

def ssh_multiple_commands(cmd_list):
    dotenv_path = '/app/.env'
    env = dotenv_values(dotenv_path)
    # # return ssh_config
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(env['SYNOLOGY_HOST'], port=env['SSH_PORT'], username=env['SSH_USERNAME'], password=env['SSH_PASSWORD'])
    channel = ssh.get_transport().open_session()
    channel.get_pty()
    channel.invoke_shell()
    break_cmd = False
    response = []
    while True:
        if break_cmd is True:
            break
        for cmd in cmd_list:
            channel.send(cmd + '\n')
            break_cmd = True if cmd == 'exit' else False
            while True:
                if channel.recv_ready():
                    output = (re.compile(r'\x1b[^m]*m')).sub('', channel.recv(1024).decode())
                    response.append(output)
                else:
                    time.sleep(0.5)
                    if not(channel.recv_ready()):
                        break
    return response

def upload_script(script):
    dotenv_path = '/app/.env'
    env = dotenv_values(dotenv_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(env['SYNOLOGY_HOST'], port=env['SSH_PORT'], username=env['SSH_USERNAME'], password=env['SSH_PASSWORD'])

    # Go!    
    scp = SCPClient(ssh.get_transport())

    filepath = "~/" + script
    localpath = "/app/scripts/" + script
    scp.put(localpath,filepath)