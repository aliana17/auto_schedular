from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from secrets import token_urlsafe
from sqlalchemy import exc

engine = create_engine('postgresql://postgres:postgres@localhost:5432/schedular')
Session = sessionmaker(bind=engine)

Base = declarative_base()

# This class will be used to retrive user name for the otp that user will enter during login. 
class Otp(Base):
    __tablename__ = 'otp'
    id = Column(Integer, primary_key=True)
    tg_username = Column(String, nullable=False)
    otp = Column(String, nullable=False)

    def insert_record_in_otp(session, tg_user):
        while True:
            token=token_urlsafe()
            tg_user_present_status = session.query(Otp).filter_by(tg_username=tg_user).all()
            print(tg_user_present_status)
            if not tg_user_present_status:
                new_user = Otp(tg_username=tg_user, otp=token)
                session.add(new_user)
            else:
                session.query(Otp).filter(Otp.tg_username == tg_user).update({"otp":token},synchronize_session="fetch")
            session.commit()
            return token

Base.metadata.create_all(engine)