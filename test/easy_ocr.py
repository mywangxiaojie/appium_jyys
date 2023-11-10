import easyocr
import cv2

if __name__ == "__main__":

    reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
    print(reader.readtext('..\\case\\tmp\\ifadoebnmvul.jpg'))
    print(reader.readtext('..\\case\\tmp\\ypjozmiwebft.jpg'))


    img=cv2.imread('..\\case\\tmp\\ifadoebnmvul.jpg')
    print(reader.readtext(img))


