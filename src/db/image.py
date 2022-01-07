from bson import ObjectId

from config import C
from db.main import mongo_db


def create_image(task_id: str, filename: str):
    image_obj = {
        'task_id': ObjectId(task_id),
        'url': C.image_url + '/' + C.image_tmp_dir + '/' + task_id + '/' + filename,
        'class': 'pending'
    }
    mongo_db()['image'].insert_one(image_obj)
