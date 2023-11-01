from pprint import pprint
from mmdet.apis import init_detector, inference_detector
from PIL import Image
from pillow_heif import register_heif_opener
import time, os
import numpy as np
import torch
from dotenv import dotenv_values
from PIL import Image
from mmengine.visualization import Visualizer

register_heif_opener()
dotenv_path = '/app/.env'
env = dotenv_values(dotenv_path)

class Detection:

    _model = None
    _base_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
    _config_file = 'ml_models/' + env['CONFIG_FILE']
    _checkpoint_file = 'ml_models/' + env['CHECKPOINT']
    # _config_file = 'ml_models/rtmdet_l_8xb32-300e_coco.py'
    # _checkpoint_file = 'ml_models/rtmdet_l_8xb32-300e_coco_20220719_112030-5a0be7c4.pth'
    _all_classes = None
    _size = (1024, 1024)
    _filtered = None
    _time = None
    _threshold = float(env['THRESHOLD'])
    _device = env['DEVICE']

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
    def filter(self, classes, scores, bboxes):
        ctr_index = []
        def anon(x, i):
            ctr_index.append(self._all_classes[x]) 
            return {"class": self._all_classes[x], "prediction":scores[i], "bbox": bboxes[i]}
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
        if self._device == 'gpu':
            self._device = 'cuda:0'
        self._model = init_detector(self._base_dir + self._config_file, self._base_dir + self._checkpoint_file, device=self._device)  # or device='cpu'
        self._all_classes = self._model.dataset_meta['classes']

    def save_image(self, img, pred):
        visualizer = Visualizer(image=img)
        # single bbox formatted as [xyxy]
        for p in pred:
            visualizer.draw_bboxes(p['bbox'])
            visualizer.draw_texts(p['class'] + "("+ str(p['prediction']) +")", torch.tensor([p['bbox'][0:1], p['bbox'][1:2]]), colors='r')
        # draw multiple bboxes
        visualizer.get_image()
        im = Image.fromarray(visualizer.get_image())
        im.save("debug.jpeg")

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
            #f=open('./debug.txt', 'w+')
            #pprint(vars(id), stream=f)
            #f.close()
        except:
            return False
        end = time.time()
        self._time = (end-start) * 10**3

        # Clean the response
        pred = self.filter(id._pred_instances.labels, id._pred_instances.scores, id._pred_instances.bboxes)
        # Save the file with boxes on the detected objects. Defaults to False
        if (save):
            self.save_image(img, pred)
        return {'exec_time':self._time, 'predictions_filtered': pred}
