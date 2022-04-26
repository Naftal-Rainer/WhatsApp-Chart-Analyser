# from crypt import methods
from flask import Flask, flash, redirect, render_template, session, url_for, request, send_from_directory
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import chatanalyser


UPLOAD_FOLDER = "static/"
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.secret_key = "hello_world"
app.permanent_session_lifetime = timedelta(minutes = 5)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to check for valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('blank.html')

@app.route('/results')
def results():
    if 'user' in session:
        user = session['user']
        return render_template('index.html', user=user)
    else: 
        return redirect(url_for('login'))
    # return render_template('index.html', user=usr)


@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        nm = request.form['nm']
        email = request.form['email']
        password = request.form['password']
        session['user'] = nm
        session['email'] = email
        session['password'] = password
        details = [session['user'],session['email'],session['password']]
        session['details'] = details
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            return redirect(url_for('user'))
        return render_template('login.html')


@app.route('/user')
def user():
    if 'user' in session:
        flash('You were successfully logged in','success')
        return  redirect(url_for('results'))
    else:
        error = 'Invalid username or password'
        return redirect(url_for('login', error = error))
    

@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        flash('You have been logged out {}!'.format(user),'info')
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/details')
def details():
    if 'details' in session:
        detail = session['details']
        ht = ['Name: ','Email: ', 'Password:  ']
        return  render_template('profile.html', identity = zip(detail,ht))
    else:
        return render_template('error.html')
    

@app.route('/upload', methods = ['POST','GET'])
def upload():
    if request.method == 'POST':
        # Check if file is present in the post request
        if 'file' not in request.files:
            flash('No file part','warning')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            flash('File Uploaded Successfully')
            session['file'] = filename
            df = chatanalyser.get_chat(filepath)
            t_messages = chatanalyser.total_messages(df)
            m_messages = chatanalyser.media_message(df)
            l_messages = chatanalyser.links(df) 
            chatanalyser.most_used_words(df)
            # src={{ url_for('static', filename = chatanalyser.most_used_words(df)) }}
            return render_template('index.html', tm = t_messages,mm = m_messages,lm = l_messages)
            # return redirect(request.url, tm = t_messages)
            # return redirect(url_for('view_file', name = filename))
        # file = open(app.config['UPLOAD_FOLDER'] + filename, 'r')
        # content = file.read()
        # # return 'file uploaded successfully'
    return render_template('index.html')
    

@app.route('/raw_file')
def raw_file():
        if 'file' in session:
            name = session['file']
            return redirect(url_for('view_file', name = name))

@app.route('/view_file/<name>')
def view_file(name):
        if 'file' in session:
            name = session['file']
            return send_from_directory(app.config['UPLOAD_FOLDER'], name)
        else:
            return render_template('error.html')
    
if __name__ == '__main__':
    app.run(debug=True)