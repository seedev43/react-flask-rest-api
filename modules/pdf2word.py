import requests as req
import json
import re
from urllib.request import urlopen
from random import random, randint
from bs4 import BeautifulSoup as bs4


class PDFToWord:
    def __init__(self, url, nameDocs):
        self.url = url
        self.nameDocs = nameDocs

        self.headers = {
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'sec-gpc': '1',
            'origin': 'https://www.ilovepdf.com'
        }

    def get_config_data(self):
        response = req.get("https://www.ilovepdf.com/pdf_to_word")
        # soup = bs4(response.text, "html.parser")
        config_match = re.search('var ilovepdfConfig = (.*?);', response.text)
        task_id_match = re.search("ilovepdfConfig.taskId = '(.*?)'", response.text)
        
        if not config_match or not task_id_match:
            raise Exception("Failed to retrieve web configuration")

        config_data = json.loads(config_match.group(1))
        servers = config_data['servers']
        random_server = servers[randint(0, len(servers) - 1)]
        token = config_data['token']

        return {
            'bearer_token': token,
            'servers': random_server,
            'task': task_id_match.group(1)
        }

    def upload_file_to_server(self):
        config = self.get_config_data()

        post_data = {
            'name': self.nameDocs,
            'chunk': 0,
            'chunks': 1,
            'task': config['task'],
            'preview': 1,
            'pdfinfo': 0,
            'pdfforms': 0,
            'pdfresetforms': 0,
            'v': 'web.0'
        }

        file_to_upload = (self.nameDocs, self.url)
        self.headers['authorization'] = f"Bearer {config['bearer_token']}"

        upload_response = req.post("https://"+config['servers']+".ilovepdf.com/v1/upload", files={
                                 'file': file_to_upload}, data=post_data, headers=self.headers)

        upload_result = json.loads(upload_response.text)
        
        if 'server_filename' not in upload_result:
            raise Exception("File upload failed")

        upload_result['filename'] = self.nameDocs
        upload_result['taskId'] = config['task']
        upload_result['server'] = config['servers']

        return upload_result

    def processConvertFile(self):
        config = self.get_config_data()
        upload_result = self.upload_file_to_server()

        post_data = {
            'convert_to': 'docx',
            'output_filename': '{filename}',
            'packaged_filename': 'ilovepdf_converted',
            'ocr': 1,
            'task': upload_result['taskId'],
            'tool': 'pdfoffice',
            'files[0][server_filename]': upload_result['server_filename'],
            'files[0][filename]': upload_result['filename']
        }
        
        self.headers['host'] = upload_result['server'] + ".ilovepdf.com"
        self.headers['authorization'] = f"Bearer {config['bearer_token']}"

        process_response = req.post("https://"+upload_result['server']+".ilovepdf.com/v1/process", data=post_data, headers=self.headers)
        
        process_result = json.loads(process_response.text)

        process_result['download_url'] = "https://" + upload_result['server'] + ".ilovepdf.com/v1/download/" + upload_result['taskId']

        process_result['success'] = True
        process_result['msg'] = "Success convert file"
        
        return process_result
