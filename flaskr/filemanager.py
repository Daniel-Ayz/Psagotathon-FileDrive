import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('filemanager', __name__)
files = [x.name for x in os.scandir('uploaded') if x.is_file()]


@bp.route('/')
def index():
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    return render_template('home.html', files=files)


@bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # category = request.form.get('category')
    # if not category:
    #     return jsonify({'error': 'No category specified'}), 400

    if file:
        file.save("uploaded/" + file.filename)
        files.append(file.filename)
        return redirect(url_for('filemanager.show_files'))


@bp.route('/files', methods=['GET'])
def show_files():
    return render_template('home.html', files=files)


@bp.route('/view/<filename>', methods=['GET'])
def view_file(filename):
    file_contents = ""
    if not (filename.endswith('.png') or filename.endswith('.pdf')):
        with open(filename, 'r') as f:
            file_contents = f.read()
    return render_template('view.html', filename=filename, file_contents=file_contents)


# @bp.route('/add_category', methods=['POST'])
# @login_required
# def add_category():
#     new_category = request.form.get('new_category')
#     if not new_category:
#         return jsonify({'error': 'No category specified'}), 400
#
#     categories.append(new_category)
#     return redirect(url_for('show_files'))
