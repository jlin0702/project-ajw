import os
import datetime
import re

from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict
import hashlib

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

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
    ["", "work_edu", "hobbies", "timeline", "map"],
    ["About Me", "Work Experience/Education", "Hobbies", "Timeline Posts", "Map"]
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
    job_description = [["October 2019 - March 2020"]]
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

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    get_name = request.form.get('name')
    if get_name == "" or get_name is None:
        return "Invalid name", 400
    else:
        name = request.form['name']

    get_email = request.form.get('email')
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if not re.fullmatch(regex, get_email) or get_email is None:
        return "Invalid email", 400
    else:
        email = request.form['email']

    get_content = request.form.get('content')
    if get_content == "" or get_content is None:
        return "Invalid content", 400
    else:
        content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts' : [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():
    id = request.form['id']
    TimelinePost.delete_by_id(id)
    return "ID " + id + " has been deleted"

@app.route('/timeline')
def timeline():
    posts = get_time_line_post()["timeline_posts"]
    for post in posts:
        gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(post["email"].lower().encode()).hexdigest()
        post["image_src"] = gravatar_url
        post["created_at"] = post["created_at"].strftime("%a, %d %B %Y %H:%M:%S") + " GMT"
    return render_template("timeline.html", nav=profile_nav, posts=posts, title="Timeline")

if __name__ == "__main__":
    app.run(debug=True)
