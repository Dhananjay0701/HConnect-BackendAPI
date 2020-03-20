from flask import Flask
from flask import jsonify
import os
from google.cloud import firestore

app = Flask(__name__)

############################################################ Helper

def bit_not(n, numbits=8):
    return (1 << numbits) - 1 - n

############################################################ HOME

@app.route("/")
def home():
    return "Hello, Welcome to AutoStart API."

#############################################################  READ

@app.route("/<CID>/read/<prop>")
def readPropData(CID, prop):
    with open(f'data/{CID}/{prop}.txt', 'r') as file:
        propData = file.read()
    return propData
    
@app.route("/<CID>/read/RelayStatus/JSON")
def readPropDataJSON(CID):
    with open(f'data/{CID}/RelayStatus.txt', 'r') as file:
        propData = file.read()

    propData = int(propData)
    jsonDict = {}
    for i in range(1, 9):
        jsonDict[f'pid{i}'] = propData % 10
        propData = propData // 10
    
    return jsonify({'States' : jsonDict})
    
@app.route("/<EID>/JSON")
def readPropDataAllJSON(EID):
    db = firestore.Client.from_service_account_json('firebaseConfig.json')
    users_ref = db.collection(u'room')
    docs = users_ref.get()

    chipList = []

    for doc in docs:
        docDict = doc.to_dict()
        if docDict['user-email'] == EID:
            chipList.append(docDict['chipId'])

    jsonDict = {}
    for chip in chipList:
        with open(f'data/{chip}/RelayStatus.txt', 'r') as file:
            propData = file.read()

        propData = int(propData)
        tempDict = {}
        for i in range(1, 9):
            tempDict[f'pid{i}'] = propData % 10
            propData = propData // 10

        jsonDict[chip] = tempDict
    
    return jsonify({EID : jsonDict})

#############################################################  WRITE

@app.route("/<CID>/write/<prop>/<payload>")
def writePropData(CID, prop, payload):
    try:
        os.mkdir(f'data/{CID}')
    except FileExistsError:
        pass

    if(prop == 'RelayStatus'):
        payload = int(payload)
        PID = (payload % 10) - 1
        payload = int(payload / 10)
        PIDStat = payload % 10

        with open(f'data/{CID}/{prop}.txt', 'r') as file:
            orig = file.read()
        pass

        orig = int(orig, 2)

        if (PIDStat == 1):
            data = orig | (1 << PID)
        elif (PIDStat == 0):
            data = orig & bit_not(1 << PID)

        with open(f'data/{CID}/{prop}.txt', 'w') as file:
            file.write('{0:08b}'.format(data))
    else:
        with open(f'data/{CID}/{prop}.txt', 'w') as file:
            file.write(payload)
    
    return 'Done'
    
#############################################################  All ON/OFF

@app.route("/<CID>/allOn")
def allOn(CID):
    try:
        os.mkdir(f'data/{CID}')
    except FileExistsError:
        pass

    with open(f'data/{CID}/RelayStatus.txt', 'w') as file:
        file.write('11111111')
    
    return 'All On'

@app.route("/<CID>/allOff")
def allOff(CID):
    try:
        os.mkdir(f'data/{CID}')
    except FileExistsError:
        pass

    with open(f'data/{CID}/RelayStatus.txt', 'w') as file:
        file.write('00000000')
    
    return 'All Off'

#############################################################  CREATE

@app.route("/<CID>/create")
def create(CID):
    if os.path.exists(f'data/{CID}'):
        return f'{CID} already exists'
    else:
        os.mkdir(f'data/{CID}')
        with open(f'data/{CID}/RelayStatus.txt', 'w') as file:
            file.write('00000000')
            
        # with open(f'data/{CID}/RemoteStatus.txt', 'w') as file:
        #     file.write('0')
            
        # with open(f'data/{CID}/ACTemp.txt', 'w') as file:
        #     file.write('16')
            
        # with open(f'data/{CID}/ACStatus.txt', 'w') as file:
        #     file.write('0')
    
    return 'Created ' + CID


if __name__ == "__main__":
    app.run(debug=True)
