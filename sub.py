from __future__ import print_function

import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2

#dont forget to roslaunch openni2_launch openni2.launch
 

predictor_path = "/home/robin/Feeding/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

class image_converter:

  def __init__(self):
    #self.image_pub = rospy.Publisher("/camera/rgb/image_rect_color",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_rect_color",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    #(rows,cols,channels) = cv_image.shape
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
      shape = predictor(gray, rect)
      shape = face_utils.shape_to_np(shape)
      features = face_utils.FACIAL_LANDMARKS_IDXS.items()
      mouth = features[0]
      points = shape[mouth[1][0]:mouth[1][1]]
      for (x,y) in points: 
        cv2.circle(cv_image, (x, y), 1, (0, 0, 255), -1)

      inside_points = shape[60:68]
      mouth_top = shape[62]
      mouth_bottom = shape[66]
      mouth_center_x = mouth_bottom[0] +(mouth_top[0]-mouth_bottom[0])/2
      mouth_center_y = mouth_bottom[1] +(mouth_top[1]-mouth_bottom[1])/2
      cv2.circle(cv_image, (mouth_center_x, mouth_center_y), 1, (255, 0, 255), 5)
    
      # cv2.polylines(cv_image, [inside_points],True, (0,255,255))
    # if cols > 60 and rows > 60 :
    #   cv2.circle(cv_image, (50,50), 10, 255)

    cv2.imshow("Image window", cv_image)
    cv2.waitKey(1)

    # try:
    #   self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    # except CvBridgeError as e:
    #   print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)