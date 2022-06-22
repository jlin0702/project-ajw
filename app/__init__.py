import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

'''
    dynamic navigation bar
    url: the url for the link, list
    label: what to call the link, list
'''
class nav:
    def __init__(self, url, label):
        self.url = url
        self.label = label

profile_nav = nav(
    ["", "work_edu", "hobbies"],
    ["About Me", "Work Experience/Education", "Hobbies"]
)

@app.route('/')
def index():
    return render_template('index.html', nav=profile_nav, title="Jacky", url=os.getenv("URL"))

# for jacky page
@app.route('/jacky')
def jacky():
    return render_template('jacky.html', nav=profile_nav, title="About Me", url=os.getenv("URL"))

# for work experience/education page
@app.route('/work_edu')
def work_edu():
    job = ["Wendy's"]
    # value: 2d list with inner generating new lines
    job_description = [["October 2019 - March 2020"]],
    education = ["University of Kansas", "Northwest High School"]
    # value: 2d list with inner generating new lines
    edu_description = [["B.S. Computer Science","Aug 2020 - May 2024"], ["High School", "Aug 2016 - May 2020"]]
    return render_template("work_edu.html", nav=profile_nav, job=job, job_description=job_description, education=education, 
            edu_description=edu_description, title="Work/Education", url=os.getenv("URL"))

# for work experience/education page
@app.route('/hobbies')
def hobbies():
    hobbies = ["Gaming, Driving, Deep discussions"]
    photo = "jacky_hobby.jpg"
    return render_template("hobbies.html", nav=profile_nav, hobbies=hobbies, title="Hobbies", photo=photo, url=os.getenv("URL"))


# for map page
@app.route('/map')
def map():
    return render_template('map.html', nav=profile_nav, title="Map", url=os.getenv("URL"))

if __name__ == "__main__":
    app.run(debug=True)