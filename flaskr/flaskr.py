#imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, \
                render_template, flash


# create the app
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from env. vars.
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flasker.db'),
    SECRET_KEY='development_key',
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('FLASKER_SETTINGS', silent=True)
""" DATABASE FUNCTIONS """
# connecting DATABASE
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# assigning to sqlite database
def get_db():
    if not hasattr(g, 'sqlite.db'):
        g.sqlite_db = connect_db()

    return g.sqlite_db

# closing db connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print 'Database Initalized'

""" VIEW FUNCTIONS """
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',\
                [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry success!')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out !')
    return redirect(url_for('show_entries'))
