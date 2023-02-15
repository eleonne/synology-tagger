# Synology Tagger

Simple tool to improove the Synology Photos search. The idea is to use Machine Learning to classify the pictures and save the classification as tags in the pictures. The Synology Photos already knows how to search for the tags, so if the ML model classifies a picture as `{dog, plant vase, orange}`, you should be able to search for these terms.<br/>
The list of tags are saved in the `general_tag` table and the N <--> N in `many_unit_has_many_general_tag`.<br/>

## Installation
1. Ubuntu essentials or Windows Visual Studio CE (NOT VS Code!)
```console
sudo apt-get install build-essentials libssl-dev libffi-dev
```

2. Install python 3.9, pip3.9 and venv
```console
sudo apt install python3.9 python3.9-dev 
sudo apt install python3.9-venv
```

3. Install git or add the git client to Windows PATH
```console
sudo apt install git
```

4. Create and activate the virtual environment
```console
python3.9 -m venv venv
```
Linux
```console
source venv/bin/activate 
```
Windows
```console Windows
cd venv/Scripts
activate.bat
```

5. Install torch
<p>https://pytorch.org/get-started/locally/</p>

6. Install MMDetect dependencies
```console
pip install -U openmim
mim install mmcv-full
```

7. Install everything else
```console
pip install -r requirements.txt
```

8. Download or train a MMDetection model and put it under ml_models folder. I used Faster RCNN. If you choose a different model, update `_config_file` and `_checkpoint_file` on [mmdetection.py](https://github.com/eleonne/synology-tagger/blob/main/src/mmdetection.py)
```console
python3.9 -m mim download mmdet --config faster_rcnn_r50_caffe_fpn_mstrain_3x_coco --dest ml_models
```
More pre-trained models here: https://github.com/open-mmlab/mmdetection/tree/3.x/configs

9. Create a Postgres user for yourself with access to select and insert in the database SynoFoto. Login with SSH and then:
```console
psql -d synofoto
```
```pgsql
CREATE ROLE username WITH LOGIN SUPERUSER PASSWORD 'password';
```

10. Create the tags in the database. <br/>
Execute [sql_insert_general_tags](https://github.com/eleonne/synology-tagger/blob/main/sql/sql_insert_general_tags) in the database. <br/>
The second and fouth columns have texts in Portuguese, so it would be a good idea to translate them to your language before running the inserts <br/>
Ex:<br/>
```pgsql
insert into general_tag (id_user, name, count, normalized_name) values (1,'Pessoa', 0, 'person pessoa');
```
English
```pgsql
insert into general_tag (id_user, name, count, normalized_name) values (1,'Person', 0, 'person');
```
Spanish
```pgsql
insert into general_tag (id_user, name, count, normalized_name) values (1,'Persona', 0, 'person persona');
```

## Configuration
Add your Postgres credentials and mounted folder path to [app.config](https://github.com/eleonne/synology-tagger/blob/main/app.config.default)

## RUN
Always activate the v-env before running

Linux
```console
source venv/bin/activate 
```
Windows
```console Windows
cd venv/Scripts
activate.bat
```
Finally
```console
python3.9 app.py
```
