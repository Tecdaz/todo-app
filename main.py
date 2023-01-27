import unittest

from flask import make_response, redirect, render_template, flash, url_for
from flask_login import login_required, current_user

from app import create_app
from app.firestore_service import get_todos, put_todo, delete_todo, update_todo
from app.forms import TodoForm

app = create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    response = make_response(redirect('hello'))
    return response


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    username = current_user.username
    todo_form = TodoForm()
    context = {
        'todos': get_todos(current_user.id),
        'username': username,
        'todo_form': todo_form,
    }

    if todo_form.validate_on_submit():
        put_todo(current_user.id, todo_form.description.data)
        flash('Tarea creada con exito!', 'success')
        return redirect(url_for('hello'))

    return render_template('hello.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id, todo_id)
    return redirect(url_for('hello'))


@app.route('/todos/update/<todo_id>', methods=['POST'])
def update(todo_id):
    user_id = current_user.id
    update_todo(user_id, todo_id)
    return redirect(url_for('hello'))
