from src.model import get_images, save_tags, get_short_videos, get_long_videos, get_longest_videos, test_connection
from src.model_batch import new_item, complete_batch
from src.mmdetection import Detection
import time, os
from src.VideoDetector import VideoDetector as VD
from src.utils import get_logger
from dotenv import dotenv_values

class Classifier:

    def __init__(self, batch_id) -> None:
        dotenv_path = '/app/.env'
        env = dotenv_values(dotenv_path)
        self.media_folder = env['MEDIA_FOLDER']
        self.batch_id = batch_id
        if batch_id > 0:
            self.logger = get_logger('batch_' + str(batch_id) + '.log')

    def is_media_folder_ok(self):
        return os.path.isdir(self.media_folder)
    
    def is_synology_db_connection_ok(self):
        try:
            res = test_connection()
            return True
        except Exception as e:
            return False
    
    def validate(self):
        if not self.is_media_folder_ok():
            return {
                'error': True,
                'error_code': 1,
                'error_msg': 'Media folder is not mounted'
            }
        if not self.is_synology_db_connection_ok():
            return {
                'error': True,
                'error_code': 2,
                'error_msg': 'Synology DB Connection could not be established'
            }
        return {
            'error': False
        }

    
    def prepare(self):
        self.detection = Detection()
        self.vd = VD(self.detection)
        return {
            'error': False
        }
    
    def classify_image(self, row):
        start = time.time()
        filename, file_extension = os.path.splitext(self.media_folder + row.full_path)
        # Classify simply as gif if the file is a gif. Can't load gifs or videos in this model
        if (file_extension == 'gif'):
            save_tags([{'class':'gif'}], row.unit_id)
            diff = time.time() - start
            new_item({
                'full_path': row.full_path, 
                'processing_time': diff, 
                'type': 'GIF', 
                'batch_id': self.batch_id
            })
            self.logger.info("GIF ID: {0} in {1} seconds".format(row.unit_id, diff))
        else:
            pred = self.detection.predict(self.media_folder + row.full_path, False)
            # False means the pic could not be loaded for any reason. The script will tag it as NOT CLASSIFIED and move on.
            if pred is False:
                save_tags([{'class':'none'}], row.unit_id)
                diff = time.time() - start
                new_item({
                    'full_path': row.full_path, 
                    'processing_time': diff, 
                    'type': 'ERROR_LOADING', 
                    'batch_id': self.batch_id
                })
                self.logger.error("PICTURE NOT LOADED ID: {0} in {1} seconds - {2}".format(row.unit_id, diff, self.media_folder + row.full_path))
            else:
                # Pic was classified and saved in the DB
                if len(pred['predictions_filtered']):
                    save_tags(pred['predictions_filtered'], row.unit_id)
                    diff = time.time() - start
                    new_item({
                        'full_path': row.full_path, 
                        'processing_time': diff, 
                        'type': 'PICTURE', 
                        'batch_id': self.batch_id
                    })
                    self.logger.info("PICTURE ID: {0} in {1} seconds".format(row.unit_id, diff))
                else:
                    # Nothing was detected in the picture. Probably something you don't want like a black picture. 
                    # The pic will be tagged for deletion. 
                    # You can search for delete using the SynoPhoto interface and do as you will.
                    save_tags([{'class':'delete'}], row.unit_id)
                    diff = time.time() - start
                    new_item({
                        'full_path': row.full_path, 
                        'processing_time': diff, 
                        'type': 'PICTURE_TO_DELETE', 
                        'batch_id': self.batch_id
                    })
                    self.logger.info("PICTURE ID: {0} in {1} seconds".format(row.unit_id, diff))
    
    def classify_images(self):
        list = get_images()

        # reiterate the list from DB until all pics are tagged
        while len(list) > 0:
            for row in list: 
                self.classify_image(row)
                        
            list = get_images()

    def classify_short_videos(self):
        # get the list of short videos (less than 60s) from the synofoto database. Loads by 300's
        list = get_short_videos()
        # reiterate the list from DB until all pics are tagged
        while len(list) > 0:
            for row in list: 
                start = time.time()
                frames = self.vd.extract_short_video_frames(self.media_folder + row.full_path)
                diff = time.time() - start
                self.logger.info("SHORT VIDEO ID: {0} in {1} seconds".format(row.unit_id, diff))
                tags = self.vd.process_frames(frames['list'], self.logger)
                if len(tags['list']) > 0:
                    save_tags(tags['list'], row.unit_id)
                    new_item({
                        'full_path': row.full_path, 
                        'processing_time': diff, 
                        'type': 'SHORT_VIDEO', 
                        'batch_id': self.batch_id
                    })
                else:
                    save_tags([{'class':'delete'}], row.unit_id)
                    new_item({
                        'full_path': row.full_path, 
                        'processing_time': diff, 
                        'type': 'SHORT_VIDEO_TO_DELETE', 
                        'batch_id': self.batch_id
                    })
            list = get_short_videos()

    def classify_videos(self):
        # get the list of long videos (more than 60s and less than 300s) from the synofoto database. Loads by 100's
        list = get_long_videos()
        # reiterate the list from DB until all pics are tagged
        while len(list) > 0:
            for row in list: 
                start = time.time()
                frames = self.vd.extract_long_video_frames(self.media_folder + row.full_path)
                diff = time.time() - start
                self.logger.info("VIDEO ID: {0} in {1} seconds".format(row.unit_id, diff))
                tags = self.vd.process_frames(frames['list'], self.logger)
                if len(tags['list']) > 0:
                    save_tags(tags['list'], row.unit_id)
                    new_item({
                        'full_path': row.full_path, 
                        'processing_time': diff, 
                        'type': 'VIDEO', 
                        'batch_id': self.batch_id
                    })
                else:
                    save_tags([{'class':'delete'}], row.unit_id)
                    new_item({
                        'full_path': row.full_path, 
                        'processing_time': diff,
                        'type': 'VIDEO_TO_DELETE', 
                        'batch_id': self.batch_id
                    })
            list = get_long_videos()

    def classify_long_videos(self):
        # get the list of longest videos (more than 300s) from the synofoto database. Loads by 10's
        list = get_longest_videos()
        # reiterate the list from DB until all pics are tagged
        while len(list) > 0:
            for row in list: 
                start = time.time()
                frames = self.vd.extract_longest_video_frames(self.media_folder + row.full_path)
                diff = time.time() - start
                self.logger.info("LONG VIDEO ID: {0} in {1} seconds".format(row.unit_id, diff))
                tags = self.vd.process_frames(frames['list'], self.logger)
                if len(tags['list']) > 0:
                    save_tags(tags['list'], row.unit_id)
                    new_item({
                        'full_path': row.full_path, 
                        'processing_time': diff, 
                        'type': 'LONG_VIDEO', 
                        'batch_id': self.batch_id
                    })
                else:
                    save_tags([{'class':'delete'}], row.unit_id)
                    new_item({
                        'full_path': row.full_path, 
                        'processing_time': diff, 
                        'type': 'LONG_VIDEO_TO_DELETE', 
                        'batch_id': self.batch_id
                    })
            
            list = get_longest_videos()

    def finish_classification(self):
        complete_batch()

    def classify(self):
        try:
            self.classify_images()
            self.classify_short_videos()
            self.classify_videos()
            self.classify_long_videos()
            self.finish_classification()
        except Exception as e:
            self.logger.error("An exception occurred: ", exc_info=True)