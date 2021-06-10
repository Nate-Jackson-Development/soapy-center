from bs4 import BeautifulSoup
import requests
import json
import re

def main(username, password):
    session = requests.Session()
    # Handles Cookies for logging in and persistance

    url = "https://homeaccess.beth.k12.pa.us/HomeAccess/Account/LogOn/index.html"
    # URL for going to the site

    r = session.get(url)
    # setting the website url to 'r'

    soup = BeautifulSoup(r.text, features="lxml")
    # extracting the raw website data into 'soup'

    VerificationToken = soup.find("input", {"name":"__RequestVerificationToken"}).get("value")
    # Retarted Verification Token added for no good reason

    payload = {
        "__RequestVerificationToken" : VerificationToken,
        "ReturnUrl" : "/HomeAccess/Classes/Classwork",
        "SCKTY00328510CustomEnabled" : False,
        "Database" : 10,
        "LogOnDetails.UserName" : username,
        "LogOnDetails.Password" : password
            }
    # Payload Information to send for login

    GradeLogin = session.post(url = "https://homeaccess.beth.k12.pa.us/HomeAccess/Account/LogOn/index.html?ReturnUrl=%2fhomeaccess", data = payload)
    # Sending to Payload to the website for login

    soup = BeautifulSoup(GradeLogin.text, features="lxml")
    # Parsing the response from the payload

    assignments = soup.find("iframe")
    # Finding the Location of the Grades

    link_get_source = "https://homeaccess.beth.k12.pa.us" + assignments.get("src")
    # Generates Link for the Extraction

    GradesLocation = session.post(url = link_get_source, data = payload)
    # grabs grades location

    soup = BeautifulSoup(GradesLocation.text, features="lxml")
    # Applies grades code to the variable 'soup' 

    # Start extraction --

    classes = soup.find_all("a", {"class":"sg-header-heading"})
    #classes = soup.select("a.sg-header-heading")
    # Finds Classes Names
    
    averages = soup.find_all("span", {"class":"sg-header-heading sg-right"})
    #averages = soup.select("span.sg-header-heading.sg-right")
    # Finds Grades for the class

    mainList = list()
    # initialize the array for the mixed classname/grades

    for i, j in zip(classes, averages):
        temp = i.text.strip() + ":" + j.text
        mainList.append(temp)

    #subList = []
    # Initializes the array for the individual assignments

    #print(classes, averages)

    testAssignment = soup.select("div.AssignmentClass > div.sg-content-grid")

    temp = list()
    tempA = list()
    tempB = list()
    tempC = str()
    assignmentList = list()
    TestList = list()
    amountOfAssignments = list()
    assignmentGradesPoints = list()
    assignmentGradesFixed = list()
    assigGradeCombine = list()
    evenSoupier = list()
    assignmentDesc = list()
    i = 0
    it = 0

    for c in testAssignment: # 5 times
        soupy = BeautifulSoup(str(c), features="lxml") # Parse table

        assignmentNames = soupy.select("table.sg-asp-table > tr.sg-asp-table-data-row > td > a ") # get assignment names
        
        assignmentGrades = soupy.select("table.sg-asp-table > tr.sg-asp-table-data-row > td.sg-view-quick")

        assignmentCheckExcusal = soupy.select("table.sg-asp-table > tr.sg-asp-table-data-row > td")

        

        #soup = BeautifulSoup(str(assignmentGrades), features="lxml")

        #assignmentGrades = soup.prettify(formatter=lambda s: s.replace(u'\xa0', 'None'))

        regex = re.compile(r"(>.{1,9}%<)")
        i = 0
        
        for a in assignmentNames:
            tempA.append(a['title'])
        
        for a in assignmentCheckExcusal:
            i += 1

            if i == 5: # Get Points pt. 1
                if a.text == "\xa0":
                    tempC = ("None" + "/")
                elif a.text == "\n":
                    tempC = ("None" + "/")
                else:
                    tempC = (a.text.strip() + "/")

            if i == 6: # Get Points pt. 2
                tempB.append(str(tempC + a.text.strip())) # Combine Points

            if i == 10 : # Get Percentage grade
                i = 0
                if a.text == "\xa0":
                    temp.append("None")
                elif "E" in tempC:
                    temp.append("Excused")
                else:
                    temp.append(a.text.strip())
        
        assignmentGradesPoints.append(tempB)
        assignmentDesc.append(tempA)
        assignmentGradesFixed.append(temp)
        amountOfAssignments.append(len(assignmentNames)) # get amount of assignments

        temp = list()
        tempB = list()
        tempC = str()

        for assigname in assignmentNames:
            sTemp = assigname.text.strip() # strip assignments of garbage
            temp.append(sTemp) # append to a temporary list

        assignmentList.append(temp) # append temporary list to list of assignments
        temp = list() # reset temporary list

        for a, b in zip(assignmentList[it], assignmentGradesFixed[it]):
            temp.append(a + "^" + b)

        
        assigGradeCombine.append(temp)
        it += 1
        temp = list()


        

    temp = None



    return mainList, assigGradeCombine, amountOfAssignments, assignmentDesc, assignmentGradesPoints

def attendanceFunc(username: str, password: str):
    """
    ## Scrapes the Attendance information from homeaccess center
    Returns iframeLink, cookiejar, iframeData

    iframeLink is the absolute link to the iframe

    cookiejar is the requests cookiejar for the iframe

    iframeData is the HTML source of the iframe
    """

    session = requests.Session()
    # Handles Cookies for logging in and persistance

    url = "https://homeaccess.beth.k12.pa.us/HomeAccess/Account/LogOn/index.html"
    # URL for going to the site

    r = session.get(url)
    # setting the website url to 'r'

    soup = BeautifulSoup(r.text, features="lxml")
    # extracting the raw website data into 'soup'

    VerificationToken = soup.find("input", {"name":"__RequestVerificationToken"}).get("value")
    # Retarted Verification Token added for no good reason

    payload = {
        "__RequestVerificationToken" : VerificationToken,
        "SCKTY00328510CustomEnabled" : False,
        "Database" : 10,
        "LogOnDetails.UserName" : username,
        "LogOnDetails.Password" : password
            }
    # Payload Information to send for login

    GradeLogin = session.post(url = "https://homeaccess.beth.k12.pa.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2fAttendance%2fMonthView", data = payload)

    soup = BeautifulSoup(GradeLogin.text, features="lxml")
    # Parsing the response from the payload

    attendanceFrame = soup.find("iframe")
    # Finding the Location of the Grades

    iframeLink = "https://homeaccess.beth.k12.pa.us" + attendanceFrame.get("src")
    # Generates Link for the Extraction

    iframeData = session.post(iframeLink).text

    cookiejar = session.cookies

    return (iframeLink, cookiejar, iframeData)

if __name__ == "__main__":
    a, b, c, d, e = main("mooren", "Basd1010749")
    print(b)