
########### Python 2.7 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, binascii

subKey = 'ad68d0b1e1f2455e9410495d5b1c9d2f'

def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()

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

    print(jObj)
    personId = jObj["personId"]

    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subKey,
    }

    conn.close()

    add_face(group_id, personId, meta_data)

    
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

    body = load_binary('img/002.jpg')

    urlStr = '/face/v1.0/persongroups/%s/persons/%s/persistedFaces?%s' % (group_id, personId, params)

    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", urlStr, body, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')

    print(data)
    conn.close()


def create_group(group_id, group_name):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subKey,
    }

    body = '{"name" : "%s"}' % group_name

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("PUT", "/face/v1.0/persongroups/%s" % group_id, body, headers)
        response = conn.getresponse()
        data = response.read()
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
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/verify", body, headers)
        response = conn.getresponse()
        data = response.read()
        jObj = json.loads(data)
        
        # print jObj

        conn.close()
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
    print(data)
    jObj = json.loads(data)
    genders = []
    ids = []
    metaData = []


    for face in jObj:
        genders.append(face['faceAttributes']['gender'])
        ids.append(face['faceId'])
        fr = face['faceRectangle']
        rectString = "%s,%s,%s,%s" % (fr['left'],fr['top'],fr['width'],fr['height'])
        metaData.append({"img" : path, "targetFace" : rectString})

    conn.close()
    return (genders,ids,metaData)
    
