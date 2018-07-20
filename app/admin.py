from flask_admin.contrib.sqla import ModelView

from app import admin, db
from app.models import User

def init_admin(f_admin):
    f_admin.add_view(ModelView(User, db.session))
