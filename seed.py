"""Seed file to make sample data for user db."""
# from models.py import user model and db object
from models import User, db 
# from app.py import app(flask)
from app import app #


# Create all tables
db.drop_all()  # Delete all the table whichs are existed in db(drop)
db.create_all()# Create all the table whichs defined by db(create)

# If table isn't empty, empty it
User.query.delete() # Delete all the record whichs in 'User' table

# Add user
richard = User(first_name='Richard',last_name= 'Gear',image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7xuTNYpCk_GOjgM2a2lVpopy7A97r4uQUNb9M1LlTcTyl07m-lNo5lUJKbI28oGIq-ho&usqp=CAU')
Tom = User(first_name='Tom',last_name= 'Cruise',image_url='https://i.namu.wiki/i/DTp1I6C3vFHRycQPyfjyGVOclv_Vq4eDDHD1WAgnw3Vd_46wbqLCWfEKzTVsUsji9dLkCH3DvU7tlfD4vItnGQ.gif')



 
# Add new objects to session, so they'll persist
db.session.add(richard)
db.session.add(Tom)

#Commit-otherwise, this never gets saved!
db.session.commit()