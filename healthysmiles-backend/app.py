from flask import Flask, request, send_file
from flask_cors import CORS
from flask_cors import CORS
from PIL import Image
import base64
from imutils import face_utils
import imutils
import dlib
import io
import sys
import numpy as np
import cv2


def visualize_mouth_landmarks(image, img2, shape, shape2, rows, cols, ch, color=(0,0,0), alpha=0.5):
	# Create two copies of the image.  One will apply the overlay to a copy of an output image
	overlay = image.copy()
	output = image.copy()

	# Only need the inner mouth indeces.  This gets the indeces of the intermouth in the shape np array
	(j, k) = face_utils.FACIAL_LANDMARKS_IDXS["inner_mouth"]

	# this will get the points that can create a convex hull on the overlay image
	pts = shape[j:k].astype(np.float32)

	pts2 = shape2[j:k].astype(np.float32)

	print(type(pts), file=sys.stderr)

	print(pts2, file=sys.stderr)

	H = cv2.estimateAffine2D(pts2, pts)

	print(H[0], file=sys.stderr)

	dst = cv2.warpAffine(img2, H[0], (cols, rows))

	print("HERE8", file=sys.stderr)


	mask = np.zeros(dst.shape, np.uint8)

	print("HERE9", file=sys.stderr)

	pts3 = shape[j:k]

	hull = cv2.convexHull(pts3)

	print("HERE10", file=sys.stderr)

	cv2.drawContours(mask, [hull], -1, (255,255,255), -1)

	print("HERE11", file=sys.stderr)


	result3 = cv2.fillPoly(image, pts = [hull], color = (0,0,0))

	mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

	result = cv2.bitwise_and(dst, dst, mask = mask)
	# create a hull with these points

	# hull = cv2.convexHull(pts)

	# draw the hull on the overlay image with the default color

	# cv2.drawContours(overlay, [hull], -1, color, -1)

	# apply the overlay to the output image
	output1 = cv2.addWeighted(dst, alpha, image, 1 - alpha, 1)


	result2 = cv2.bitwise_or(result, result3, mask = None)

	# return the output image
	return result2

app = Flask(__name__)
CORS(app)


@app.route('/api', methods=['POST', 'GET'])
def api():
	# grab json from react
	data = request.get_json()
	resp = 'Nobody'

	# check if data exists
	if data:
		try:
			result = data['data']
			b = bytes(result.get("base64"), 'utf-8')
			image = b[b.find(b',') + 1:]
			im = Image.open(io.BytesIO(base64.b64decode(image)))
			im = im.convert("RGB")
			im.save('./images/image.jpg')

			print("HERE1", file=sys.stderr)

			detector = dlib.get_frontal_face_detector()
			predictor = dlib.shape_predictor("./predictor/shape_predictor_68_face_landmarks.dat")

			print("HERE2", file=sys.stderr)

			image_manip = cv2.imread("./images/image.jpg")
			image_manip = imutils.resize(image_manip, width=250, height=250)

			print("HERE3", file=sys.stderr)

			rows, cols, ch = image_manip.shape

			gray = cv2.cvtColor(image_manip, cv2.COLOR_BGR2GRAY)
			rect = detector(gray, 1)

			print("HERE4", file=sys.stderr)

			img2 = cv2.imread("./images/teeth.jpg")
			gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
			rect2 = detector(gray2, 1)

			print("HERE5", file=sys.stderr)

			print("HERE69", file=sys.stderr)
			
			shape = predictor(gray, rect[0])
			shape = face_utils.shape_to_np(shape)

			print("HERE6", file=sys.stderr)

			shape2 = predictor(gray2, rect2[0])
			shape2 = face_utils.shape_to_np(shape2)

			print("HERE7", file=sys.stderr)

			# visualize all facial landmarks with a transparent overlay
			output = visualize_mouth_landmarks(image_manip, img2, shape, shape2, rows, cols, ch)
			cv2.imwrite("./images/mask_image.png", output)
			cv2.waitKey(0)


		except:
			pass
	return send_file("./images/mask_image.png", mimetype="image/png")
	


if __name__ == '__main__':
	app.run(debug=True)