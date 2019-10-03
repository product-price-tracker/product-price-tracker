def getAccessKey():
    with open('../secureKey.txt', 'r') as f:
        return f.read()
