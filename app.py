import csv
import json
import os
from jobs import run_mave, run_mnv
from flask import Flask, request, render_template
from werkzeug import secure_filename

from redis import Redis
from rq import Queue

UPLOAD_FOLDER = 'datafiles'
ALLOWED_EXTENSIONS = set(['csv'])

STATIC_URL_PATH = '/static/'

# get options from config file
q = Queue(connection=Redis())

app = Flask(__name__, static_url_path=STATIC_URL_PATH)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_unique_filename(basename):
    tmp_name = os.path.join(app.config['UPLOAD_FOLDER'], basename)
    i = 0
    while os.path.exists(tmp_name):
        tmp_name = os.path.join(app.config['UPLOAD_FOLDER'], str(i)+'_'+basename)
    return tmp_name

def get_datafile_from_request(request):
    data_file = request.files["datafile"]
    if data_file and allowed_file(data_file.filename):
        filename = secure_filename(data_file.filename)
        filename = get_unique_filename(filename)
        # save data file to local storage
        data_file.save(filename)
        return filename
    return None

@app.route('/mnv', methods=['POST'])
def do_mnv():
    assert request.method == 'POST'
    datafile = get_datafile_from_request(request)
    if datafile == None:
        raise Exception("Bad datafile")
    q.enqueue(run_mnv, datafile)
    return

@app.route('/mave', methods=['POST'])
def do_mave():
    assert request.method == 'POST'
    datafile = get_datafile_from_request(request)
    if datafile == None:
        raise Exception("Bad datafile")
    q.enqueue(run_mave, datafile)
    return

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        data_file = request.files["datafile"]
        if data_file and allowed_file(data_file.filename):
            filename = secure_filename(data_file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filename = get_unique_filename(filename)
            # save data file to local storage
            data_file.save(filename)
            # 
            q.enqueue(run_mnv, filename)

    return render_template('index.html', data=None)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
