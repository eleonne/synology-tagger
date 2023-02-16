
import cv2
import time, os
from pathlib import Path
from src.mmdetection import Detection
from src.model import save_tags
import src.config as config

db_config = config.get(section='GENERAL')

class VideoDetector:

    def __init__(self, detection) -> None:
        self._all_classes = detection._all_classes
        self._threshold = float(db_config['threshold'])
        self.detection = detection

    # Remove duplicates and predictions less than 55% of certainty
    def filter(self, img_tags):
        ctr_index = []
        res = []
        for tags in img_tags:
            for tag in tags:
                if tag['prediction'] > self._threshold and tag['class'] not in ctr_index:
                    ctr_index.append(tag['class']) 
                    res.append(tag)

        return res

    def extract_short_video_frames(self, video):

        cap = cv2.VideoCapture(video)
        fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        every_x_seconds = 1
        duration = int(round((frame_count / fps) % 60))

        if (duration > 120):
            return []

        res = []

        start = time.time()
        for i in range(1, duration, every_x_seconds):
            cap.set(cv2.CAP_PROP_POS_MSEC, i * 1000)
            success, image = cap.read()
            if image is not None:
                res.append(image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        end = time.time()
        _time = (end-start) * 10**3

        return {"exec_time": _time, "list":res}
    
    def process_frames(self, list):
        tags = []
        start = time.time()
        count = 0
        for img in list:
            count += 1
            pred = self.detection.predict(image = img)
            # False means the pic could not be loaded for any reason. The script will tag it as NOT CLASSIFIED and move on.
            if pred is False:
                print('Vish!')
            else:
                # Pic was classified and saved in the DB
                if len(pred['predictions_filtered']):
                    tags.append(pred['predictions_filtered'])
                    
        end = time.time()
        filtered_tags = self.filter(tags)
        
        return {"exec_time": (end-start) * 10**3, "list": filtered_tags}
