from src.database import query, execute

def test_connection(db='syno'):
    sql = """SELECT 1"""
    res = query(sql, None, db).one()
    return res

# Select the total of classified media
def get_total_classified():
    sql = """SELECT count(*) as total
             FROM public.unit u 
             LEFT JOIN (
                 SELECT mgt.id_unit
                 FROM public.many_unit_has_many_general_tag mgt
                 GROUP BY mgt.id_unit
             ) xmgt ON xmgt.id_unit = u.id
             WHERE u.is_major = true"""
    res = query(sql, None).one()
    return res

# Select total tagged pictures
def get_total_classified_images():
    sql = """SELECT count(*) as total
             FROM public.unit u
             LEFT JOIN (
                 SELECT mgt.id_unit
                 FROM public.many_unit_has_many_general_tag mgt
                 GROUP BY mgt.id_unit
             ) xmgt ON xmgt.id_unit = u.id
             WHERE u.type = 0 and u.is_major = true"""
    res = query(sql, None).one()
    return res

# Select total tagged short videos
def get_total_classified_short_videos():
    sql = """SELECT COALESCE(sum(duration) / 1000, 0) as total
             FROM public.unit u
             LEFT JOIN (
                 SELECT mgt.id_unit
                 FROM public.many_unit_has_many_general_tag mgt
                 GROUP BY mgt.id_unit
             ) xmgt ON xmgt.id_unit = u.id
             JOIN video_additional va on u.id = va.id_unit
             WHERE u.type = 1 AND u.is_major = true AND duration < 60000"""
    res = query(sql, None).one()
    return res

# Select total tagged long videos
def get_total_classified_long_videos():
    sql = """SELECT COALESCE(sum(duration) / 1000, 0) as total
             FROM public.unit u
             LEFT JOIN (
                 SELECT mgt.id_unit
                 FROM public.many_unit_has_many_general_tag mgt
                 GROUP BY mgt.id_unit
             ) xmgt ON xmgt.id_unit = u.id
             JOIN video_additional va on u.id = va.id_unit
             WHERE u.type = 1 
                   AND u.is_major = true 
                   AND duration BETWEEN 60000 AND 300000"""
    res = query(sql, None).one()
    return res

# Select total tagged longest videos
def get_total_classified_longest_videos():
    sql = """SELECT COALESCE(sum(duration) / 1000, 0) as total
             FROM public.unit u
             LEFT JOIN (
                 SELECT mgt.id_unit
                 FROM public.many_unit_has_many_general_tag mgt
                 GROUP BY mgt.id_unit
             ) xmgt ON xmgt.id_unit = u.id
             JOIN video_additional va on u.id = va.id_unit
             WHERE u.type = 1 
                   AND u.is_major = true 
                   AND duration > 300000"""
    res = query(sql, None).one()
    return res

# Select the total of unclassified media
def get_total_unclassified():
    sql = """SELECT count(*) as total
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             WHERE mgt.id_unit IS null AND u.is_major = true"""
    res = query(sql, None).one()
    return res

# Select the total of pics not tagged yet
def get_total_unclassified_images():
    sql = """SELECT count(*) as total
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN folder f ON f.id = u.id_folder
             WHERE mgt.id_unit IS null AND u.type = 0"""
    res = query(sql, None).first()
    return res

# Select the total of short videos (less than 60 secs) not tagged yet
def get_total_unclassified_short_videos():
    sql = """SELECT COALESCE(sum(duration) / 1000, 0) as total
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN video_additional va on u.id = va.id_unit
             WHERE mgt.id_unit IS null AND u.type = 1 AND u.is_major = true AND duration < 60000"""
    res = query(sql, None).one()
    return res

