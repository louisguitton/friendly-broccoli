from flask import redirect, url_for, request, current_app
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user
from flask_principal import Permission, RoleNeed, identity_loaded, UserNeed


admin_role = RoleNeed('admin')
admin_permission = Permission(admin_role)


class MyModelView(ModelView):

    @admin_permission.require()
    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))


class MyAdminIndexView(AdminIndexView):
    
    @admin_permission.require()
    def is_accessible(self):
        return True


def init_admin(f_admin):
    from app import db
    from app.models import User, Question

    f_admin.add_view(MyModelView(User, db.session))
    f_admin.add_view(MyModelView(Question, db.session))


def register_principal_identity_signal(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # update the identity with the roles
        if identity.id in app.config['ADMINS']:
            identity.provides.add(admin_role)