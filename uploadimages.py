import mysql.connector


urlfile = open("SG_filenames_array.txt")


lines = urlfile.readlines()

endpoint = "https://s3.amazonaws.com/byl-originals/"
cnx = mysql.connector.connect(user='turkusername', password='turkpassword', host='turkdbs.cea2xgnpufud.us-east-1.rds.amazonaws.com', database='turkdb')
 	
imageID = 0

for line in lines:

	imageID += 1
	parts = line.split("\"")

	params = parts[1]

	url = endpoint + params

	print url
	cursor = cnx.cursor()
	query = ("INSERT INTO images (imageID, imageURL, imageType) VALUES ("  + str(imageID) + ",'" + url + "','" +  "image" + "');")
	cursor.execute(query)

	cnx.commit()
	cursor.close()