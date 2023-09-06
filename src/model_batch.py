from src.database import query, execute
import os

def get_next_run():
    sql = """SELECT *
             FROM batch
             WHERE status = 'SCHEDULED'"""
    res = query(sql, None, 'tagger').one()
    return res

def get_is_running():
    sql = """SELECT total_images, total_short_videos, total_videos, total_long_videos
             FROM batch
             WHERE status = 'RUNNING'"""
    res = query(sql, None, 'tagger').first()
    return res

def get_percentage_processed():
    sql = """SELECT total_images, total_short_videos, total_videos, total_long_videos
             FROM batch
             WHERE status = 'RUNNING'"""
    res = query(sql, None, 'tagger').one()
    return res

def get_classification_data():
    sql = """SELECT strftime('%m-%Y', start_date) AS label,
                    CAST(SUM((julianday(end_date) - julianday(start_date)) * 86400) AS INTEGER) AS value
             FROM "batch"
             WHERE status = 'COMPLETED'
             GROUP BY strftime('%m%Y', start_date)
             ORDER BY strftime('%Y%m', start_date) ASC"""
    res = query(sql, None, 'tagger').all()
    return res

def schedule_batch(start_date):
    sql = """INSERT INTO batch (created_at,start_date,status,total_images, total_short_videos, total_videos, total_long_videos) 
                        VALUES (CURRENT_TIMESTAMP, :start_date, 'SCHEDULED', 0, 0, 0, 0)"""
    execute(sql, {'start_date': start_date})

def run_batch(totals, id):
    sql = """UPDATE batch SET start_date=CURRENT_TIMESTAMP, status='RUNNING', total_images=:total_images, 
                              total_short_videos=:total_short_videos, total_videos=:total_videos, total_long_videos=:total_long_videos
             WHERE ROWID=:id"""
    execute(sql, {
        'total_images': totals.total_images, 
        'total_short_videos': totals.total_short_videos, 
        'total_videos': totals.total_videos, 
        'total_long_videos': totals.total_long_videos, 
        'id': id
    })

def complete_batch(id):
    sql = """UPDATE batch SET end_date=CURRENT_TIMESTAMP, status='COMPLETE'
             WHERE ROWID=:id"""
    execute(sql, {
        'id': id
    })

def new_item(item):
    sql = """INSERT INTO items (full_path,processing_time,type,batch_id) 
                        VALUES (:full_path,:processing_time,:type,:batch_id)"""
    execute(sql, {
        'full_path': item.full_path, 
        'processing_time': item.processing_time, 
        'type': item.type, 
        'batch_id': item.batch_id
    })