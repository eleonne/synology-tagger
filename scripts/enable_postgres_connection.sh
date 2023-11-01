#! /bin/bash

if [ -e /etc/postgresql/pg_hba.conf.original ]
then
    cp /etc/postgresql/pg_hba.conf.bkp /etc/postgresql/pg_hba.conf
    sudo echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/pg_hba.conf
    echo "pg_hba.conf have been changed"
else
    cp /etc/postgresql/pg_hba.conf /etc/postgresql/pg_hba.conf.original
    cp /etc/postgresql/pg_hba.conf /etc/postgresql/pg_hba.conf.bkp
    echo "Backup of pg_hba.conf created"
fi

if [ -e /etc/postgresql/postgresql.conf.original ]
then
    cp /etc/postgresql/postgresql.conf.bkp /etc/postgresql/postgresql.conf
    sudo echo "listen_addresses = '*'" >> /etc/postgresql/postgresql.conf
    echo "postgresql.conf have been changed"
else
    cp /etc/postgresql/postgresql.conf /etc/postgresql/postgresql.conf.original
    cp /etc/postgresql/postgresql.conf /etc/postgresql/postgresql.conf.bkp
    echo "Backup of postgresql.conf created"
fi

sudo systemctl restart pgsql

sudo -u postgres psql -d synofoto -c "CREATE ROLE $1 WITH LOGIN SUPERUSER PASSWORD '$2';"

sudo -u postgres psql -d synofoto -c "ALTER USER $1 WITH PASSWORD '$2';"