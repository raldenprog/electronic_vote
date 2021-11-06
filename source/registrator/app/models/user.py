from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id_user = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    user_name = db.Column(db.String(64), index=True, unique=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id_user


@login.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))
