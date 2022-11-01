from flask import Flask, request, send_file
from flask_cors import CORS
from flask_cors import CORS
from PIL import Image
import base64
from imutils import face_utils
import imutils
import dlib
import io
import cv2


def visualize_mouth_landmarks(image, shape, color=(0,0,0), alpha=1):
	# Create two copies of the image.  One will apply the overlay to a copy of an output image
	overlay = image.copy()
	output = image.copy()

	# Only need the inner mouth indeces.  This gets the indeces of the intermouth in the shape np array
	(j, k) = face_utils.FACIAL_LANDMARKS_IDXS["inner_mouth"]

	# this will get the points that can create a convex hull on the overlay image
	pts = shape[j:k]


	# create a hull with these points
	hull = cv2.convexHull(pts)

	# draw the hull on the overlay image with the default color
	cv2.drawContours(overlay, [hull], -1, color, -1)

	# apply the overlay to the output image
	cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

	# return the output image
	return output

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

			detector = dlib.get_frontal_face_detector()
			predictor = dlib.shape_predictor("./predictor/shape_predictor_68_face_landmarks.dat")

			image_manip = cv2.imread("./images/image.jpg")
			image_manip = imutils.resize(image_manip, width=500, height=500)
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