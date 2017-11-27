from sklearn.cluster import KMeans
import utils
import cv2
import os
import glob
import tools
import numpy as np
import math

senia = 'prueba'

train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\25-11-2017\\Juan\\'+senia+'\\rgb'
video_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\videos\\25-11-2017\\Juan\\' + senia
save_path =  'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\25-11-2017\\Juan\\'+senia+'\\rgb'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classesAll = ['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesDinamic = ['prueba']
classes = classesDinamic

frame = None
inputMode = False
roiPts = []
idxName = 1
# prueba
# roiPts = [(310, 228), (322, 148), (303, 195), (331, 189), (380, 229), (393, 173), (365,204), (369,146)]
cantPoint = 8

rWidth = 450
rHeight = 700

def stdImage(frame):
  # Image del cuadro en la pantalla
  color1 = frame[:,:, 0]
  color2 = frame[:,:, 1]
  color3 = frame[:,:, 2]

  # Colocar la imagen de NxN dimensiones en una sola dimension N^2
  color1 = color1.reshape(-1)
  color2 = color2.reshape(-1)
  color3 = color3.reshape(-1)

  # Promedio de color para cada canal de la imagen
  meanColor1 = np.average(color1)
  meanColor2 = np.average(color2)
  meanColor3 = np.average(color3)

  # Desviacion estandar de la imagen
  stdColor1 = np.std(color1)
  stdColor2 = np.std(color2)
  stdColor3 = np.std(color3)

  # colors = frame.reshape((frame.shape[0] * frame.shape[1], 3))
  # stdColors = 


  return stdColor1, stdColor2, stdColor3

def centroid_histogram(clt):
  # grab the number of different clusters and create a histogram
  # based on the number of pixels assigned to each cluster
  numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
  (hist, _) = np.histogram(clt.labels_, bins = numLabels)
 
  # normalize the histogram, such that it sums to one
  hist = hist.astype("float")
  hist /= hist.sum()
 
  # return the histogram
  return hist

def plot_colors(hist, centroids):
  # initialize the bar chart representing the relative frequency
  # of each of the colors
  bar = np.zeros((50, 300, 3), dtype = "uint8")
  startX = 0
 
  # loop over the percentage of each cluster and the color of
  # each cluster
  for (percent, color) in zip(hist, centroids):
    # plot the relative percentage of each cluster
    endX = startX + (percent * 300)
    cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
      color.astype("uint8").tolist(), -1)
    startX = endX
  
  # return the bar chart
  return bar

def readFolder2():
    global frame
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(train_path, fld,'*g')
        files = glob.glob(path)
        for fl in files:
            img = cv2.imread(fl)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            stdColor1, stdColor2, stdColor3 = stdImage(img.copy())

            img2 = img.copy().reshape((img.shape[0] * img.shape[1], 3))
            
            # cluster the pixel intensities
            clt = KMeans(n_clusters = 1)
            clt.fit(img2)

            hist = centroid_histogram(clt)
            bar = plot_colors(hist, clt.cluster_centers_)

            # print(bar.mean())
            print("std1 {0}, \tstd2 {1}, \tstd3 {2}, \nclt1 {3}, \tclt2 {4}, \tclt3 {5}\n".format(stdColor1,stdColor2,stdColor3,  bar[:,:,0].mean(), bar[:,:,1].mean(), bar[:,:,2].mean()))

            cv2.destroyAllWindows()
            cv2.imshow("frame", img)
            cv2.imshow("hist3", bar)
            k = cv2.waitKey(0)

            if k == ord("e"):
                break

        if k == ord("e"):
            break

readFolder2()
