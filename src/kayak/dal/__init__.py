from sqlalchemy.orm import sessionmaker, mapper, create_session
from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData, Table

from boobox.kayak.dao.AlbumDAO import Album
from boobox.kayak.dao.ItemDAO import Item
from boobox.kayak.dao.CommentDAO import Comment
from boobox.kayak.dao.PhotoDAO import Photo
from boobox.kayak.dao.UserDAO import User

import boobox
import boobox.config

engine = create_engine(boobox.config.DB_LOCATION, echo=boobox.config.DB_DEBUG)
Session = sessionmaker(bind=engine)        

metadata = MetaData(engine)
t_userIndexes = Table(boobox.config.TABLE_USER_INDEX, metadata, autoload=True)
usermapper = mapper(Album, t_userIndexes)
usermapper = mapper(Item, t_userIndexes)
usermapper = mapper(Comment, t_userIndexes)
usermapper = mapper(Photo, t_userIndexes)

t_user = Table(boobox.config.TABLE_USER, metadata, autoload=True)
usermapper = mapper(User, t_user)