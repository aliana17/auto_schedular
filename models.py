from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from secrets import token_urlsafe
from sqlalchemy import exc

engine = create_engine('postgresql://postgres:postgres@localhost:5432/schedular')
Session = sessionmaker(bind=engine)

Base = declarative_base()

# This class will be used to retrive user name for the otp that user will enter during login. 

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_username = Column(String, nullable=False)
    otp = Column(String, nullable=False, unique=True)
    groups = relationship('Group', secondary='link')

    def insert_record_in_user(session, tg_user):
        while True:
            token=token_urlsafe()
            tg_user_present_status = session.query(User).filter_by(tg_username=tg_user).all()
            if not tg_user_present_status:
                new_user = User(tg_username=tg_user, otp=token)
                session.add(new_user)
            else:
                session.query(User).filter(User.tg_username == tg_user).update({"otp":token},synchronize_session="fetch")
            session.commit()
            return token

# This class will be used to save the group names that a user will enter
class Group(Base):
    __tablename__ = 'groups'
    grp_id = Column(String, primary_key=True)
    group_name = Column(String, nullable=False,unique=True)
    users = relationship('User',secondary='link')

    def add_group(session,group_id,group_name):
        new_group = Group(grp_id=group_id,group_name=group_name)
        session.add(new_group)
        session.commit()

# This is an attribute class use for building many to many relationship between user and group tables
class Link(Base):
    __tablename__ = 'link'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(String, ForeignKey('groups.grp_id'))

    def insert_record(session,u_id,grp_id):
        new_row = Link(user_id=u_id,group_id=grp_id)
        session.add(new_row)
        session.commit()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id')) 
    linkedin_token = Column(String)
    twitter_token = Column(String)
    fb_token = Column(String)
    fb_pg_id = Column(String)

    def insert_record(session, fb_tkn, twitr_tkn, lkn_tkn, fb_pg_id, u_id):
        user_present_status = session.query(Event).filter(Event.user_id==u_id).all()
        if not user_present_status:
            new_row = Event(user_id=u_id, linkedin_token=lkn_tkn, twitter_token=twitr_tkn, fb_token=fb_tkn, fb_pg_id=fb_pg_id)
            session.add(new_row)
        else:
            session.query(Event).filter(Event.user_id==u_id).update({"linkedin_token":lkn_tkn,"twitter_token":twitr_tkn,"fb_token":fb_tkn,"fb_pg_id":fb_pg_id},synchronize_session="fetch")
        session.commit()

Base.metadata.create_all(engine)