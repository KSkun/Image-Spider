import json

from bson import ObjectId
from typing import Dict

from config import C
from db.main import mongo_db, redis_client

_classifier_stream_name: str = 'classify_cmd'
_classifier_group_name: str = 'classifier'


def create_image(task_id: str, filename: str) -> ObjectId:
    image_obj = {
        'task_id': ObjectId(task_id),
        'url': C.image_url + '/' + C.image_tmp_dir + '/' + task_id + '/' + filename,
        'class': 'pending'
    }
    return mongo_db()['image'].insert_one(image_obj).inserted_id


def push_classifier_cmd(task_id: str, image: Dict[str, str]):
    redis_client().xadd(_classifier_stream_name, {
        'op': 'one',
        'task_id': task_id,
        'image': json.dumps(image)
    })
