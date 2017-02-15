from mongoengine import Document, ReferenceField, \
                        StringField, BooleanField, NotUniqueError


class Todo(Document):
    task = StringField(unique=True)
    completed = BooleanField(default=False)
    owner = ReferenceField('User')

    def to_json(self):
        return {'id': str(self.id),
                'task': self.task,
                'completed': self.completed}
