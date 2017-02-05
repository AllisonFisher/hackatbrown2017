from __future__ import division
import analyzer

def main():
	num_frames = 66

	frames_with_people = num_frames

	male_frames = 0
	female_frames = 0

	ids = []
	genders = []
	metaDatas = []

	for x in xrange(1,num_frames + 1):
		results = analyzer.face_detect("img/ot/%03d.jpg" % x)	
		genders.extend(results[0])
		ids.extend(results[1])
		metaDatas.extend(results[2])
		pass

	for gender in genders:	
		if gender == "male":
			male_frames = male_frames + 1
		elif gender == "female":
			female_frames = female_frames + 1
		else:
			frames_with_people = frames_with_people - 1
		pass

	for x in xrange(0,len(ids) - 1):
		analyzer.compare_ids(ids[x], ids[x+1])
		pass

	avg_male = int(round(male_frames / frames_with_people))
	avg_female = int(round(female_frames / frames_with_people))

	print "m: %s, f: %s" % (avg_male, avg_female)
	print list(set(ids))
	return 0

if __name__ == "__main__":
    main()
