import requests as req, json
import re
from urllib.request import urlopen
from random import random, randint
from bs4 import BeautifulSoup as bs4



class CVW2PDF:
    def __init__(self, url, nameDocs):
        self.url = url
        self.nameDocs = nameDocs

        self.headers = {
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'sec-gpc': '1',
            'origin': 'https://www.ilovepdf.com'
        }



    def getDataWeb(self):
        reqWeb = req.get("https://www.ilovepdf.com/word_to_pdf")
        exebs1 = bs4(reqWeb.text, "html.parser")
        fnd = re.search('var ilovepdfConfig = (.*?);', reqWeb.text).group(1)
        taskId = re.search("ilovepdfConfig.taskId = '(.*?)'", reqWeb.text).group(1)
        loadJson = json.loads(fnd)
        serverResult = loadJson['servers']
        shuffleServers = serverResult[randint(0, len(serverResult))]
        token = loadJson['token']

        result = {
            'bearerToken': token, 
            'servers': shuffleServers, 
            'task': taskId
            }

        return json.dumps(result)


        
    def uploadFileToServer(self):
        loadJson = json.loads(self.getDataWeb())

        postData = {

            'name': self.nameDocs,
            'chunk': 0,
            'chunks': 1,
            'task': loadJson['task'],
            'preview': 1,
            'pdfinfo': 0,
            'pdfforms': 0,
            'pdfresetforms': 0,
            'v': 'web.0'
        }

        fileWhileUpload = (self.nameDocs, urlopen(self.url).read())
        
        self.headers['authorization'] = 'Bearer '+loadJson['bearerToken']

        reqPostUpload = req.post("https:"+loadJson['servers']+"/v1/upload", files={'file': fileWhileUpload}, data=postData, headers=self.headers)

        deJson = json.loads(reqPostUpload.text)
        if 'server_filename' not in deJson:
            return json.dumps({
                'error': True, 
                'msg': 'somethin wrong, try again'
                })
            
        deJson['filename'] = self.nameDocs
        deJson['taskId'] = loadJson['task']
        deJson['server'] = loadJson['servers']

        return json.dumps(deJson)



    def processConvertFile(self):
        loadJson1 = json.loads(self.getDataWeb())
        loadJson2 = json.loads(self.uploadFileToServer())

        postData = {
            'output_filename': '{filename}',
            'packaged_filename': 'ilovepdf_converted',
            'task': loadJson2['taskId'],
            'tool': 'officepdf',
            'files[0][server_filename]': loadJson2['server_filename'],
            'files[0][filename]': loadJson2['filename']
        }

        self.headers['host'] = loadJson2['server'].replace("/", "")
        self.headers['authorization'] = 'Bearer '+loadJson1['bearerToken']

        reqPostProcess = req.post("https:"+loadJson2['server']+"/v1/process", data=postData, headers=self.headers)
        decodeJson = json.loads(reqPostProcess.text)

        decodeJson['download_url'] = "https:" +loadJson2['server']+ "/v1/download/" +loadJson2['taskId']

        return json.dumps(decodeJson)
        


callClass = CVW2PDF("http://localhost:8080/TesUy.docx", "Oghey.docx")
print(callClass.processConvertFile())