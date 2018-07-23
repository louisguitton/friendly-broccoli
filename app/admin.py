from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user


class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated
        # return current_user.is_active and current_user.is_authenticated and current_user.has_role('ROLE_ADMIN')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated


def init_admin(f_admin):
    from app import db
    from app.models import User, Question

    f_admin.add_view(MyModelView(User, db.session))
    f_admin.add_view(MyModelView(Question, db.session))
