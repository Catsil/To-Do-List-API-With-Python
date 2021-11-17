"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Task
from sqlalchemy import exc
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/task', methods=['GET'])
def get_task():
    tasks= Task.get_all()
    all_tasks=[task.to_dict() for task in tasks]
    return jsonify(all_tasks), 200

@app.route('/task/<int:id>', methods=['GET'])
def get_task_by_id(id):
    task= Task.get_by_id(id)

    if task:
        return jsonify(task.to_dict()), 200

        return jsonify({'error': 'task not found'}), 404

@app.route('/task', methods=['POST'])
def create_item():
    new_item=request.json.get('item',None)

    if not new_item:
        return jsonify({'error':'missing items'}), 400

    task= Task(item=new_item, done=False)
    try:
        task_created=task.create()
        return jsonify(task_created.to_dict()), 201
    except exc.IntegrityError:
        return jsonify({'error': 'fail in data'}), 400

@app.route('/task/<int:id>', methods=['PUT','PATCH'])
def update_task(id):
    new_item=request.json.get('item', None)

    if not new_item:
        return jsonify({'error': 'missing items'}), 400

    task= Task.get_by_id(id)
    if task:
        task=task.update(new_item)

    return jsonify({'error': 'task not found'}), 404

@app.route('/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task=Task.get_by_id(id)
    if task:
        task.delete()
        return jsonify(task.to_dict()), 200

    return jsonify({'error':'task not found'}), 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
