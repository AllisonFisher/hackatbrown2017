import os
import pickle
from enum import Enum

# faceIds is a list of faceIds (returned from faceFind)


def face_find_similar(faceId, demographicFaceList):
    import http.client, urllib.request, urllib.parse, urllib.error, base64
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '{subscription key}',
    }

    params = urllib.parse.urlencode({
    })

    body = json.dumps({
        "faceId": faceId,
        "faceIds": demographicFaceList,
        "maxNumOfCandidatesReturned": 20,
        "mode": "matchFace"
        })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/findsimilars?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print(("[Errno {0}] {1}".format(e.errno, e.strerror)))


# Pythonic enum?
class RaceGroup(Enum):
    american_indian_alaskan_native = 0
    asian = 1
    black_african_american = 2
    native_hawaiian_other_pacific_islander = 3
    white = 4
    hispanic_latino = 5

def initDemographicFaceGroup():
    data_dir = '../demographic_faces/'
    flag_path = os.path.join(data_dir, 'flag.txt')
    with open(flag_path, 'r') as file:
        f = file.readline
    # we've already populated the demographics, read it from the pickle file
    if len(f) > 4:
        with open('demographic_mapping.pickle', 'rb') as handle:
            mapping = pickle.load(handle)
    else:
        print((1/0))
        mapping = {
            RaceGroup.american_indian_alaskan_native: [],
            RaceGroup.asian: [],
            RaceGroup.black_african_american: [],
            RaceGroup.native_hawaiian_other_pacific_islander: [],
            RaceGroup.white: [],
            RaceGroup.hispanic_latino: []
        }

        # cry
        for file in os.path.join(data_dir, 'american-indian-alaskan-native'):
            if os.path.isfile(file):
                face_detect_data = face_detect(file, 'true', 'false', '')
                detect_json = json.loads(face_detect_data)
                faceId = detect_json['faceId']
                mapping[RaceGroup.american_indian_alaskan_native].append(faceId)
        for file in os.path.join(data_dir, 'asian'):
            if os.path.isfile(file):
                face_detect_data = face_detect(file, 'true', 'false', '')
                detect_json = json.loads(face_detect_data)
                faceId = detect_json['faceId']
                mapping[RaceGroup.asian].append(faceId)
        for file in os.path.join(data_dir, 'black-african-american'):
            if os.path.isfile(file):
                face_detect_data = face_detect(file, 'true', 'false', '')
                detect_json = json.loads(face_detect_data)
                faceId = detect_json['faceId']
                mapping[RaceGroup.black_african_american].append(faceId)
        for file in os.path.join(data_dir, 'native-hawaiian-other-pacific-islander'):
            if os.path.isfile(file):
                face_detect_data = face_detect(file, 'true', 'false', '')
                detect_json = json.loads(face_detect_data)
                faceId = detect_json['faceId']
                mapping[RaceGroup.native_hawaiian_other_pacific_islander].append(faceId)
        for file in os.path.join(data_dir, 'white'):
            if os.path.isfile(file):
                face_detect_data = face_detect(file, 'true', 'false', '')
                detect_json = json.loads(face_detect_data)
                faceId = detect_json['faceId']
                mapping[RaceGroup.white].append(faceId)
        for file in os.path.join(data_dir, 'hispanic-latino'):
            if os.path.isfile(file):
                face_detect_data = face_detect(file, 'true', 'false', '')
                detect_json = json.loads(face_detect_data)
                faceId = detect_json['faceId']
                mapping[RaceGroup.hispanic_latino].append(faceId)

        with open('demographic_mapping.pickle', 'wb') as handle:
            pickle.dump(mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(flag_path, 'w') as file:
            file.writeline('FLAG!')
    return mapping
            



def getRaceGroup(faceId, demographic_mapping):
    for group, arr in demographic_mapping:
        if faceId in arr:
            return group
    return None

#assumes demographicFaceList has B/W photos
def guessRace(faceId, demographicFaceList):
    # initialize the demographicFaceList
    demographicFaceList = initDemographicFaceList()
    # 
    data = face_find_similar(faceId, demographicFaceList)
    results = json.loads(data)
    matchingFaceIds = [0 for i in range(6)]
    count = 0
    for match in results:
        matchId = match['persistedFaceId']
        raceGroup = getRaceGroup(matchId)
        assert(raceGroup != None)
        matchingFaceIds[raceGroup] += match['confidence']
    mostLikelyRace = results.index(max(results))
    if mostLikelyRace == 0:
        return RaceGroup.american_indian_alaskan_native
    elif mostLikelyRace == 1:
        return RaceGroup.asian
    elif mostLikelyRace == 2:
        return RaceGroup.black_african_american
    elif mostLikelyRace == 3:
        return RaceGroup.native_hawaiian_other_pacific_islander
    elif mostLikelyRace == 4:
        return RaceGroup.white
    else:
        assert(mostLikelyRace == 5)
        return RaceGroup.hispanic_latino
    #