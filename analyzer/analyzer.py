
########### Python 2.7 #############
import httplib, urllib, base64

def faceDetect(path):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'ad68d0b1e1f2455e9410495d5b1c9d2f',
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender',
    })

    body = "{ 'url' : 'http://weknowyourdreams.com/images/people/people-06.jpg' }"

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return data


def main()
    print "main()"
    return 0

if __name__ == "main":
    main()