# Select the total of long videos (more than 60s and less than 300s) not tagged yet
def get_total_unclassified_long_videos():
    sql = """SELECT COALESCE(sum(duration) / 1000, 0) as total
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN video_additional va on u.id = va.id_unit
             JOIN folder f ON f.id = u.id_folder
             WHERE mgt.id_unit IS null 
                   AND u.type = 1 
                   AND u.is_major = true 
                   AND duration BETWEEN 60000 AND 300000"""
    res = query(sql, None).one()
    return res

# Select the total of longest videos (more than 300s) not tagged yet
def get_total_unclassified_longest_videos():
    sql = """SELECT COALESCE(sum(duration) / 1000, 0) as total
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN video_additional va on u.id = va.id_unit
             JOIN folder f ON f.id = u.id_folder
             WHERE mgt.id_unit IS null 
                   AND u.type = 1 
                   AND u.is_major = true 
                   AND duration > 300000"""
    res = query(sql, None).one()
    return res

# Select the 1st 1000 pics not tagged yet
def get_images():
    sql = """SELECT u.id as unit_id, CONCAT('/', ui.name, '/Photos', f.name, '/', u.filename) as full_path 
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN folder f ON f.id = u.id_folder
             JOIN user_info ui ON ui.id = f.id_user
             WHERE mgt.id_unit IS null AND u.type = 0
             LIMIT 1000"""
    res = query(sql, None).all()
    return res
    
# Select the 1st 300 short videos (less than 60 secs) not tagged yet
def get_short_videos():
    sql = """SELECT u.id as unit_id, CONCAT('/', ui.name, '/Photos', f.name, '/', u.filename) as full_path 
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN video_additional va on u.id = va.id_unit
             JOIN folder f ON f.id = u.id_folder
             JOIN user_info ui ON ui.id = f.id_user
             WHERE mgt.id_unit IS null AND u.type = 1 AND u.is_major = true AND duration < 60000
             LIMIT 300"""
    res = query(sql, None).all()
    return res

# Select the 1st 100 long videos (more than 60s and less than 300s) not tagged yet
def get_long_videos():
    sql = """SELECT u.id as unit_id, CONCAT('/', ui.name, '/Photos', f.name, '/', u.filename) as full_path 
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN video_additional va on u.id = va.id_unit
             JOIN folder f ON f.id = u.id_folder
             JOIN user_info ui ON ui.id = f.id_user
             WHERE mgt.id_unit IS null 
                   AND u.type = 1 
                   AND u.is_major = true 
                   AND duration BETWEEN 60000 AND 300000
             LIMIT 100"""
    res = query(sql, None).all()
    return res

# Select the 1st 100 longest videos (more than 300s) not tagged yet
def get_longest_videos():
    sql = """SELECT u.id as unit_id, CONCAT('/', ui.name, '/Photos', f.name, '/', u.filename) as full_path 
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN video_additional va on u.id = va.id_unit
             JOIN folder f ON f.id = u.id_folder
             JOIN user_info ui ON ui.id = f.id_user
             WHERE mgt.id_unit IS null 
                   AND u.type = 1 
                   AND u.is_major = true 
                   AND duration > 300000
             LIMIT 10"""
    res = query(sql, None).all()
    return res

def get_last_picture_taken():
    sql = """SELECT u.id as unit_id, CONCAT('/', ui.name, '/Photos', f.name, '/', u.filename) as full_path 
             FROM public.unit u
             JOIN folder f ON f.id = u.id_folder
             JOIN user_info ui ON ui.id = f.id_user
             WHERE u.type = 0 AND u.is_major = true
             ORDER BY u.createtime DESC
             LIMIT 1"""
    res = query(sql, None).one()
    return res

# Save the tags that were detected
'''
tags = [
    {"class": "xxx"},
    ...
]
'''
def save_tags(tags, unit_id):
    tags = [tag['class'] for tag in tags]
    tags = "|".join(tags)
    sql = """SELECT id, name, normalized_name
            FROM public.general_tag g
            WHERE g.normalized_name SIMILAR TO '("""+ tags +""")%'
        """
    #print(sql)
    res = query(sql, None)
    for row in res:
        sql = "INSERT INTO many_unit_has_many_general_tag(id_unit, id_general_tag) VALUES (:unit_id, :id)"
        execute(sql, {'unit_id': unit_id, 'id': row.id})

