from sqlalchemy.orm import sessionmaker

from database import (
    connect,
    create_tables,
    session_scope,
    get_or_create
)
from models import ApartmentPost, ApartmentTag
from padcrawler.loaders import ApartmentPostLoader


class SQLStorePipeline:

    def __init__(self):
        engine = connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Store items in the database"""

        post = ApartmentPost(**item)
        tags = item['tag_list'].split(ApartmentPostLoader.tag_sep)

        with session_scope(self.Session) as session:
            post.tags = [get_or_create(session, ApartmentTag, name=tag_name)
                         for tag_name in tags]
            session.add(post)

        return item
