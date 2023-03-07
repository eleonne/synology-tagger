from src.database import query, execute

# Select the 1st 1000 pics not tagged yet
def get_images():
    sql = """SELECT u.id as unit_id, CONCAT(f.name, '/', u.filename) as full_path 
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN folder f ON f.id = u.id_folder
             WHERE mgt.id_unit IS null AND u.type = 0
             LIMIT 1000"""
    res = query(sql, None).all()
    return res
    
# Select the 1st 300 short videos (less than 60 secs) not tagged yet
def get_short_videos():
    sql = """SELECT u.id as unit_id, CONCAT(f.name, '/', u.filename) as full_path 
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN video_additional va on u.id = va.id_unit
             JOIN folder f ON f.id = u.id_folder
             WHERE mgt.id_unit IS null AND u.type = 1 AND u.is_major = true AND duration < 60000
             LIMIT 300"""
    res = query(sql, None).all()
    return res

# Select the 1st 100 long videos (more than 60s and less than 300s) not tagged yet
def get_long_videos():
    sql = """SELECT u.id as unit_id, CONCAT(f.name, '/', u.filename) as full_path 
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN video_additional va on u.id = va.id_unit
             JOIN folder f ON f.id = u.id_folder
             WHERE mgt.id_unit IS null 
                   AND u.type = 1 
                   AND u.is_major = true 
                   AND duration BETWEEN 60000 AND 300000
             LIMIT 100"""
    res = query(sql, None).all()
    return res

# Select the 1st 100 longest videos (more than 300s) not tagged yet
def get_longest_videos():
    sql = """SELECT u.id as unit_id, CONCAT(f.name, '/', u.filename) as full_path 
             FROM public.unit u
             LEFT JOIN public.many_unit_has_many_general_tag mgt ON u.id = mgt.id_unit
             JOIN video_additional va on u.id = va.id_unit
             JOIN folder f ON f.id = u.id_folder
             WHERE mgt.id_unit IS null 
                   AND u.type = 1 
                   AND u.is_major = true 
                   AND duration > 300000
             LIMIT 10"""
    res = query(sql, None).all()
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
    res = query(sql, None)
    for row in res:
        sql = "INSERT INTO many_unit_has_many_general_tag(id_unit, id_general_tag) VALUES (:unit_id, :id)"
        execute(sql, {'unit_id': unit_id, 'id': row.id})
