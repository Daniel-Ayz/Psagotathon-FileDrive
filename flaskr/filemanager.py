import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('filemanager', __name__)
files = [x.name for x in os.scandir('static') if x.is_file()]
categories = []

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('home.html', posts=posts)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    category = request.form.get('category')
    if not category:
        return jsonify({'error': 'No category specified'}), 400

    if file:
        file.save("static/" + file.filename)
        files.append((file.filename, category))
        return redirect(url_for('show_files'))


@app.route('/files', methods=['GET'])
def show_files():
    categorized_files = [(file_name, category) for file_name, category in files]
    return render_template('index.html', files=categorized_files, categories=categories)