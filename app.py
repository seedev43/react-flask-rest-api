from crypt import methods
from flask import Flask, request
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from modules.ttdl import TikTokDownloader
from modules.cvw2pdf import CVW2PDF

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/test", methods=['GET'])
@cross_origin()
def testPage():
    return "This is test page"


@app.route("/api/tiktokdl/", methods=['POST'])
@cross_origin()
def TikTokDL():
    if request.form['url']:
        url = request.form['url']
        return TikTokDownloader(url)


@app.route("/api/convert-word-to-pdf", methods=['POST'])
@cross_origin()
def cvpage():
    if request.files['file'] and request.form['filename']:
        url = request.files['file']
        fileName = request.form['filename']
        convertFile = CVW2PDF(url, fileName)
        return convertFile.executeProcess()


if __name__ == '__main__':
    app.run()
