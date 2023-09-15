from src.database import query, execute
import os

def get_is_running():
    sql = """SELECT total_images, total_short_videos, total_videos, total_long_videos, status, id
             FROM batch
             WHERE status = 'RUNNING'"""
    #return sql
    res = query(sql, None, 'tagger').fetchone()
    return res

def get_percentage_processed():
    sql = """SELECT total_images, total_short_videos, total_videos, total_long_videos
             FROM batch
             WHERE status = 'RUNNING'"""
    res = query(sql, None, 'tagger').one()
    return res

def get_classification_data():
    sql = """SELECT DATE_FORMAT(start_date, '%Y-%m') as label,
                 SUM(TIMESTAMPDIFF(SECOND, start_date, end_date)) as value
             FROM batch
             WHERE status = 'COMPLETED'
             GROUP BY DATE_FORMAT(start_date, '%Y-%m')
             ORDER BY DATE_FORMAT(start_date, '%Y-%m') ASC"""
    res = query(sql, None, 'tagger').all()
    return res

def schedule_batch(sleep_time):
    sql = """INSERT INTO batch (created_at,start_date,status,total_images, total_short_videos, total_videos, total_long_videos) 
                        VALUES (CURRENT_TIMESTAMP, DATE_ADD(now(), INTERVAL :sleep_time second), 'SCHEDULED', 0, 0, 0, 0)"""
    execute(sql, {'sleep_time': sleep_time}, 'tagger')

def new_batch(totals):
    sql = """INSERT INTO batch (start_date, status, total_images, total_short_videos, total_videos, total_long_videos)
                        VALUES (CURRENT_TIMESTAMP, 'RUNNING', :total_images, :total_short_videos, :total_videos, :total_long_videos)"""
    execute(sql, {
        'total_images': totals['total_images'], 
        'total_short_videos': totals['total_short_videos'], 
        'total_videos': totals['total_videos'], 
        'total_long_videos': totals['total_long_videos']
    }, 'tagger')

def complete_batch():
    sql = """UPDATE batch SET end_date=CURRENT_TIMESTAMP, status='COMPLETED'
             WHERE status='RUNNING'"""
    execute(sql, None, 'tagger')

def new_item(item):
    sql = """INSERT INTO items (full_path,processing_time,type,batch_id) 
                        VALUES (:full_path,:processing_time,:type,:batch_id)"""
    execute(sql, {
        'full_path': item['full_path'], 
        'processing_time': item['processing_time'], 
        'type': item['type'], 
        'batch_id': item['batch_id']
    }, 'tagger')