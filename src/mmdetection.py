from mmdet.apis import init_detector, inference_detector
from PIL import Image
from pillow_heif import register_heif_opener
import time, os
import numpy as np
import src.config as config

register_heif_opener()
db_config = config.get(section='GENERAL')

class Detection:

    _model = None
    _config_file = 'ml_models/faster_rcnn_r50_caffe_fpn_mstrain_3x_coco.py'
    _checkpoint_file = 'ml_models/faster_rcnn_r50_caffe_fpn_mstrain_3x_coco_20210526_095054-1f77628b.pth'
    _all_classes = None
    _size = (1024, 1024)
    _filtered = None
    _time = None
    _threshold = float(db_config['threshold'])

    def load_image(self, img):
        try:
            pil_image = Image.open(img)
            pil_image = pil_image.resize(self._size, Image.ANTIALIAS)   

            open_cv_image = np.array(pil_image) 
            # Convert RGB to BGR 
            im = open_cv_image[:, :, ::-1].copy() 
            return im
        except:
            return False

    # Remove duplicates and predictions less than 55% of certainty
    def filter(self, classes, scores):
        ctr_index = []
        def anon(x, i):
            ctr_index.append(self._all_classes[x]) 
            return {"class": self._all_classes[x], "prediction":scores[i]}
        self._filtered = [anon(x, i)
                        for i,x in enumerate(classes) 
                        if scores[i] > self._threshold and self._all_classes[x] not in ctr_index]

        return self._filtered

    def __str__(self):
        return f"""
        **************
            Execution time: {self._time} ms
            {self._filtered}
        **************
        """

    def __init__(self):
        # Use cuda:0 if you have an NVIDIA and CUDA Toolkit installed. Otherwise, cpu
        self._model = init_detector(self._config_file, self._checkpoint_file, device='cuda:0')  # or device='cpu'
        self._all_classes = self._model.CLASSES

    def predict(self, img_path = None, save=False, image = None):
        if image is not None:
            img = image
        else:
            img = self.load_image(img_path)
        # Verifies if the image failed to load for any reason
        if img is False:
            return False
        start = time.time()
        # Returns false if the prediction fails
        try:
            id = inference_detector(self._model, img)
        except:
            return False
        end = time.time()
        arr = np.vstack(id)
        self._time = (end-start) * 10**3

        #Extract the list of possible labels from the inference detector
        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32)
            for i, bbox in enumerate(id)
        ]
        labels = np.concatenate(labels)
        # Clean the response
        pred = self.filter(labels, arr[:, 4])
        # Save the file in the output folder with boxes on the detected objects. Defaults to False
        if (save):
            self._model.show_result(img, id, out_file='output/' + os.path.basename(img_path))
        return {'exec_time':self._time, 'predictions_filtered': pred}
