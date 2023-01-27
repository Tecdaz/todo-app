import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()


def user_reference(user):
    return db.collection('users').document(user)


def todo_reference(user_id, todo_id):
    return user_reference(user_id).collection('todos').document(todo_id)


def get_users():
    return db.collection('users').get()


def get_user(user_id):
    return user_reference(user_id).get()


def get_todos(user_id):
    return user_reference(user_id).collection('todos').get()


def user_put(user_data):
    user_ref = user_reference(user_data.userid)
    user_ref.set({'password': user_data.password,
                  'username': user_data.username})


def put_todo(user_id, description):
    todos_collection_reference = user_reference(user_id).collection('todos')
    todos_collection_reference.add({'description': description,
                                    'done': False})


def delete_todo(user_id, todo_id):
    todo_ref = todo_reference(user_id, todo_id)
    todo_ref.delete()


def update_todo(user_id, todo_id):
    todo_ref = todo_reference(user_id, todo_id)
    actual_status = todo_ref.get().to_dict()['done']
    todo_ref.update({'done': not actual_status})


