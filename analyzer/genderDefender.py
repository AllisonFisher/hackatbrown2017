from __future__ import division
import analyzer

def main():
	group_id = "id15"

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
				for personId in results[1]:
					if personId == results[1][i]:
						gender = results[0][i]
						if gender == "male":
							num_males = num_males + 1
						elif gender == "female":
							num_females = num_females + 1
					i = i + 1
						 

		pass

	print("This many people: %s. %s males, %s females." % (personId, num_males, num_females))

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

if __name__ == "__main__":
    main()
