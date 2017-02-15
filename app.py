import random
from werkzeug.exceptions import BadRequest

from flask import Flask, request
from flask_restful import Resource, Api
from mongoengine import connect, Document, StringField, BooleanField, NotUniqueError, DoesNotExist


connect('todoApp')

class Todo(Document):
    task = StringField(unique=True)
    completed = BooleanField(default=False)

    def to_json(self):
        return {'id': str(self.id),
                'task': self.task,
                'completed': self.completed}

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class TodoResource(Resource):
    # get todos
    def get(self):
        return {'todos': [todo.to_json() for todo in Todo.objects]}

    # Update a todo
    def put(self, todo_id):
        input_json = request.get_json()
        try:
            todo = Todo(id=todo_id).save()
        except DoesNotExist:
            raise BadRequest('Invalid Todo Id')
        todo.update(completed=input_json['completed'],
                    task=input_json['task'])
        return {'success': True}

    # create a todo
    def post(self):
        input_json = request.get_json()
        try:
            todo = Todo(task=input_json['task']).save()
        except NotUniqueError:
            raise BadRequest('Redundant Todo')
        return {'success': True}


api.add_resource(HelloWorld, '/')
api.add_resource(TodoResource, '/todos', '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
