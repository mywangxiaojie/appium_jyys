import easyocr

if __name__ == "__main__":

    reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
    print(reader.readtext('..\\case\\tmp\\ifadoebnmvul.jpg'))
    print(reader.readtext('..\\case\\tmp\\ypjozmiwebft.jpg'))