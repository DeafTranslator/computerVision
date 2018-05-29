import sys
sys.path.append("../..")
from setup import cv2, np, myCV, saveMode, save_path, blurryLim, filterName


def variance_of_laplacian(image):
  return cv2.Laplacian(image, cv2.CV_64F).var()


def blurDetection(shades, inI, name, outI, fld, namePath):
  blurryFlag = False
  good = True
  fm = 0

  file = open("blurSimple.txt", "r+")
  for image in shades:
    grayHand = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    old = file.read()
    file.seek(0)
    if type(grayHand) is np.ndarray:
      fm = variance_of_laplacian(grayHand)
      file.write("{0}\t{1}\t{2}\t{3}\n".format(old, name, fm, str(grayHand.shape)))
    else:
      good = False
      break


    if fm < blurryLim:
      blurryFlag = True
      # k = cv2.waitKey(0)
      break

  file.close()

  text = "Not blurry"
  if blurryFlag is True:
    text = "Blurry"
    # return False
  # return True
  elif saveMode:
    myCV.saveImage(name, outI.copy(), save_path +'\\'+ namePath, fld, filterName)
    print("saved")

  if good is True:
    return cv2.putText(inI, "{}: {:.2f}".format(text,fm), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

  return False