def get_photo_trend():
    sql = """SELECT TO_CHAR(TO_TIMESTAMP(mtime), 'YYYY') as label, count(*) as value
             FROM public.unit u
             WHERE u.type = 0 and u.is_major = true
             GROUP BY TO_CHAR(TO_TIMESTAMP(mtime), 'YYYY')
             ORDER BY TO_CHAR(TO_TIMESTAMP(mtime), 'YYYY') ASC"""
    res = query(sql, None).all()
    return res

def get_video_trend():
    sql = """SELECT TO_CHAR(TO_TIMESTAMP(takentime), 'YYYY') as label, SUM(duration / 1000) as value
             FROM public.unit u
             JOIN video_additional va on u.id = va.id_unit
             WHERE u.type = 1 and u.is_major = true
             GROUP BY TO_CHAR(TO_TIMESTAMP(takentime), 'YYYY')
             ORDER BY TO_CHAR(TO_TIMESTAMP(takentime), 'YYYY') ASC"""
    res = query(sql, None).all()
    return res

def get_video_trend_split():
    sql = """SELECT CASE WHEN duration / 1000 <= 30 THEN 'SHORT'
                         WHEN duration / 1000 > 30 AND duration / 1000 <= 60 THEN 'SMALL'
                         WHEN duration / 1000 > 60 AND duration / 1000 <= 300 THEN 'REGULAR'
                         WHEN duration / 1000 > 300 THEN 'LONG'
                    END AS label,
                    COUNT(*) as count, SUM(duration / 1000) as duration, SUM(filesize) as filesize
             FROM public.unit u
             JOIN video_additional va on u.id = va.id_unit
             WHERE u.type = 1 and u.is_major = true
             GROUP BY CASE WHEN duration / 1000 <= 30 THEN 'SHORT'
                           WHEN duration / 1000 > 30 AND duration / 1000 <= 60 THEN 'SMALL'
                           WHEN duration / 1000 > 60 AND duration / 1000 <= 300 THEN 'REGULAR'
                           WHEN duration / 1000 > 300 THEN 'LONG'
                      END"""
    res = query(sql, None).all()
    return res

def get_photo_by_country():
    sql = """SELECT DISTINCT COALESCE(gc.country, '-') AS label, COUNT(*) AS value
             FROM public.unit u
             LEFT JOIN geocoding_info gc ON gc.id_geocoding = u.id_geocoding AND lang = 0
             WHERE u.type = 0 AND u.is_major = true
             GROUP BY gc.country
             ORDER BY COUNT(*) DESC"""
    res = query(sql, None).all()
    return res

def get_bytes_by_folder(top_folder_id, is_video, is_major):
    is_video = 1 if is_video else 0
    is_major = 'true' if is_major else 'false'
    sql = """WITH RECURSIVE x AS (
                SELECT id, parent, name, id as top_parent_id
                FROM folder
                WHERE id IN (select id from folder where parent = :top_folder_id)
                UNION 
                SELECT p.id, p.parent, p.name, x1.top_parent_id
                FROM folder p
                INNER JOIN x x1 ON p.parent = x1.id 
            ) 

            SELECT x.top_parent_id as id, f.name as folder, sum(u.filesize) as filesize, count(*) as count
            FROM x
            JOIN public.unit u ON u.id_folder = x.id
            JOIN folder f ON f.id = x.top_parent_id
            WHERE u.type = :is_video and u.is_major = :is_major
            GROUP BY x.top_parent_id, f.name
            ORDER BY sum(u.filesize) DESC"""
    res = query(sql, {
        'top_folder_id': top_folder_id, 
        'is_video': is_video, 
        'is_major': is_major
    }).all()
    return res