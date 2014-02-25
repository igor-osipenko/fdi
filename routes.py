from flask import request, render_template, url_for, redirect, flash, session, make_response
from application import app
from database import db, DB_PATH
from models import User, Subject, Category, Role, Order, File, OS, TaskStatus, ROLE_ADMIN
from admin import admin
import forms
import hashlib
import uuid
import os

_CATEGORY_ERROR = 'app_error'
_CATEGORY_MESSAGE = 'app_message'


# ################ AJAX ##############################################################

@app.route('/tools/lff', methods=['POST'])
def load_feedback_form():
    if 'username' not in session:
        return 'error'

    if 'order_id' not in request.form:
        return 'error'

    try:
        order_id = int(request.form['order_id'])
    except Exception:
        return 'error'

    return render_template('review_form.html', order_id=order_id)


@app.route('/tools/do', methods=['POST'])
def delete_order():

    if 'username' not in session:
        return 'error'

    if 'id' not in request.form:
        return 'error'

    try:
        order_id = int(request.form['id'])
    except Exception:
        return 'error'

    o = Order.query.filter_by(user_id=int(session['user_id']), id=order_id).first()
    o.is_deleted = True
    db.session.commit()

    return 'true'


@app.route('/tools/gc', methods=['POST'])
def get_categories():

    if 'username' not in session:
        return ''

    if 's' not in request.form:
        return ''

    try:
        subject_id = int(request.form['s'])
    except TypeError:
        return ''

    categories = Category.query.filter_by(subject_id=subject_id)
    options = '<option value="0">Select...</option>'

    for c in categories:
        options += '<option value="%s">%s</option>' % (c.id, c.name)

    return options


@app.route('/tools/god', methods=['POST'])
def get_order_details():

    from time import sleep

    sleep(1.3)

    if 'username' not in session:
        return ''

    if 'id' not in request.form:
        return ''

    headers = ('ID:', 'Title:', 'Deadline:', 'OS:', 'Detailed explanations:',
               'Subject:', 'Category:', 'Details:', 'Price:')

    try:
        order_id = int(request.form['id'])
    except TypeError:
        return ''

    _order = Order.query.with_entities(Order.id, Order.title, Order.deadline, OS.name,
                                      Order.explanations, Subject.name, Category.name, Order.details, Order.price)\
        .filter_by(user_id=session['user_id'], id=order_id)\
        .join(Order.category)\
        .join(Order.subject)\
        .join(Order.os)\
        .all()[0]

    keys = ('id', 'title', 'deadline', 'os', 'explanations', 'subject', 'category', 'details', 'price')
    _order = dict(zip(keys, zip(headers, _order)))

    order_files = File.query.filter_by(order_id=_order['id'][1]).all()

    return render_template('order_details.html', order=_order, files=order_files)

# ################ AJAX END ##############################################################


@app.route('/very_secret_admin_login_form', methods=['GET', 'POST'])
def admin_login():
    form = forms.AdminLoginForm(request.form)

    if request.method == 'POST' and form.validate():
        password = hashlib.sha512(form.password.data).hexdigest()
        user = User.query.filter_by(email=form.email.data, password=password, role_id=ROLE_ADMIN).first()
        if user is None:
            flash('Invalid login information :(', _CATEGORY_ERROR)
            return render_template('admin_login.html', form=form)

        session['username'] = user.username
        session['user_id'] = user.id
        session['role'] = ROLE_ADMIN
        return redirect('/admin')

    return render_template('admin_login.html', form=form)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    return render_template('reviews.html')


@app.route('/download/<file_uuid>', methods=['GET'])
def download(file_uuid):

    if 'username' not in session:
        return ''

    order_file = File.query.filter_by(local_name=file_uuid).first()

    path = os.path.join('files', order_file.local_name)

    try:
        with open(path, 'rb') as f:
            content = f.read()
    except IOError:
        return redirect('/')

    response = make_response(content)
    response.headers["Content-Disposition"] = "attachment; filename=" + order_file.name
    return response


