"""""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.reservation import Reservation
from booking import Booking
from billing import Billing
from guests import Guest



class DBStorage:
    
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("MYSQL_USER")
        passwd = getenv("MYSQL_PWD")
        db = getenv("MYSQL_DB")
        host = getenv("MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''Returns a dictionary of objects'''
        dic = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                dic[key] = obj
        else:
            classes = [Reservation, Booking, Billing, Guest]
            for cls in classes:
                query = self.__session.query(cls)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    dic[key] = obj
        return dic

    def new(self, obj):
        '''Add a new object to the session'''
        self.__session.add(obj)

    def save(self):
        '''Commit all changes in the session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Delete an object from the session'''
        if obj:
            self.__session.delete(obj)

    def reload(self):
        '''Create tables and session'''
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                               expire_on_commit=False))
        self.__session = Session()

    def close(self):
        '''Close the session'''
        self.__session.close()
        
"""""