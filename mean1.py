import numpy as np
import argparse
import cv2
import util
from matplotlib import pyplot as plt

"""
  Current frame of a video that we are processsing
"""
frame = None;

"""
  Boolean flag, indicating whether or not we are currently
  selecting the object we want to track in the video
"""
inputMode = False;
drawing = False
ix,iy = -1,-1
track_window = None
original = None
original2 = None
listaROI = [];
roi_hist = None;
lista_za_histograme = [];
histogram_flag = False;
histogrami = [];
boja1 = (255, 0, 0);
boja2 = (0, 0, 255);
boja = boja1;
brojGresaka = 0


"""
  VideoCapture: Class for video capturing from video files, image sequences or cameras. 
"""
cap = cv2.VideoCapture('C:/Users/lokalac/Desktop/t7.mp4')

"""
    Returns the specified VideoCapture property: video's length, width and height
"""
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT));
width =  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT));
print width; #3260
print height; #570
print  length #7515
cap.release();

"""
    Returns a file object, and is most commonly used withtwo arguments:
    open(filename, mode)
"""
trajectoryFile = open("t7_oznaceno.txt", "r");

"""
    Fill our new dictionary with all rectangles in all frames specified in
    trajectory file
"""
dictionary = {}
dictionary = util.fillDictionary(trajectoryFile, dictionary, length);

def draw_rectangle(event,x,y,flags,param):
    global ix,iy,drawing, original, original2, listaROI, histogram_flag, boja1, boja2, boja;
    if (inputMode == True):
      if event == cv2.EVENT_LBUTTONDOWN:
          drawing = True
          ix,iy = x,y;

      elif event == cv2.EVENT_MOUSEMOVE:
          if drawing == True:
              original2 = original.copy();
              cv2.imshow("frame", original2);
              cv2.rectangle(original2,(ix,iy),(x,y), boja,1)
              cv2.imshow("frame", original2);
            

      elif event == cv2.EVENT_LBUTTONUP:
          drawing = False
          cv2.rectangle(frame,(ix,iy),(x,y),boja, 1)
          cv2.imshow("frame", frame);
          original = frame.copy();
          if (ix < x and iy < y):
            listaROI.append((ix, iy, x - ix, y - iy));
          elif (ix < x and iy > y):
            listaROI.append((ix, y, x - ix, iy - y));
          elif (ix > x and iy < y):
            listaROI.append((x, iy, ix - x, y - iy));
          elif (ix > x and iy > y):
            listaROI.append((x, y, ix - x, iy - y));
          print listaROI[0];


