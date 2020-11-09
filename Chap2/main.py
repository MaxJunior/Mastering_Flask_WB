from flask import Flask 
from config import DevConfig 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


class User(db.Model) :
    # explicity declare the table name to connect to, by default is the name of the class, 
    # in this case : 'user'
    # __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref = 'user',
        lazy= 'dynamic'
    )

    def __init__(self, username):
        self.username = username 

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
        
    def __repr__(self):
        return "<User '{}'".format(self.username) 
db.create_all()

tags = db.Table('post_tags',
    db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
    db.Column('tag_id',db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model) :
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50))
    text = db.Column(db.Text())
    # Was updated
    #publish_date = db.Column(db.DateTime())
    publish_date = db.Column(db.DateTime,nullable=False, default=datetime.utcnow )
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    comments  = db.relationship(
        'Comment',
        backref = 'post',
        lazy = 'dynamic'
    )
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts',lazy='dynamic')
    )

    def __init__(self, title):
        self.title = title 
    
    def __repr__(self):
        return "<Post '{}'>".format(self.title)

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self,title):
        self.title= title 
    
    def __repr__(self):
        return "<Tag '{}'>".format(self.title)


class Comment(db.Model) :
    id      = db.Column(db.Integer(), primary_key=True)
    name    = db.Column(db.String(255))
    text    = db.Column(db.Text())
    date    = db.Column(db.DateTime,nullable=False, default=datetime.utcnow )
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'> ...".format(self.text[:15])


@app.route('/')
def home() :
    return '<h1> Hello World ! </h1>'

@app.route('/jogador/')
def index():
    return '<h2> Endeless Factors</h2>'



if __name__ == '__main__' :
    app.secret_key ='secret123'
    app.run()