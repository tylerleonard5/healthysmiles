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
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2


def visualize_mouth_landmarks(image, shape, colors=None, alpha=0.75):
	# create two copies of the input image -- one for the
	# overlay and one for the final output image
	overlay = image.copy()
	output = image.copy()

	# if the colors list is None, initialize it with a unique
	# color for each facial landmark region
	if colors is None:
		colors = [(0,0,0), (0,0,0), (0,0,0),
			(0,0,0), (0,0,0),
			(0,0,0), (0,0,0), (0,0,0)]

	# loop over the facial landmark regions individually
	for (i, name) in enumerate(face_utils.FACIAL_LANDMARKS_IDXS.keys()):
		# grab the (x, y)-coordinates associated with the
		# face landmark
		if name == "inner_mouth":
			(j, k) = face_utils.FACIAL_LANDMARKS_IDXS[name]
			pts = shape[j:k]

			# check if are supposed to draw the jawline
			if name == "jaw":
				# since the jawline is a non-enclosed facial region,
				# just draw lines between the (x, y)-coordinates
				for l in range(1, len(pts)):
					ptA = tuple(pts[l - 1])
					ptB = tuple(pts[l])
					cv2.line(overlay, ptA, ptB, colors[i], 2)

			# otherwise, compute the convex hull of the facial
			# landmark coordinates points and display it
			else:
				hull = cv2.convexHull(pts)
				cv2.drawContours(overlay, [hull], -1, colors[i], -1)

	# apply the transparent overlay
	cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

	# return the output image
	return output

app = Flask(__name__)
CORS(app)


@app.route('/api', methods=['POST', 'GET'])
def api():
	data = request.get_json()
	resp = 'Nobody'

	if data:
		try:
			result = data['data']
			b = bytes(result.get("base64"), 'utf-8')
			image = b[b.find(b',') + 1:]
			im = Image.open(io.BytesIO(base64.b64decode(image)))
			im = im.convert("RGB")
			im.save('./images/image.jpg')

			detector = dlib.get_frontal_face_detector()
			predictor = dlib.shape_predictor("./predictor/shape_predictor_68_face_landmarks.dat")

			image_manip = cv2.imread("./images/image.jpg")
			image_manip = imutils.resize(image_manip, width=500)
			gray = cv2.cvtColor(image_manip, cv2.COLOR_BGR2GRAY)
			rects = detector(gray, 1)

			for (i, rect) in enumerate(rects):
				shape = predictor(gray, rect)
				shape = face_utils.shape_to_np(shape)
				# visualize all facial landmarks with a transparent overlay
				output = visualize_mouth_landmarks(image_manip, shape)
				cv2.imwrite("./images/mask_image.png", output)
				cv2.waitKey(0)


		except:
			pass
	return send_file("./images/mask_image.png", mimetype="image/png")
	


if __name__ == '__main__':
	app.run()