from bson import ObjectId

from db.main import mongo_db


def mark_task_done(task_id: str):
    mongo_db()['task'].update_one({'_id': ObjectId(task_id)}, {'$set': {'spider_done': True}})
