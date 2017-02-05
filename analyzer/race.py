import os
import analyzer 
import pickle
import uuid
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
    for key in demographic_mapping:
        arr = demographic_mapping[key]
        if faceId in arr:
            #print (key)
            return key
    return None

#assumes demographicFaceList has B/W photos
def guessRace(faceId, demographicFaceMapping):
    groupToIdx = {
        RaceGroup.american_indian_alaskan_native: 0,
        RaceGroup.asian: 1,
        RaceGroup.black_african_american: 2,
        RaceGroup.native_hawaiian_other_pacific_islander: 3,
        RaceGroup.white: 4,
        RaceGroup.hispanic_latino: 5
    }
    flatten = lambda l: [item for sublist in l for item in sublist]
    demographicFaceList = flatten(list(demographicFaceMapping.values()))
    data = analyzer.face_find_similar(faceId, demographicFaceList)
    results = json.loads(data)
    matchingFaceIds = [0 for i in range(6)]
    count = 0
    for match in results:
        matchId = match['faceId']
        raceGroup = getRaceGroup(matchId, demographicFaceMapping)
        assert(raceGroup != None)
        matchingFaceIds[groupToIdx[raceGroup]] += match['confidence']
    #print(matchingFaceIds)
    mostLikelyRace = matchingFaceIds.index(max(matchingFaceIds))
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


# SO LIT SO HYPE
def analyze(num_frames, folder_path):
    group_id = group_id = str(uuid.uuid4())
    demographicFaceGroup = initDemographicFaceGroup()
    raceCount = {
            RaceGroup.american_indian_alaskan_native: 0,
            RaceGroup.asian: 0,
            RaceGroup.black_african_american: 0,
            RaceGroup.native_hawaiian_other_pacific_islander: 0,
            RaceGroup.white: 0,
            RaceGroup.hispanic_latino: 0
        }

    num_frames = 24

    analyzer.create_group(group_id, "gender group")

    frames_with_people = num_frames

    male_frames = 0
    female_frames = 0

    num_males = 0
    num_females = 0

    ids = []
    genders = []
    metaDatas = []

    first = False

    for x in range(1,num_frames + 1):
        results = analyzer.face_detect("img/v2/%03d.jpg" % x)   
        genders.extend(results[0])
        ids.extend(results[1])
        metaDatas.extend(results[2])
        if len(results[0]) > 0 and first == False:
            first = True
            # On the first pass, create a new person for each
            for i in range(0,len(genders)):
                gender = results[0][i]
                if gender == "male":
                    num_males = num_males + 1
                elif gender == "female":
                    num_females = num_females + 1
                print(analyzer.create_person("person", group_id, metaDatas[i]))           
                pass
            analyzer.train_group(group_id)
            pass
        elif len(results[0]) > 0:
            peopleAdded = analyzer.identify_ids_in_group(results[1], group_id, results[3])

            for person in peopleAdded:
                i = 0
                for faceId in results[1]:
                    raceGuess = guessRace(faceId, demographicFaceGroup)
                    raceCount[raceGuess] += 1
                    if faceId == results[1][i]:
                        gender = results[0][i]
                        if gender == "male":
                            num_males = num_males + 1
                        elif gender == "female":
                            num_females = num_females + 1
                    i = i + 1
                         

        pass

    print("This many people: %s. %s males, %s females." % (faceId, num_males, num_females))
    print("Race data: ")
    print(raceCount)

    i = 0
    for gender in genders:  
        if gender == "male":
            male_frames = male_frames + 1
        elif gender == "female":
            female_frames = female_frames + 1
        else:
            frames_with_people = frames_with_people - 1
        i = i + 1
        pass

    avg_male = male_frames / frames_with_people
    avg_female = female_frames / frames_with_people

    print("Average per frame - m: %s, f: %s" % (avg_male, avg_female))
    print(list(set(ids)))
    return 0

def main():
    analyze(24, "img/v2")
    return 0

if __name__ == "__main__":
    main()

"""
def main():
    demographicMapping = initDemographicFaceGroup()
    #print (demographicMapping)
    data = analyzer.face_detect_raw("img/003.jpg")
    jsonObj = json.loads(data)
    guesses = []
    for face in jsonObj:
        guess = (guessRace(face['faceId'], demographicMapping))
        guesses.append(guess)
    print (guesses)



if __name__ == '__main__':
    main()"""