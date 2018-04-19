import sys
sys.path.append("../..")
from setup import cv2, np

def edgeDetection(gray):
    img_gaussian = cv2.GaussianBlur(gray,(3,3),0)
    # Canny
    # myCanny = cv2.Canny(img_gaussian.copy(), img_gaussian.mean(), 200)
    # wide  = cv2.Canny(img_gaussian.copy(), 10, 200)
    # sigma = 0.33
    # v = np.median(gray)
    # lower = int(max(0, (1.0 - sigma) * v))
	# upper = int(min(255, (1.0 + sigma) * v))
	# myCanny = cv2.Canny(image, lower, upper)
    
    # #Laplacian
    myCanny = cv2.Laplacian(gray.copy(),0)
    # print(gray.shape)
    # myCanny = cv2.Canny(gray.copy(), 90, 255)
    # cv2.CV_64F
    
    # #prewitt
    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    kernelx = np.array([[0,0,0],[0,1,0],[0,0,-1]])
    kernely = np.array([[0,0,0],[0,0,1],[0,-1,0]])

    img_prewittx = cv2.filter2D(img_gaussian, -1, kernelx)
    img_prewitty = cv2.filter2D(img_gaussian, -1, kernely)
    myCanny2 = img_prewitty + img_prewittx

    #sobel
    # img_sobelx = cv2.Sobel(img_gaussian,cv2.CV_8U,1,0,ksize=3)
    # img_sobely = cv2.Sobel(img_gaussian,cv2.CV_8U,0,1,ksize=3)
    # myCanny = img_sobelx + img_sobely

    # return myCanny + myCanny2
    return myCanny
