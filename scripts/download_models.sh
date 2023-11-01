#!/bin/sh

defaultParam="faster-rcnn_r50-caffe_fpn_ms-3x_coco"
MODEL=$1
FILTERED="${MODEL:-$defaultParam}" # return default value if from2nd is empty
mim download mmdet --config $FILTERED --dest ml_models/