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

success = False

def visualize_mouth_landmarks(image, img2, shape, shape2, rows, cols, ch, color=(0,0,0), alpha=0.5):
	
	# Only need the inner mouth indeces.  This gets the indeces of the intermouth in the shape np array
	(j, k) = face_utils.FACIAL_LANDMARKS_IDXS["inner_mouth"]

	# this will get the points that can create a convex hull on the overlay image
	# need two sets of points. One set is for the uploaded headshot, the other is for the smile replacement
	pts = shape[j:k].astype(np.float32)
	pts2 = shape2[j:k].astype(np.float32)

	# Debug printing
	print(type(pts), file=sys.stderr)
	print(pts2, file=sys.stderr)

	# Estimate the optimal affine transformation between the two point sets.
	H = cv2.estimateAffine2D(pts2, pts)

	# Debug
	print(H[0], file=sys.stderr)

	# Applies the affine transformation to the replacement image
	dst = cv2.warpAffine(img2, H[0], (cols, rows))

	# Create a black canvas for a mask
	mask = np.zeros(dst.shape, np.uint8)

	# Another set of points used for creating a convex hull
	pts3 = shape[j:k]

	# Create a convex hull with the points
	hull = cv2.convexHull(pts3)

	# Draw the hull on the mask with white 
	cv2.drawContours(mask, [hull], -1, (255,255,255), -1)

	# Black out the same hull on the uploaded image so it can be cominded with the masked out image of the replacement image
	result3 = cv2.fillPoly(image, pts = [hull], color = (0,0,0))

	# Mask to gray
	mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

	# Crop out smile of the replacement 
	result = cv2.bitwise_and(dst, dst, mask = mask)


	# # apply the overlay to the output image
	# output1 = cv2.addWeighted(dst, alpha, image, 1 - alpha, 1)

	# Combine the masked out replacement with the original using bitwise or operation
	result2 = cv2.bitwise_or(result, result3, mask = None)

	# return the output image
	return result2

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST', 'GET'])
def api():
	global success
	# grab json from react
	data = request.get_json()
	resp = 'Nobody'
	error = False

	# check if data exists
	if data:
		try:
			result = data['data']
			b = bytes(result.get("base64"), 'utf-8')
			image = b[b.find(b',') + 1:]
			im = Image.open(io.BytesIO(base64.b64decode(image)))
			im = im.convert("RGB")
			im.save('./images/image.jpg')

			# HOG SVM implementation of facial detector
			detector = dlib.get_frontal_face_detector()

			# Predict points for fascial landmarks
			predictor = dlib.shape_predictor("./predictor/shape_predictor_68_face_landmarks.dat")

			# Get original image and resize
			image_manip = cv2.imread("./images/image.jpg")
			image_manip = imutils.resize(image_manip, width=500, height=500)

			# rows, cols, ch 
			rows, cols, ch = image_manip.shape

			# get rect with detector
			gray = cv2.cvtColor(image_manip, cv2.COLOR_BGR2GRAY)
			rect = detector(gray, 1)

			# Get rect2 with detector as well
			img2 = cv2.imread("./images/smiles/teeth3.jpg")
			gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
			rect2 = detector(gray2, 1)

			print(len(rect), file=	sys.stderr)
			if len(rect) != 1:
				raise Exception("error")


			# Grab numpy arrays for the points of the landmarks
			shape = predictor(gray, rect[0])
			shape = face_utils.shape_to_np(shape)

			# Second numpy array
			shape2 = predictor(gray2, rect2[0])
			shape2 = face_utils.shape_to_np(shape2)

			# run code to get replacement image
			output = visualize_mouth_landmarks(image_manip, img2, shape, shape2, rows, cols, ch)
			cv2.imwrite("./images/mask_image.png", output)
			cv2.waitKey(0)

		# Error handling
		except:
			print("here", file=sys.stderr)
			error = True
	
	if error:
		print("here1", file=sys.stderr)
		#return send_file("./images/image.jpg", mimetype="image/jpg")
		success = False
		return 'error'
	else:
		print("here2", file=sys.stderr)
		#return send_file("./images/mask_image.png", mimetype="image/png")
		success = True
		return 'true'



# Second endpt for getting the image
@app.route('/get', methods=['GET'])
def get():
	global success
	if not success:
		print("here3", file=sys.stderr)
		# return send_file("./images/image.jpg", mimetype="image/jpg")
		return 'error'
	else:
		print("here4", file=sys.stderr)
		return send_file("./images/mask_image.png", mimetype="image/png")
	


if __name__ == '__main__':
	app.run(debug=True)