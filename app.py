from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_db, close_db
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

@app.route('/')
def index():
    db = get_db()
    projects = db.execute('SELECT * FROM projects').fetchall()
    return render_template('index.html', projects=projects)

@app.route('/project/<int:project_id>')
def project(project_id):
    db = get_db()
    project = db.execute('SELECT * FROM projects WHERE id = ?', (project_id,)).fetchone()
    progress = db.execute('SELECT * FROM progress WHERE project_id = ?', (project_id,)).fetchall()
    features = db.execute('SELECT * FROM features WHERE project_id = ?', (project_id,)).fetchall()
    thoughts = db.execute('SELECT * FROM thoughts WHERE project_id = ?', (project_id,)).fetchall()
    return render_template('project.html', project=project, progress=progress, features=features, thoughts=thoughts)

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db = get_db()
        db.execute('INSERT INTO projects (name, description) VALUES (?, ?)', (name, description))
        db.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_project.html')

@app.route('/add_progress/<int:project_id>', methods=['GET', 'POST'])
def add_progress(project_id):
    if request.method == 'POST':
        progress_update = request.form['update']
        db = get_db()
        db.execute('INSERT INTO progress (project_id, progress_update, date) VALUES (?, ?, ?)', 
                   (project_id, progress_update, datetime.now().strftime('%Y-%m-%d')))
        db.commit()
        flash('Progress updated!', 'success')
        return redirect(url_for('project', project_id=project_id))
    return render_template('add_progress.html', project_id=project_id)

@app.route('/add_feature/<int:project_id>', methods=['GET', 'POST'])
def add_feature(project_id):
    if request.method == 'POST':
        feature = request.form['feature']
        db = get_db()
        db.execute('INSERT INTO features (project_id, feature) VALUES (?, ?)', (project_id, feature))
        db.commit()
        flash('Feature added!', 'success')
        return redirect(url_for('project', project_id=project_id))
    return render_template('add_feature.html', project_id=project_id)

@app.route('/add_thought/<int:project_id>', methods=['GET', 'POST'])
def add_thought(project_id):
    if request.method == 'POST':
        thought = request.form['thought']
        db = get_db()
        db.execute('INSERT INTO thoughts (project_id, thought) VALUES (?, ?)', (project_id, thought))
        db.commit()
        flash('Thought added!', 'success')
        return redirect(url_for('project', project_id=project_id))
    return render_template('add_thought.html', project_id=project_id)

@app.route('/convert_thought/<int:project_id>/<int:thought_id>', methods=['GET', 'POST'])
def convert_thought(project_id, thought_id):
    db = get_db()
    thought = db.execute('SELECT * FROM thoughts WHERE id = ?', (thought_id,)).fetchone()
    if request.method == 'POST':
        feature = request.form['feature']
        db.execute('INSERT INTO features (project_id, feature) VALUES (?, ?)', (project_id, feature))
        db.execute('DELETE FROM thoughts WHERE id = ?', (thought_id,))
        db.commit()
        flash('Thought converted to feature!', 'success')
        return redirect(url_for('project', project_id=project_id))
    return render_template('convert_thought.html', project_id=project_id, thought=thought)

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    db = get_db()
    # Delete related progress, features, and thoughts first due to foreign key constraints
    db.execute('DELETE FROM progress WHERE project_id = ?', (project_id,))
    db.execute('DELETE FROM features WHERE project_id = ?', (project_id,))
    db.execute('DELETE FROM thoughts WHERE project_id = ?', (project_id,))
    db.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    db.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_progress/<int:project_id>/<int:progress_id>', methods=['POST'])
def delete_progress(project_id, progress_id):
    db = get_db()
    db.execute('DELETE FROM progress WHERE id = ?', (progress_id,))
    db.commit()
    flash('Progress update deleted!', 'success')
    return redirect(url_for('project', project_id=project_id))

@app.route('/delete_feature/<int:project_id>/<int:feature_id>', methods=['POST'])
def delete_feature(project_id, feature_id):
    db = get_db()
    db.execute('DELETE FROM features WHERE id = ?', (feature_id,))
    db.commit()
    flash('Feature deleted!', 'success')
    return redirect(url_for('project', project_id=project_id))

@app.route('/delete_thought/<int:project_id>/<int:thought_id>', methods=['POST'])
def delete_thought(project_id, thought_id):
    db = get_db()
    db.execute('DELETE FROM thoughts WHERE id = ?', (thought_id,))
    db.commit()
    flash('Thought deleted!', 'success')
    return redirect(url_for('project', project_id=project_id))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)