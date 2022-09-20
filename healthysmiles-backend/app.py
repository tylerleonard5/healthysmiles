from flask import Flask, request
from flask_cors import CORS
import json
from PIL import Image
import base64
import io
import os
import shutil
import time


app = Flask(__name__)
CORS(app)


@app.route('/api', methods=['POST', 'GET'])
def api():
	data = request.get_json()
	resp = 'Nobody'
	directory = './images'

	if data:
		try:
			result = data['data']
			b = bytes(result, 'utf-8')
			image = b[b.find(b'/9'):]
			im = Image.open(io.BytesIO(base64.b64decode(image)))
			im.save(directory+'/image.jpeg')
		except:
			pass
	return resp
	


if __name__ == '__main__':
	app.run()