import cv2;
import pygame;
import math;


"""
        Razred MyRectangle predstavlja pravokutnik koji obavija igraca i zadan
        je unutar datoteke t1_oznaceno.txt. Osnovne komponente su najmanja i
        najveca x vrijednost, kao i najmanja i najveca y vrijednost cime imamo
        koordinate svih vrhova, a time sirinu, visinu , i koordinate centra
        samog pravokutnika
        
"""

class myRectangle:
        def __init__(self, idIgraca, minRow, maxRow, minCol, maxCol):
              self.idIgraca = idIgraca;
              self.minRow = minRow;
              self.maxRow = maxRow;
              self.minCol = minCol;
              self.maxCol = maxCol;
        def getWidth(self):
              razlika = self.maxCol - self.minCol;
              return razlika;
        def getHeight(self):
              razlika = self.maxRow - self.minRow;
              return razlika;
        def getCenterRow(self):
              centerRow = (self.minRow + self.maxRow) / 2;
              return centerRow;
        def getCenterCol(self):
               centerCol = (self.minCol + self.maxCol) / 2;
               return centerCol;
        def setID(self, idIgraca):
                self.idIgraca = idIgraca;
        def __str__(self):
               return 'ID: {}, x: {}, y: {}, width: {}, height: {}'.format(self.idIgraca, self.minRow, self.minCol, self.getWidth(), self.getHeight()); 
      


#Rjecnici koriste rasprseno adresiranje (hashing), konstantno prosjecno vrijeme pristupa, umetanja i brisanja za
# razliku od lista kod koje umetanje i brisanje ovisi o broju elemenata i poziciji na kojoj se element dodaje ili brise
def fillDictionary (filename, dictionary, length):
      #Pridodajem svakom kljucu praznu listu
      dictionary = {k:[] for k in range (1, length + 1)};
      flag = False;
      for line in filename:
           #print line
           if (line == "#trajectories\n") and (flag == False):
              flag = True;
              continue;
           if (flag == False):
              continue;
           #print line;
           lista = line.split(";");
           brojFramea = (int) (lista[0]);
           idIgraca = (int) (lista[1]);
           minRow = (int) (lista[2]);
           maxRow = (int) (lista[3]);
           # Posto video koji koristimo u programu resizeamo za 0.5 puta horizontalno, preuredujemo i ova 2 podatka
           minCol = (int) (lista[4]) // 2; 
           maxCol = (int) (lista[5]) // 2;
           #centarRow = (minRow + maxRow) / 2;
           #centarCol = (minCol + maxCol) / 2;
           #height = (maxRow - minRow);
           #width = (maxCol - minCol);
           newRectangle = myRectangle (idIgraca, minRow, maxRow, minCol, maxCol);
           dictionary[brojFramea].append(newRectangle);
      return dictionary;

def proxima (rect1, dictionary,  frameIndex):
        minimum = float("inf");
        print frameIndex;
        for rect2 in dictionary[frameIndex]:
                print rect2, "rect2"
                udaljenost = math.sqrt(pow(rect1.getCenterRow() - rect2.getCenterRow(), 2) + pow(rect1.getCenterCol() - rect2.getCenterCol(), 2));
                if (udaljenost < minimum):
                        minimum = udaljenost;
                        najblizi = rect2;
        return najblizi;
"""
        Presjek dva pravokutnika necemo racunati po presjeku povrsina dva pravokutnika vec po udaljenosti dvije
        centralne tocke dva pravokutnika
"""
def udaljenost (rect1, rect2):
        udaljenost = math.sqrt(pow(rect1.getCenterRow() - rect2.getCenterRow(), 2) + pow(rect1.getCenterCol() - rect2.getCenterCol(), 2));
        return udaljenost;
        
