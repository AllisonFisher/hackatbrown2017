
import http.client
import urllib.request, urllib.parse, urllib.error 
import base64
import json

import race

def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()

def face_detect(path, returnFaceId='true', returnFaceLandmarks='false', 
    returnFaceAttributes='age,gender'):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': 'ad68d0b1e1f2455e9410495d5b1c9d2f',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': returnFaceId,
        'returnFaceLandmarks': returnFaceLandmarks,
        'returnFaceAttributes': returnFaceAttributes,
    })

    body = load_binary(path)

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print(("[Errno {0}] {1}".format(e.errno, e.strerror)))





def main():
    data = face_detect("003.jpg")

    #demographicFaceGroup = initDemographicFaceGroup()
    jObj = json.load(data)
    faceIds = []
    for face in jObj:
        faceIds.append(face['faceId'])

    print (faceIds)
    return
    

    # grObj = json.loads(groups)



    return 0

if __name__ == "__main__":
    main()

