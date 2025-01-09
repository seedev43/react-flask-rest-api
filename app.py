# from crypt import methods
from flask import Flask, request
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from modules.ttdl import TikTokDownloader
from modules.word2pdf import WordToPDF
from modules.pdf2word import PDFToWord

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
def word2pdf():
    try:
        file = request.files.get('file')
        
        if not file:
            return {
                "success": False, 
                "message": "file are required"
            }, 400
        
        convertFile = WordToPDF(file, file.filename)
        return convertFile.processConvertFile()
    except Exception as e:
        return {
            "success": False,
                "message": str(e)
        }, 500

@app.route("/api/convert-pdf-to-word", methods=['POST'])
@cross_origin()
def pdf2word():
    try:
        file = request.files.get('file')
        
        if not file:
            return {
                "success": False, 
                "message": "file are required"
            }, 400
        
        convertFile = PDFToWord(file, file.filename)
        return convertFile.processConvertFile()
    except Exception as e:
        return {
            "success": False,
                "message": str(e)
        }, 500


if __name__ == '__main__':
    app.run(debug=True)
