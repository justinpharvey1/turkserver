from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import sqlite3

import MySQLdb




app = Flask(__name__)


counter = 0




# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)






@app.teardown_appcontext
def close_db(error):
    db.close()




@app.route('/vote', methods=["POST"])
def submit_vote():

    db2 = MySQLdb.connect(host="turkdbs.cea2xgnpufud.us-east-1.rds.amazonaws.com", user="turkusername", passwd="turkpassword", db="turkdb")

    global counter 
    render_template('index.html', vote=request.form['vote'])

    increment = 0

    if (request.form['vote'] == "no"):
        pass

    if (request.form['vote'] == "yes"):
        increment =1

    
    query = 'update votes set votes = votes + 1, score = score + %d where imageID="%s" and selfieID=%s ' %(increment, request.form["imageID"], request.form["selfieID"])
    cursor2 = db2.cursor()
    cursor2.execute(query)
    db.commit()
    cursor2.close()
    db2.close()

    counter = counter + 1

    if (counter < 10): 
	   return redirect(url_for('show_entries'))

    else: 
        return ("All done. Thank you!")






@app.route('/')
def show_entries():
  
    db1 = MySQLdb.connect(host="turkdbs.cea2xgnpufud.us-east-1.rds.amazonaws.com", user="turkusername", passwd="turkpassword", db="turkdb")
    cursor1 = db1.cursor()
    cursor1.execute('select  image.imageID as imageID, votes.selfieID as selfieID, image.imageURL as imageURL, selfie.imageURL as selfieURL from votes join images image on image.imageID = votes.imageID and image.imageType = "image" join images selfie on selfie.imageID = votes.selfieID and selfie.imageType = "selfie" order by votes.votes limit 1')
    cursor1.close()
    db1.close()


    for  imageID, selfieID, imageURL, selfieURL in cursor1: 

        return render_template('index.html', comparisonImage=imageURL, selfieImage=selfieURL, imageID=imageID, selfieID=selfieID )

    cursor.close()

    #return("hello world")



    return "hello world"



if __name__ == '__main__':
    app.run()
