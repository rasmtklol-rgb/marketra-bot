
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String

Base = declarative_base()

class Subscription(Base):
    __tablename__="subscriptions"
    guild_id=Column(Integer,primary_key=True)
    expires_at=Column(Integer)
    grace_until=Column(Integer)

class GuildSettings(Base):
    __tablename__="guild_settings"
    guild_id=Column(Integer,primary_key=True)
    prefix=Column(String,default="!")
