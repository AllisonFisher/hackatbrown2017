import os
import analyzerDanny as analyzer 
import pickle
from enum import Enum
import json

# faceIds is a list of faceIds (returned from faceFind)


# Pythonic enum?
class RaceGroup(Enum):
    american_indian_alaskan_native = 0
    asian = 1
    black_african_american = 2
    native_hawaiian_other_pacific_islander = 3
    white = 4
    hispanic_latino = 5

def initDemographicFaceGroup():
    print("called init")
    data_dir = '../demographic_faces/'
    flag_path = os.path.join(data_dir, 'flag.txt')
    with open(flag_path, 'r') as file:
        f = file.readline()
    # we've already populated the demographics, read it from the pickle file
    if len(f) > 4:
        print("Loading previously initialized mapping...")
        with open('demographic_mapping_color.pickle', 'rb') as handle:
            mapping = pickle.load(handle)
    else:
        print("Making mapping from scratch...")
        mapping = {
            RaceGroup.american_indian_alaskan_native: [],
            RaceGroup.asian: [],
            RaceGroup.black_african_american: [],
            RaceGroup.native_hawaiian_other_pacific_islander: [],
            RaceGroup.white: [],
            RaceGroup.hispanic_latino: []
        }

        dirs = {
            'american-indian-alaskan-native': RaceGroup.american_indian_alaskan_native, 
            'asian': RaceGroup.asian, 
            'black-african-american': RaceGroup.black_african_american,
            'native-hawaiian-other-pacific-islander': RaceGroup.native_hawaiian_other_pacific_islander, 
            'white': RaceGroup.white,
            'hispanic-latino': RaceGroup.hispanic_latino
        }

        for dirname in dirs:
            for file in os.listdir(os.path.join(data_dir, dirname)):
                full_path = os.path.join(data_dir,dirname,file)
                if os.path.isfile(full_path):
                    face_detect_data = analyzer.face_detect_raw(full_path, 'true', 'false', '')
                    detect_json = json.loads(face_detect_data)
                    for face in detect_json:
                        faceId = face['faceId']
                        key = dirs[dirname]
                        mapping[key].append(faceId)
        
        with open('demographic_mapping_color.pickle', 'wb') as handle:
            pickle.dump(mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(flag_path, 'w') as file:
            file.write('FLAG!\n')
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
    data = analyzer.face_find_similar(faceId, demographicFaceList)
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

def main():
    demographicMapping = initDemographicFaceGroup()
    print (demographicMapping)
    print ("Hi!")

if __name__ == '__main__':
    main()