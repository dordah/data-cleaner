from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import os
from DataAnalyzer import DataAnalyzer
import pandas as pd
import json
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/upload', methods=['POST'])
def upload():
    """
    Upload route, responsible for receiving a .csv file from the frontend and sending back a summary.
    :return: Json response to the frontend with column information summary
    """
    res = {'status': 200}
    for filename in request.files:
        f = request.files.get(filename)
        f.save('%s' % secure_filename(filename))
        analyzer = DataAnalyzer(pd.read_csv(secure_filename(filename)))
        res = jsonify({'status': '200', 'message': 'OK', 'data': analyzer.column_summary()})
    return res


@app.route('/clean', methods=['POST', 'OPTIONS'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def clean():
    """
    Cleaning route, responsible for cleaning the data according to the user choices
    and returning the clean .csv file to the user.
    :return: A file download response to the frontend.
    """
    payload = json.loads(request.data.decode('UTF-8'))
    instructions = payload['data']
    filename = payload['filename']
    try:
        analyzer = DataAnalyzer(pd.read_csv(filename), filename)
        if analyzer.clean(instructions):
            return send_file('clean_'+filename, as_attachment=True, download_name='clean_'+filename)
        else:
            return jsonify({'status': '360', 'message': 'Cleaning failed'})
    except FileNotFoundError as e:
        print(e)
        return jsonify({'status': '350', 'message': 'Internal error - original file not found.'})
    finally:
        os.remove(filename)


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.mkdir('uploads')
    app.run(debug=True, port=5000)

