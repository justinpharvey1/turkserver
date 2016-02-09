from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import sqlite3




app = Flask(__name__)


DATABASE = '/Users/justinharvey/turkserver/sqlite/turk.db'

counter = 0


# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='/Users/justinharvey/turkserver/sqlite/turk.db',
    DEBUG=True,
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



#def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()




@app.route('/vote', methods=["POST"])
def submit_vote():

    global counter 
    render_template('index.html', vote=request.form['vote'])

    increment = 0

    if (request.form['vote'] == "no"):
        pass

    if (request.form['vote'] == "yes"):
        increment =1

    db = get_db()
    query = 'update votes set votes = votes + 1, score = score + %d where imageID="%s" and selfieID=%s ' %(increment, request.form["imageID"], request.form["selfieID"])
    cur = db.execute(query)
    db.commit()

    counter = counter + 1

    if (counter < 10): 
	   return redirect(url_for('show_entries'))

    else: 
        return ("All done. Thank you!")






@app.route('/')
def show_entries():
    #db = get_db()
    #cur = db.execute('select  image.imageID as imageID, votes.selfieID as selfieID, image.imageURL as imageURL, selfie.imageURL as selfieURL from votes join images image on image.imageID = votes.imageID and image.imageType = "image" join images selfie on selfie.imageID = votes.selfieID and selfie.imageType = "selfie" order by votes.votes limit 1')
    #entries = cur.fetchall()
    #fetch one?^^^


    #for  imageID, selfieID, imageURL, selfieURL in entries: 

    	# return render_template('index.html', comparisonImage=imageURL, selfieImage=selfieURL, imageID=imageID, selfieID=selfieID )



    return("hello world")


    #print(entries)
    #return("hello world")
    #return render_template('show_entries.html', entries=entries)



if __name__ == '__main__':
    app.run()
