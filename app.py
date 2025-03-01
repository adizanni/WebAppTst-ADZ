import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

try:
   websitename = os.environ["WEBSITE_SITE_NAME"]
   token_credential = DefaultAzureCredential();
   blob_service_client = BlobServiceClient(
        account_url="https://testappstorageadz1.blob.core.windows.net",
        credential=token_credential
   )
   blob_client = blob_service_client.get_blob_client(container="hellotxt", blob="hello.txt")
   stream = blob_client.download_blob()
   welcomestring = stream.readall().decode()
except:
   welcomestring = "Welcome without blob"
   websitename = "Empty"

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html', welcometxt = welcomestring, websitename = websitename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':

   app.run()