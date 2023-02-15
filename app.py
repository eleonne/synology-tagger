from src.model import get_list, save_tags
from src.mmdetection import Detection
import src.config as config
import time
import os

source_folder = config.get(section='GENERAL')['source_folder']
detection = Detection()

#Verify if the Synology NAS folder is mounted
#On Windows you just have to access the NAS once on explorer and enter you username and passwd. Eg: \\192.x.x.x
#On Linux you have to mount it somewhere
#You always have to specify the source folder config in the app.config file

if not os.path.isdir(source_folder): 
    print('*** Source Folder is not MOUNTED!!! ***')
    exit()

# get the list from the synofoto database. Loads by the 1000's
list = get_list()
# reiterate the list from DB until all pics are tagged
while len(list) > 0:
    print('****** STARTING BATCH *******')
    for row in list: 
        start = time.time()
        filename, file_extension = os.path.splitext(source_folder + row.full_path)
        # Classify simply as gif if the file is a gif. Can't load gifs or videos in this model
        if (file_extension == 'gif'):
            save_tags([{'class':'gif'}], row.unit_id)
            end = time.time()
            print('GIF DETECTED: ', row.full_path)
        else:
            pred = detection.predict(source_folder + row.full_path, False)
            # False means the pic could not be loaded for any reason. The script will tag it as NOT CLASSIFIED and move on.
            if pred is False:
                save_tags([{'class':'none'}], row.unit_id)
                end = time.time()
                print('FAIL TO LOAD PICTURE: ', row.full_path, 'CAN\'T BE CLASSIFIED')
            else:
                # Pic was classified and saved in the DB
                if len(pred['predictions_filtered']):
                    save_tags(pred['predictions_filtered'], row.unit_id)
                    end = time.time()
                    print('PICTURE ', row.full_path, ' PROCESSED IN ', (end-start) * 10**3, ' ms')
                else:
                    # Nothing was detected in the picture. Probably something you don't want like a black picture. 
                    # The pic will be tagged for deletion. 
                    # You can search for delete using the SynoPhoto interface and do as you will.
                    save_tags([{'class':'delete'}], row.unit_id)
                    end = time.time()
                    print('NOTHING DETECTED IN PICTURE ', row.full_path, ' PROCESSED IN ', (end-start) * 10**3, ' ms')
                
    print('***** BATCH FINISHED *****')
    list = get_list()