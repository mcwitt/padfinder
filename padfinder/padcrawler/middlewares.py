from scrapy.exceptions import IgnoreRequest
from sqlalchemy.orm import sessionmaker

from database import connect
from models import ApartmentPost


class IgnoreDuplicatesMiddleware:

    def __init__(self):
        engine = connect()
        self.Session = sessionmaker(bind=engine)

    def process_request(self, request, spider):
        """
        If requesting post detail page, check whether the post id is already
        present in the database. If not, proceed; else ignore.
        """

        post = request.meta.get('post')

        if post:
            session = self.Session()

            post_exists = (session
                           .query(ApartmentPost)
                           .filter(ApartmentPost.id == post['id'])
                           .first())

            if post_exists:
                raise IgnoreRequest()
