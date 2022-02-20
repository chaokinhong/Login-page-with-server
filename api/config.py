from dotenv import load_dotenv
import os
import redis

load_dotenv()



class ApplicationConfig:
    #在 python 中通过 os.environ 可以获取有关系统的各种信息 the dict of environment
    #有些字符不宜明文写进代码里 write in .env
    SECRET_KEY = os.environ["SECRET_KEY"]

    # stop logging useless message in db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #every time run a sql function i want to echo what's happening with the database in cmd
    SQLALCHEMY_ECHO = True

    #set the database uri: Uniform Resource Identifier(統一唯一標識符) r: raw string
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"

    #session config for login successful
    SESSION_TYPE = 'redis'

    # we don't want the session to be permanent (forever)
    SESSION_PERMANENT = False

    # use the secret key signer
    SESSION_USE_SIGNER = True

    # point to our redis client
    SESSION_REDIS = redis.from_url('redis://127.0.0.1:6379')
