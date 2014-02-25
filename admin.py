from application import app
from models import User, Role, Subject, Category, Order, File, OS, TaskStatus, ROLE_ADMIN
from database import db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import session as app_session


class AuthModelView(ModelView):

    def is_accessible(self):
        if 'role' in app_session:
            return app_session['role'] == ROLE_ADMIN
        return True

    def __init__(self, model, session, **kwargs):
        ModelView.__init__(self, model, session, **kwargs)


class AdminRoles(AuthModelView):
    column_list = ('id', 'name')

    def __init__(self, session, **kwargs):
        AuthModelView.__init__(self, Role, session, **kwargs)


class AdminUsers(AuthModelView):
    column_list = ('role', 'email', 'username', 'registration_date', 'gmt')

    def __init__(self, session, **kwargs):
        AuthModelView.__init__(self, User, session, **kwargs)


class AdminSubject(AuthModelView):
    def __init__(self, session, **kwargs):
        AuthModelView.__init__(self, Subject, session, **kwargs)


class AdminCategory(AuthModelView):
    def __init__(self, session, **kwargs):
        AuthModelView.__init__(self, Category, session, **kwargs)


class AdminOrder(AuthModelView):
    def __init__(self, session, **kwargs):
        AuthModelView.__init__(self, Order, session, **kwargs)


class AdminFile(AuthModelView):
    def __init__(self, session, **kwargs):
        AuthModelView.__init__(self, File, session, **kwargs)


class AdminOS(AuthModelView):
    def __init__(self, session, **kwargs):
        AuthModelView.__init__(self, OS, session, **kwargs)


class AdminTaskStatus(AuthModelView):
    def __init__(self, session, **kwargs):
        AuthModelView.__init__(self, TaskStatus, session, **kwargs)


admin = Admin(app, name='Control Panel')

admin.add_view(AdminRoles(db.session, name='Roles'))
admin.add_view(AdminUsers(db.session, name='Users'))
admin.add_view(AdminSubject(db.session, name='Subjects'))
admin.add_view(AdminCategory(db.session, name='Categories'))
admin.add_view(AdminOrder(db.session, name='Orders'))
admin.add_view(AdminFile(db.session, name='Files'))
admin.add_view(AdminOS(db.session, name='OS'))
admin.add_view(AdminTaskStatus(db.session, name='Task statuses'))