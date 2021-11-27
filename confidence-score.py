import csv, math
import statistics as st

# get data from google_poi file
google_poi = dict()
with open('google_poi.csv') as csvfile:
	reader = csv.reader(csvfile)
	for index, row in enumerate(reader):
		data = row[0].split(';')
		internal_id = data[0]

		google_poi[internal_id] = data[1:4]

# get data from osm_poi file
osm_poi = dict()
with open('osm_poi.csv') as csvfile:
	reader = csv.reader(csvfile)
	for index, row in enumerate(reader):
		try:
			data = row[0].split(';')
			internal_id = data[1]

			osm_poi[internal_id] = data[2:5]
		except:
			continue

# get data from google_osm_poi_matching file
matching = []
with open('google_osm_poi_matching.csv') as csvfile:
	reader = csv.reader(csvfile)
	for index, row in enumerate(reader):
		if index == 0:
			header = row[0].split(';')
			header.append('confidence score')
			continue
		try:
			data = row[0].split(';')
			matching.append(data)
		except:
			continue

differences_list = []
for match in matching:
	# match the two entries
	google = google_poi[match[2]]
	osm = osm_poi[match[1]]

	# calculate distance between them using the coordinates
	diff = math.sqrt((float(google[1])-float(osm[1]))**2 + (float(google[2])-float(osm[2]))**2) # pythagorean theorem
	differences_list.append(diff)

median = st.median(differences_list)
mad = st.median( [abs(diff - median) for diff in differences_list] ) # median absolute deviation
updated_difflist = [diff for diff in differences_list if diff / mad < 20] # if value over 20 times the mad, it is an outlier
mean = st.mean(updated_difflist)

def find_confidence(match):
	google = google_poi[match[2]]
	osm = osm_poi[match[1]]

	diff = math.sqrt((float(google[1])-float(osm[1]))**2 + (float(google[2])-float(osm[2]))**2)

	val = 1 - (diff / mean / 40)
	val = val if val > 0 else 0 # return 0 if less than 0
	val = val if val <= 1 else 1 # return 1 if greater than 1
	return val


if __name__ == "__main__":

	for match in matching:
		confidence_score = round(find_confidence(match), 4)
		match.append(confidence_score)

	with open('updated_matching.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		matching.insert(0, header) # add header
		writer.writerows(matching)











