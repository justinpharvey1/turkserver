import mysql.connector

endpoint = "https://s3.amazonaws.com/byl-originals/"
cnx = mysql.connector.connect(user='turkusername', password='turkpassword', host='turkdbs.cea2xgnpufud.us-east-1.rds.amazonaws.com', database='turkdb')



deletevotes = cnx.cursor()
query = ("DELETE from votes;")
deletevotes.execute(query)
deletevotes.close()




imagecursor = cnx.cursor()
query = ("SELECT * from images;")
imagecursor.execute(query)


imagelist = []
selfielist = []


#Build list of all selfies and images
for (imageID, imageURL, imageType) in imagecursor:

	if (imageType == "selfie"):
		selfielist.append(imageID)

	if (imageType == "image"):
		imagelist.append(imageID)

imagecursor.close()





#update database for unique image-selfie pairs 
for image in imagelist: 

	for selfie in selfielist:

		print (image, selfie)

		votescursor = cnx.cursor(buffered=True)
		votesquery = ("insert into votes (imageID, selfieID, votes, score) values (" + str(image) + "," + str(selfie) + ", 0, 0);")
		votescursor.execute(votesquery)
		cnx.commit()
		votescursor.close()

cnx.close()



		




