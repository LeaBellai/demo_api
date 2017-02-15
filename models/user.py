from mongoengine import Document, StringField
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(Document):
    name = StringField()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer('SECRETKEY!!!!', 'SECRET_KEY')
        try:
            data = s.loads(token)
            user = User.objects.get(id=data['id'])
        except:
            return None
        return user

    def generate_auth_token(self, expiration=60*60*24*365):
        s = Serializer('SECRETKEY!!!!', expires_in=expiration)
        return s.dumps({'id': str(self.id)})