@app.route('/')
def hello_world():
    return render_template('index.html', title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'username' in session:
        return redirect('/profile')

    form = forms.LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            str(form.password.data)
        except UnicodeEncodeError:
            return redirect('/')

        password = hashlib.sha512(form.password.data).hexdigest()
        user = User.query.filter_by(email=form.email.data, password=password).first()
        if user is None:
            flash('Invalid login information :(', _CATEGORY_ERROR)
            return render_template('login.html', form=form)

        session['username'] = user.username
        session['user_id'] = user.id
        return redirect('/profile')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if 'username' in session:
        return redirect(url_for('/profile'))

    form = forms.RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Sorry, but this email is already used :(', _CATEGORY_ERROR)
            return render_template('register.html', form=form)

        try:
            gmt = int(request.form['timezone'])
        except TypeError:
            return render_template('register.html', form=form)

        user = User(e=form.email.data, un=form.name.data, psw=form.password.data, gmt=gmt)
        db.session.add(user)
        db.session.commit()

        flash('Hoooooray! You have registered at our awesome service :)', _CATEGORY_MESSAGE)
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    orders = Order.query.filter_by(user_id=int(session['user_id']), is_deleted=False).all()
    return render_template('profile.html', orders=orders)


@app.route('/logout')
def logout():
    session.pop('role', None)
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/')


@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'username' not in session:
        return redirect(url_for('login'))

    form = forms.OrderForm(formdata=request.form)
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(subject_id=form.subject.data)]

    if ('0', 'Select...') not in form.subject.choices:
        form.subject.choices.insert(0, ('0', 'Select...'))

    if request.method == 'POST' and form.validate():

        new_order = Order()

        new_order.title = form.title.data
        new_order.user_id = session['user_id']
        new_order.subject_id = form.subject.data
        new_order.category_id = form.category.data
        new_order.os_id = form.os.data
        new_order.details = form.details.data
        new_order.deadline = form.deadline.data
        new_order.explanations = form.explanations.data

        db.session.add(new_order)
        db.session.commit()

        files = request.files.getlist('file[]')
        order_files = []
        for f in files:
            if f.filename:
                ext = f.filename.split('.')[-1]
                name = str(uuid.uuid4()) + '.' + ext
                path = os.path.join(app.config['FILE_UPLOAD_PATH'], name)
                f.save(path)

                of = File()
                of.order_id = new_order.id
                of.name = f.filename
                of.local_name = name
                order_files.append(of)

        for of in order_files:
            db.session.add(of)

        db.session.commit()

        flash('Order submitted :)', _CATEGORY_MESSAGE)

        return redirect(url_for('profile'))

    return render_template('order.html', form=form)


def create_db():
    import os
    if os.path.exists(DB_PATH):
        return
    
    db.create_all()

    roles = [u'user', u'operator', u'administrator']
    subjects = [u'Programming']
    categories = [
        u'ASP.NET',
        u'Assembler',
        u'C',
        u'C#',
        u'C++',
        u'Delphi | Pascal',
        u'Java',
        u'HTML | CSS | JavaScript',
        u'Oracle',
        u'Python',
        u'QT',
        u'SQL | MySQL | MS SQL | PL/SQL',
        u'Visual Basic',
        u'Other'
    ]
    os_list = [u'Windows', u'Unix-like']

    task_statuses = [
        ('New', 'Client submitted the new task and operator hasn\'t got it yet'),
        ('Discussion', 'Operator discussing details with Client'),
        ('Solving', 'Task went off to solving'),
        ('Pending', 'Payment is going to be delivered soon by PayPal'),
        ('Done', 'User received solution'),
    ]

    for r in roles:
        db.session.add(Role(r))
    db.session.commit()

    for s in subjects:
        db.session.add(Subject(s))
    db.session.commit()

    s = Subject.query.filter_by(name=u'Programming').first()

    for c in categories:
        db.session.add(Category(name=c, subject_id=s.id))

    for o in os_list:
        db.session.add(OS(n=o))

    for ts in task_statuses:
        db.session.add(TaskStatus(*ts))

    db.session.commit()


if __name__ == '__main__':
    create_db()
    app.run(debug=True, host='0.0.0.0')
