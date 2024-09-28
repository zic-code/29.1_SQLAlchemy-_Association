"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#connect to DataBase
def connect_db(app): 
  db.app = app
  db.init_app(app)


class User(db.Model):
  """usermodel"""

  __tablename__="users"
  
  id = db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
  first_name = db.Column(db.String(20),
                nullable=False
                )
  last_name=  db.Column(db.String(20),
                nullable=False)
  
  image_url = db.Column(db.String(200),
                nullable=True 
                        )
  @property
  def full_name(self):
      return f"{self.first_name} {self.last_name}"
  

class Post(db.Model):
  """postModel"""

  __tablename__ = "Post_Model"

  id = db.Column(db.Integer,
                primary_key = True,
                autoincrement =True)
  
  title = db.Column(db.String(20))

  content = db.Column(db.String(20))

  created_at =db.Column(db.DateTime, nullable=False, default = datetime.datetime.now)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

@property
def friendly_date(self):
    """Return nicely-formatted date."""

    return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
