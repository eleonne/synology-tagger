import os

print('**** START MYSQL ****')
os.system("service mysql start")

print('**** START RABBITMQ ****')
os.system("rabbitmq-server &")

print('**** START CELERY ****')
os.system("celery -A src.tasks worker -B -P solo -l info &")

print('**** START FLASK ****')
os.system("flask run -h 0.0.0.0 &")

print('**** SLEEPING FOREVER ****')
os.system("sleep infinity")
exit()