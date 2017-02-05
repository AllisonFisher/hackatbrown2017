
########### Python 2.7 #############
import httplib, urllib, base64, json

def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()

def compare_ids(id1, id2):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'ad68d0b1e1f2455e9410495d5b1c9d2f',
    }

    body = '{"faceId1" : "%s", "faceId2" : "%s"}' % (id1, id2)

    print body

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/verify", body, headers)
        response = conn.getresponse()
        data = response.read()
        jObj = json.loads(data)
        
        print jObj

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def face_detect(path):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': 'ad68d0b1e1f2455e9410495d5b1c9d2f',
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender',
    })

    body = load_binary(path)

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        jObj = json.loads(data)
        genders = []
        ids = []

        for face in jObj:
            genders.append(face['faceAttributes']['gender'])
            ids.append(face['faceId'])

        conn.close()
        return (genders,ids)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
