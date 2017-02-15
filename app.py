import random
from werkzeug.exceptions import BadRequest

from flask import Flask, request, g
from flask_restful import Resource, Api
from mongoengine import connect, NotUniqueError, DoesNotExist

from auth import auth
from models.user import User
from models.todo import Todo


connect('todoApp')


app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class UserResource(Resource):
    def post(self):
        pass


class TodoResource(Resource):
    # get todos
    @auth.login_required
    def get(self):
        return {'todos': [todo.to_json() for todo in Todo.objects(owner=g.user)]}

    # Update a todo
    @auth.login_required
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
    @auth.login_required
    def post(self):
        input_json = request.get_json()
        try:
            todo = Todo(task=input_json['task']).save()
        except NotUniqueError:
            raise BadRequest('Redundant Todo')
        return {'success': True}

    @auth.login_required
    def delete(self, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id).delete()
        except DoesNotExist:
            return {'success': True}
        return {'success': True}


api.add_resource(HelloWorld, '/')
api.add_resource(TodoResource, '/todos', '/todos/<todo_id>')
api.add_resource(UserResource, '/user')


if __name__ == '__main__':
    app.run(debug=True)
