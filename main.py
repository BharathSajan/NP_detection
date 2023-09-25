import cv2
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
cascade = cv2.CascadeClassifier("resources/haarcascade_russian_plate_number.xml")


def extract_num(img_name):
    minArea = 500
    global read
    img = cv2.imread(img_name)#read image into img variable
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#converts the image into grayscale
    nplate = cascade.detectMultiScale(gray, 1.1, 4)#detects all number plate instances in the image

    for (x,y,w,h) in nplate:
        a, b = (int(0.02 * img.shape[0]), int(0.0025 * img.shape[1]))
        plate = img[y+a:y+h-a, x+b:x+w-b] #we crop the numberplate
        area = w * h
        if area >minArea:
        #image processing
            kernel = np.ones((1,1), np.uint8)
            plate = cv2.dilate(plate, kernel, iterations=1)
            plate = cv2.erode(plate, kernel, iterations=1) #make the image brighter
            plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
            # plate_gauss = cv2.GaussianBlur(plate_gray, (5, 5), 0)
            # (thresh, plate) = cv2.threshold(plate_gauss, 127, 255, cv2.THRESH_BINARY)
            (thresh, plate) = cv2.threshold(plate_gray, 127, 255, cv2.THRESH_BINARY)

        #reading the number from the number plate image
        # read = pytesseract.image_to_string(plate, lang='eng',
        #                                    config='--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            read = pytesseract.image_to_string(plate)
            read = ''.join(e for e in read if e.isalnum())#remove the blank space between characters on the number plate
            print(plate.shape[0], plate.shape[1])
            if read =="":
                print("Nothing")
                continue
            print(read)
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            cv2.rectangle(img, (x,y - 40 ), (x+w, y), (255,0,0), -1)
            cv2.putText(img, read, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)
            cv2.imshow('Plate', plate)# shows image on image processed numberplate only
    # img = cv2.resize(img, (int(img.shape[0] * 0.8), int(img.shape[1] * 0.8)))
    cv2.imshow("Result",img)
    cv2.imwrite('resources/Scanned/result.jpg',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

extract_num("resources/toyota.png")



