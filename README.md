# Synology Tagger

## Installation
1. Ubuntu essentials or Windows Visual Studio CE (NOT VS Code!)
sudo apt-get install build-essentials libssl-dev libffi-dev

2. Install python 3.9, pip3.9 and venv
sudo apt install python3.9 python3.9-dev 
sudo apt install python3.9-venv

3. Install git or add the git client to Windows PATH
sudo apt install git

3. Create and activate the virtual environment
python3.9 -m venv venv
(Linux)
source venv/bin/activate 
(Windows)
cd venv/Scripts
activate.bat

5. Install torch
https://pytorch.org/get-started/locally/

6. Install MMDetect dependencies
pip install -U openmim
mim install mmcv-full

7. Install everything else
pip install -r requirements.txt

8. Download or train a MMDetection model and put it under ml_models folder. I have used faster RCNN, but maybe you can find something that better suits your needs.
python3.9 -m mim download mmdet --config faster_rcnn_r50_caffe_fpn_mstrain_3x_coco --dest ml_models
More pre-trained models here: https://github.com/open-mmlab/mmdetection/tree/3.x/configs

## Configuration
Check app.config

## Use
python3.9 app.py