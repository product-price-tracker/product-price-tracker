import os

def getAccessKey():
    if (os.path.isfile('../secureKey.txt')):
        with open('../secureKey.txt', 'r') as f:
            return f.read()
    elif (os.path.isfile('secureKey.txt')):
        with open('secureKey.txt', 'r') as f:
            return f.read()