def main():
  ap = argparse.ArgumentParser();
  ap.add_argument("-v", "--video", help = "path to the video file");
  args = vars(ap.parse_args());
  global frame, inputMode, track_window, original, listaROI, roi_hist, dictionary, lista, histogram_flag, boja, boja1, boja2, brojGresaka;
  camera = cv2.VideoCapture(args["video"]);
  cv2.namedWindow('frame')
  cv2.setMouseCallback("frame", draw_rectangle);
  term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
  frameIndex = 0
  listaIndexa = [];#BITNO!
  prvi_put = True;
  zastavica = False;
  img55 = np.zeros((570, 1630, 3), np.uint8);
  img55[:,:] = (0, 255, 0);
  while True:

    ret, frame = camera.read();
    if not ret:
      break;
    
    frame = cv2.resize(frame, None, fx = 0.5, fy = 1, interpolation = cv2.INTER_CUBIC);
    frameIndex += 1;
    if histogram_flag == True:
      hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);
      #cv2.imshow("ihsv", hsv_roi);
      for h in lista_za_histograme:
          
          if h.idIgraca >= 1 and h.idIgraca <= 10:
               #hsv_roi = cv2.cvtColor(frame[h.minRow:h.maxRow, h.minCol:h.maxCol], cv2.COLOR_BGR2HSV);
               mask = cv2.inRange(hsv_roi, np.array((110., 50.,50.)), np.array((140.,255.,255.)));
          elif h.idIgraca >= 13 and h.idIgraca <= 22:
               #hsv_roi = cv2.cvtColor(frame[h.minRow:h.maxRow, h.minCol:h.maxCol], cv2.COLOR_BGR2HSV);
               mask1 = cv2.inRange(hsv_roi, np.array((0., 100., 75.)), np.array((20., 255., 255.)));
               mask2 = cv2.inRange(hsv_roi, np.array((170., 100., 75.)), np.array((179., 255., 255.)));
               mask = mask1 + mask2;
          else:
               print "GOLMAN"
               hsv_roi = cv2.cvtColor(frame[h.minRow:h.maxRow, h.minCol:h.maxCol], cv2.COLOR_BGR2HSV);
               mask = None
          #probati bez maske
          roi_hist = cv2.calcHist([hsv_roi],[0], mask,[180],[0,179]);
          cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

          histogrami.append(roi_hist);
      print "DULJINA", len(histogrami)
      histogram_flag = False;
                        
                                  

    
    if len(listaROI) > 0 and zastavica == False:
      for l in listaROI:
          track_window = l;
          x, y, w, h = track_window;
          zastavica = True;
          rect1 = util.myRectangle (-1, y, y + h, x, x+ w);
          najblizi = util.proxima(rect1, dictionary, frameIndex);
          print najblizi;
          #cv2.rectangle(frame, (najblizi.minCol, najblizi.minRow), (najblizi.maxCol, najblizi.maxRow), 255, 1);
          #cv2.imwrite("primjer.png", frame);
          rect1.setID(najblizi.idIgraca);
          print rect1
          lista_za_histograme.append(rect1);
          listaIndexa.append(najblizi.idIgraca); #BITNO!
          histogram_flag = True;
    if len(histogrami) > 0:
      f = frame[100:470, 26:1538];
      img55[100:470, 26:1538] = f;
      i55 = cv2.cvtColor(img55, cv2.COLOR_BGR2HSV)
      #isprobati hsv
      #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      #cv2.imshow("hsv", hsv);
      #cv2.imshow("i55", img55);
      #cv2.imshow("img55", img55);
      #hsv_part = hsv[100:470, 26:1538];
      #img55[100:470, 26:1538] = hsv_part;
      #cv2.imshow("hsv_part", img55);
      
      k = 0;
      for his in histogrami:
          # hsv ->i55
          backProj = cv2.calcBackProject([i55], [0], his, [0, 180], 1)
          
          #cv2.imshow("bp", backProj);
          ret, listaROI[k] = cv2.meanShift(backProj, listaROI[k], term_crit)
          x,y,w,h = listaROI[k];
          if lista_za_histograme[k].idIgraca >= 1 and lista_za_histograme[k].idIgraca <= 10:
              boja = boja1;
          else:
              boja = boja2;
          zastavica3 = True;
          if frameIndex % 200 == 0:
            
            
            trueRectangles = dictionary[frameIndex + 1];
            indeks1 = lista_za_histograme[k].idIgraca;
            for l in trueRectangles:
                if l.idIgraca == indeks1:
                    print l
                    
                    bioBiRect = util.myRectangle(lista_za_histograme[k].idIgraca, y, y+h, x, x + w);
                    
                    print bioBiRect
                    ud = util.udaljenost(l, bioBiRect);
                    print ud;
                    if (ud > 20):
                        print "Doslo je do pogreske tijekom pracenja, vracamo pravokutnik nad originalni model radi daljnjeg pracenja.";
                        brojGresaka += 1;
                        x = l.minCol;
                        y = l.minRow;
                        w = l.maxCol - l.minCol;
                        h = l.maxRow - l.minRow;
                        listaROI[k] = x, y, w, h;
                        cv2.rectangle(frame, (x, y), (x+w, y+h),boja, 1);
                        zastavica3 = False;
                        
          #cv2.rectangle(backProj, (x,y), (x+w,y+h), boja,1)
          if k == 0:
             #cv2.rectangle(backProj, (x,y), (x+w,y+h), boja,1)
             cv2.imshow("bp", backProj);
          if (zastavica3 == True):
              cv2.rectangle(frame, (x,y), (x+w,y+h), boja,1)
          k = k + 1;
          #cv2.imshow('frame',frame);

    
              
    cv2.imshow("frame", frame);
    key = cv2.waitKey(1) & 0xFF;
    if (key == ord("r") and prvi_put == True):
      zastavica = False;
      prvi_put = False;
      inputMode = True;
      original = frame.copy();
      origi = frame.copy();
      while (True):
        
        key2 = cv2.waitKey(1) & 0xFF;
        if (key2 == ord("e")):
          inputMode = False;
          break;
        elif (key2 == ord ("d")):
            cv2.imshow("frame", origi);
            frame = origi.copy();
            original = origi.copy();
            listaROI = [];
        elif (key2 == ord("c")):
            if (boja == boja1):
                boja = boja2;
            else:
                boja = boja1;
    elif key == ord("q"):
       print "Broj gresaka pri pracenju je: ", brojGresaka
       break;
  camera.release()
  cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
    

