import flask
from flask import request, render_template, redirect, url_for, session
from flask_session import Session
from datetime import timedelta
import json
from Scraper import main, attendanceFunc
from flask_cors import CORS
from waitress import serve
from string_utils import split_str, split_str_carrot, split_str_plus

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
    attendaceLink, attendaceCookies, iframeData = attendanceFunc(username, password)

    session['authenticated'] = True
    session['class_avg'] = data # List of classes and grades
    session['individual_assignments'] = data2 # List of assignments + grade concat with '^'
    session['assignment_amount'] = data3 # Amount of assignments
    session['assignmentDescription'] = data4 # Assignment Descriptions
    session['assignmentPoints'] = data5 # Points per assignment
    session['ATTENDANCE_COOKIES'] = attendaceLink # Sets the attendance iframe URL
    session['ATTENDANCE_FRAME_LINK'] = attendaceCookies # sets the attendance Cookies
    session['IFRAME_SOURCE'] = iframeData # sets the html code for the iframe
    

## IMPORTANT
## main() returns 5 variables that can be assigned to
## class + average, individual assignments, number of assignments per class

# Authentication
@app.route('/auth/v1/', methods=['GET', 'POST'])
def auth():
    #POST form data
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        session['username'] = username
        session['password'] = password

        #print(username, password)
        try:
            getData(username, password)

            return redirect(url_for('home'))

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

    username = session.get('username')
    password = session.get('password')

    getData(username, password)

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

    for i in session.get('class_avg'):
        _temp_ = split_str(i)
        data.update({_temp_[0]:_temp_[1]})
        
    return render_template("index.html", data = data)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    session['authenticated'] = False
    return redirect(url_for('auth'))


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

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():

    cookiejar = session.get('ATTENDANCE_COOKIES')
    attendanceFrameLink = session.get('ATTENDANCE_FRAME_LINK')
    iframesource = session.get('IFRAME_SOURCE')

    data = {
        "iframeSource" : iframesource
    }

    return render_template("attendance.html", data = data)
    
@app.route('/jankModeActivated')
def jankModeActivated():
    return str(session.get('IFRAME_SOURCE'))

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000, debug=False)
    serve(app, host='::', port=5000, threads=4)
