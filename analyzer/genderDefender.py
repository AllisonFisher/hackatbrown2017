from __future__ import division
import analyzer

def main():
	group_id = "id3"

	num_frames = 66

	analyzer.create_group(group_id, "gender group")

	frames_with_people = num_frames

	male_frames = 0
	female_frames = 0

	ids = []
	genders = []
	metaDatas = []

	personId = 0
	first = False

	for x in range(1,num_frames + 1):
		results = analyzer.face_detect("img/ot/%03d.jpg" % x)	
		genders.extend(results[0])
		ids.extend(results[1])
		metaDatas.extend(results[2])
		if len(genders) > 0 and first == False:
			first = True
                        # On the first pass, create a new person for each
			personId = personId + 1
			for i in range(0,len(genders)):
                                print(analyzer.create_person("person%s" % personId, group_id, metaDatas[i]))           
                                pass
			analyzer.train_group(group_id)
			pass
		else:
			pass
		pass

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

	avg_male = int(round(male_frames / frames_with_people))
	avg_female = int(round(female_frames / frames_with_people))

	print("m: %s, f: %s" % (avg_male, avg_female))
	print(list(set(ids)))
	return 0

if __name__ == "__main__":
    main()
