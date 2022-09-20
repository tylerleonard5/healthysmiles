from flask import Flask, request, send_file
from flask_cors import CORS
from flask_cors import CORS
import json
from PIL import Image
import base64
import io
import os
import shutil
import time
import re
import sys


app = Flask(__name__)
CORS(app)


@app.route('/api', methods=['POST', 'GET'])
def api():
	data = request.get_json()
	resp = 'Nobody'

	if data:
		try:
			time.sleep(1)
			result = data['data']
			b = bytes(result.get("base64"), 'utf-8')
			image = b[b.find(b',') + 1:]
			im = Image.open(io.BytesIO(base64.b64decode(image)))
			im = im.convert("RGB")
			im.save('./images/image.jpg')
		except:
			pass
		return send_file("./images/image.jpg", mimetype="image/jpg")
	


if __name__ == '__main__':
	app.run()