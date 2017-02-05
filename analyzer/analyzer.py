import http.client, urllib.request, urllib.parse, urllib.error, base64, json, binascii, ssl
subKey = 'ad68d0b1e1f2455e9410495d5b1c9d2f'

#THIS IS VERY BAD. TODO: FIX ASAP
ssl._create_default_https_context = ssl._create_unverified_context


def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()

def identify_ids_in_group(face_ids, group_id, meta_datas):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subKey,
    }

    body = json.dumps({"personGroupId" : group_id, "faceIds" : face_ids})

    peopleAdded = []

    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/identify", body, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    jObj = json.loads(data)
    #print(jObj)
    for face in jObj:
        if(len(face["candidates"]) > 0):
            personToAdd = face["candidates"][0]["personId"]
            add_face(group_id, personToAdd, meta_datas[face["faceId"]])
        else:
            create_person("person", group_id, meta_datas[face["faceId"]])
            peopleAdded.append(face["faceId"])

    train_group(group_id) 
    return peopleAdded       
            

def train_group(group_id):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subKey,
    }

    body = ""

    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/%s/train" % group_id, body, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    
    return data == ""


def create_person(person_name, group_id, meta_data):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subKey,
    }

    body = '{"name" : "%s"}' % person_name

    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/%s/persons" % group_id, body, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    jObj = json.loads(data)

    personId = jObj["personId"]
    conn.close()

    add_face(group_id, personId, meta_data)

    return personId

    
def add_face(group_id, personId, meta_data):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subKey,
    }

    params = urllib.parse.urlencode({
    # Request parameters
    'targetFace': meta_data["targetFace"],
    })

    body = meta_data["img"]

    urlStr = '/face/v1.0/persongroups/%s/persons/%s/persistedFaces?%s' % (group_id, personId, params)

    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", urlStr, body, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')

    #print(data)
    conn.close()


def create_group(group_id, group_name):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subKey,
    }

    body = '{"name" : "%s"}' % group_name

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("PUT", "/face/v1.0/persongroups/%s" % group_id, body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        conn.close()

        return data == ""
        
    except Exception as e:
        print(("[Errno {0}] {1}".format(e.errno, e.strerror)))


def compare_ids(id1, id2):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subKey,
    }

    body = '{"faceId1" : "%s", "faceId2" : "%s"}' % (id1, id2)

    # print body

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/verify", body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        jObj = json.loads(data)
        conn.close()
        return data == ""   
    except Exception as e:
        print(("[Errno {0}] {1}".format(e.errno, e.strerror)))

def face_find_similar(faceId, demographicFaceList):

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subKey,
    }

    params = urllib.parse.urlencode({
    })

    body = json.dumps({
        "faceId": faceId,
        'faceIds': demographicFaceList,
        'maxNumOfCandidatesReturned': 10,
        'mode': 'matchFace'
        })

    #print(body)

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/findsimilars?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
        return data
    except Exception as e:
        print(("[Errno {0}] {1}".format(e.errno, e.strerror)))

def face_detect(path):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subKey,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender',
    })

    body = load_binary(path)

    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    #print(data)
    jObj = json.loads(data)
    genders = []
    ids = []
    metaData = []
    metaDict = {}

    for face in jObj:
        genders.append(face['faceAttributes']['gender'])
        ids.append(face['faceId'])
        fr = face['faceRectangle']
        rectString = "%s,%s,%s,%s" % (fr['left'],fr['top'],fr['width'],fr['height'])
        metaData.append({"img" : body, "targetFace" : rectString})
        metaDict[face['faceId']] = {"img" : body, "targetFace" : rectString}

    conn.close()
    return (genders,ids,metaData,metaDict)

def face_detect_raw(path, retFaceId='true', retFaceLandmarks='true', retFaceAttributes='age,gender'):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subKey,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': retFaceId,
        'returnFaceLandmarks': retFaceLandmarks,
        'returnFaceAttributes': retFaceAttributes,
    })

    body = load_binary(path)
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        conn.close()
        return data
    except Exception as e:
        print(("[Errno {0}] {1}".format(e.errno, e.strerror)))
    