from src.model import get_images, save_tags, get_short_videos
from src.mmdetection import Detection
import src.config as config
import time
import os
from src.VideoDetector import VideoDetector as VD
from tqdm import tqdm

source_folder = config.get(section='GENERAL')['source_folder']

detection = Detection()
vd = VD(detection)

#Verify if the Synology NAS folder is mounted
#On Windows you just have to access the NAS once on explorer and enter you username and passwd. Eg: \\192.x.x.x
#On Linux you have to mount it somewhere
#You always have to specify the source folder config in the app.config file

if not os.path.isdir(source_folder): 
    print('*** Source Folder is not MOUNTED!!! ***')
    exit()

def process_image(row):
    start = time.time()
    filename, file_extension = os.path.splitext(source_folder + row.full_path)
    # Classify simply as gif if the file is a gif. Can't load gifs or videos in this model
    if (file_extension == 'gif'):
        save_tags([{'class':'gif'}], row.unit_id)
        end = time.time()
    else:
        pred = detection.predict(source_folder + row.full_path, False)
        # False means the pic could not be loaded for any reason. The script will tag it as NOT CLASSIFIED and move on.
        if pred is False:
            save_tags([{'class':'none'}], row.unit_id)
            end = time.time()
        else:
            # Pic was classified and saved in the DB
            if len(pred['predictions_filtered']):
                save_tags(pred['predictions_filtered'], row.unit_id)
                end = time.time()
            else:
                # Nothing was detected in the picture. Probably something you don't want like a black picture. 
                # The pic will be tagged for deletion. 
                # You can search for delete using the SynoPhoto interface and do as you will.
                save_tags([{'class':'delete'}], row.unit_id)
                end = time.time()

# get the list of pics from the synofoto database. Loads by the 1000's
list = get_images()

# reiterate the list from DB until all pics are tagged
while len(list) > 0:
    print('PROCESSING IMAGE BATCH WITH', len(list), 'ITEMS')
    for row in tqdm(list): 
        process_image(row)
                
    list = get_images()

# get the list of short videos (less than 60s) from the synofoto database. Loads by 300's
list = get_short_videos()
# reiterate the list from DB until all pics are tagged
while len(list) > 0:
    print('PROCESSING SHORT VIDEOS BATCH WITH', len(list), 'ITEMS')

    for row in tqdm(list): 
        start = time.time()
        frames = vd.extract_short_video_frames(source_folder + row.full_path)
        tags = vd.process_frames(frames['list'])
        if len(tags['list']) > 0:
            save_tags(tags['list'], row.unit_id)
        else:
            save_tags([{'class':'delete'}], row.unit_id)
        #print('Frames Extracted in:', frames['exec_time'], 'ms')
        #print('Frames Classified in:', tags['exec_time'], 'ms')
        #print('Total:', frames['exec_time'] + tags['exec_time'], 'ms')
    
    list = get_short_videos()