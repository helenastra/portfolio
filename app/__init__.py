import datetime
from playhouse.shortcuts import model_to_dict
import os
import json
from flask import Flask, render_template, request, json
from dotenv import load_dotenv
from peewee import *

load_dotenv()
app = Flask(__name__, template_folder='templates')

if os.getenv("TESTING") == "true":
    print("Running is test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                         user=os.getenv("MYSQL_USER"),
                         password=os.getenv("MYSQL_PASSWORD"),
                         host=os.getenv("MYSQL_HOST"),
                         port=3306
                         )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])

print(mydb)


@app.route('/')
def index():
    return render_template('index.html', title='Team Portfolio',
                           url=os.getenv("URL"))


@app.route('/helen')
def helen():
    return render_template('helen.html', title='Helen', url=os.getenv("URL"))


@app.route('/mauricio')
def mauricio():
    return render_template('mauricio.html', title='Mauricio',
                           url=os.getenv("URL"))


@app.route('/rachel')
def rachel():
    return render_template('rachel.html', title='Rachel', url=os.getenv("URL"))


@app.route('/eliza')
def eliza():
    return render_template('eliza.html', title='Eliza', url=os.getenv("URL"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404', url=os.getenv("URL")), 404


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
        if name == "" or name == None:
            return 'Invalid name', 400
    except:
        return 'Invalid name', 400
    try:
        email = request.form['email']
        if (not (
                "@" in email and "." in email) or email == "" or email == None):
            return 'Invalid email', 400
    except:
        return 'Invalid email', 400
    try:
        content = request.form['content']
        if content == "" or content == None:
            return 'Invalid content', 400
    except:
        return 'Invalid content', 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    mydb.session_commit()
    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")


if __name__ == "__main__":
    app.run()
