import flask
import re
from bs4 import BeautifulSoup
from flask import request, render_template, redirect, url_for, session, make_response
from flask.helpers import make_response
from flask_session import Session
from datetime import timedelta
import json
from Scraper import main, attendanceFunc, getSchedule
from flask_cors import CORS
from waitress import serve
from string_utils import split_str, split_str_carrot, split_str_plus
from subprocess import Popen

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
#app.config["SESSION_TYPE"] = 'filesystem'
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def getData(username, password):
    # test if credentials work
    data, data2, data3, data4, data5 = main(username, password)

    
    

    session['authenticated'] = True
    session['class_avg'] = data # List of classes and grades
    session['individual_assignments'] = data2 # List of assignments + grade concat with '^'
    session['assignment_amount'] = data3 # Amount of assignments
    session['assignmentDescription'] = data4 # Assignment Descriptions
    session['assignmentPoints'] = data5 # Points per assignment
    

## IMPORTANT
## main() returns 5 variables that can be assigned to
## class + average, individual assignments, number of assignments per class

# Authentication
@app.route('/auth/v1/', methods=['GET', 'POST'])
def auth():
    cook = make_response(redirect(url_for('home')))

    if request.cookies.get('p') != "" or request.cookies.get('u') != "":
        try:
            session['username'] = request.cookies.get('u')
            session['password'] = request.cookies.get('p')

            session['authenticated'] = True

            return cook
        except Exception as e:
            # if they don't:
            # display the error (err = "1")
            print(e)
            return render_template('auth/v1/auth.html', err = "1")
    
    #POST form data
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        session['username'] = username
        session['password'] = password

        cook.set_cookie('u', username, max_age=60*60*24*365*2)
        cook.set_cookie('p', password, max_age=60*60*24*365*2)

        #print(username, password)
        try:
            getData(username, password)

            return cook

        except Exception as e:
            # if they don't:
            # display the error (err = "1")
            print(e)
            return render_template('auth/v1/auth.html', err = "1")
            
        pass
    
    else:
        # if no POST req:
        # show the form
        return render_template('auth/v1/auth.html', err = "0")

@app.route('/refresh')
def refresh():

    username = request.cookies.get('u')
    password = request.cookies.get('p')

    try:
        getData(username, password)
    except:
        redirect(url_for('auth'))

    return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        if session['authenticated']:
            pass
        else:
            return redirect(url_for("auth"))
    except:
        return redirect(url_for("auth"))


    data = {}

    try:
        for i in session.get('class_avg'):
            _temp_ = split_str(i)
            data.update({_temp_[0]:_temp_[1]})
    except Exception as e:
        print(e)
        redirect(url_for("refresh"))
        
    return render_template("index.html", data = data)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    session['authenticated'] = False
    cook = make_response(redirect(url_for('auth')))
    cook.set_cookie('u', "")
    cook.set_cookie('p', "")
    return cook

@app.route("/changelog")
def changelog():
    return render_template("Changelog.html")

@app.route("/api/v1/schedule")
def schedule():
    username = session.get('username')
    password = session.get('password')
    return json.dumps(getSchedule(username, password))

@app.route('/api/v1/assignmentAmounts')
def assignmentAmounts():
	return str(json.dumps(session.get('assignment_amount')))


@app.route('/api/v1', methods=['GET', 'POST'])
def api_id():
    try:
        if session['authenticated']:
            pass
        else:
            return redirect(url_for("auth"))
    except:
        return redirect(url_for("auth"))
    a = session['class_avg']
    return str(json.dumps(a, indent=2))# + "<br><br>" + str(b)

@app.route('/api/v1/<classnum>/Assignments')
def classAssignments(classnum):
    return str(json.dumps(session.get('individual_assignments')[int(classnum)]))

@app.route('/api/v1/description/<clsnum>')
def assDesc(clsnum):
    return str(json.dumps(session.get('assignmentDescription')[int(clsnum)]))

@app.route('/api/v1/points/<clsnum>')
def assPoints(clsnum):
    return str(json.dumps(session.get('assignmentPoints')[int(clsnum)]))

@app.route("/schedule")
def schedulePage():
    username = session.get('username')
    password = session.get('password')
    data = getSchedule(username, password)
    return render_template("schedule.html", data = data)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():

    username = session.get('username')
    password = session.get('password')

    attendanceFrameLink, cookiejar, iframesource = attendanceFunc(username, password)

    session["IFRAME_SOURCE"] = iframesource

    data = {
        "iframeSource" : iframesource,
        "iframeLink" : attendanceFrameLink
    }

    return make_response(render_template("attendance.html", data = data))
    
@app.route('/jankModeActivated')
def jankModeActivated():
    htmlData = str(session.get('IFRAME_SOURCE'))

    soup = BeautifulSoup(htmlData, features='html.parser')

    aTags = soup.select("a")

    for tag in aTags:
        tag.decompose()

    linkTag = re.compile(r"<link.*>")
    scriptTag = re.compile(r"<script[^>]*>[^<]*</script>")
    aTag = re.compile(r"<a[^>]*>[^>]*<\/a>", flags=re.S | re.M)
    stragglerTag = re.compile(r"<script[^>]*>[^>]*</script>", flags=re.S)

    linkless = re.sub(linkTag, '', str(soup))
    scriptless = re.sub(scriptTag, '', linkless)
    aTagLess = re.sub(aTag, '', scriptless)
    evenScriptLess = re.sub(stragglerTag, '', aTagLess)

    return str(evenScriptLess)

@app.route("/api")
def apiRef():
    return render_template("reference.html")

@app.route("/api/v1/syncAndRestart/<id>")
def sync(id):
    if id == "0749":
        Popen(["/home/nathan/soapy-center/update"])

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000, debug=False)
    serve(app, host='::', port=5000, threads=4)
