from flask import Flask
from MyQR import myqr
from os.path import exists
from os import getenv
from hashlib import md5
from flask import send_file
from flask import request
from flask import abort
from config import ApplicationConfig
from py_eureka_client import eureka_client

app = Flask(__name__)

MEDIA_ROOT = 'static/media/'
BACKGROUND_IMAGE = MEDIA_ROOT + 'deloitte.png'
PROPERTIES_URL = getenv('PROPERTIES_URL')

config = ApplicationConfig(PROPERTIES_URL)

try:
    eureka_client.init_registry_client(
        eureka_server=config.eureka_url,
        app_name=config.eureka_instance_name,
        renewal_interval_in_secs=config.eureka_lease_renewal_interval_in_seconds
    )
except Exception:
    print('Failed to init eureka')


@app.route('/')
def hello_world():
    return "Hello, Zebra!"


@app.route('/qrcode', methods=['GET'])
def get_qrcode():
    url = request.args.get('url')
    if url is None:
        return abort(404, "url parameter is required")
    cur_qr_name = md5(url.encode()).hexdigest()+'.png'
    if not exists(MEDIA_ROOT + cur_qr_name):
        myqr.run(url, version=5, picture=BACKGROUND_IMAGE, save_dir=MEDIA_ROOT, save_name=cur_qr_name)
    return send_file(MEDIA_ROOT + cur_qr_name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
