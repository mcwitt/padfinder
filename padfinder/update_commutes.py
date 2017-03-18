import click
import googlemaps
import itertools
import logging
from random import random
from sqlalchemy import not_
from sqlalchemy.orm import sessionmaker
import time

from database import connect, get_or_create, session_scope
from models import (
    ApartmentPost,
    Commute,
    Destination,
    TransitMode,
    DepartureTime
)
from secret import API_KEY

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

G = googlemaps.Client(key=API_KEY)


def _random_pause(scale):
    time.sleep(random() * scale)


def _igrouper(iterable, n):
    while True:
        yield itertools.chain(
            [next(iterable)],
            itertools.islice(iterable, n-1))


def _grouper(seq, n):
    return [list(_) for _ in _igrouper(iter(seq), n)]


def _process_batch(session, posts, destinations, modes, depart_time):
    """Request commute distances and durations for a batch of posts"""

    origins = [(_.latitude, _.longitude) for _ in posts]
    depart_ts = time.mktime(depart_time.timetuple())
    depart_time = get_or_create(session,
                                DepartureTime,
                                ts=depart_time.isoformat())

    for mode_name in modes:
        response = G.distance_matrix(origins,
                                     destinations,
                                     mode=mode_name,
                                     departure_time=depart_ts)

        mode = get_or_create(session, TransitMode, name=mode_name)

        for post, row in zip(posts, response['rows']):
            post.commutes.extend([
                Commute(destination=get_or_create(session,
                                                  Destination,
                                                  name=dest_name),
                        transit_mode=mode,
                        depart_time=depart_time,
                        distance=e['distance']['text'],
                        duration=e['duration']['text'],
                        distance_meters=e['distance']['value'],
                        duration_seconds=e['duration']['value'])
                for dest_name, e in zip(destinations, row['elements'])
                if e['status'] == 'OK'
            ])


def update_commutes(destinations,
                    modes,
                    depart_time,
                    batch_size=50,
                    delay=5):
    """
    Look up commute distances and times from Google Maps API for posts in the
    database that have lat/lon but are missing commute information.
    """

    engine = connect()
    Session = sessionmaker(bind=engine)

    with session_scope(Session) as session:
        query = (
            session
            .query(ApartmentPost)
            .outerjoin(ApartmentPost.commutes)
            .filter(not_(ApartmentPost.commutes.any()))
            .filter(ApartmentPost.latitude != None))

        num_updates = query.count()
        num_processed = 0

        for posts in _grouper(iter(query), batch_size):
            _process_batch(session, posts, destinations, modes, depart_time)
            num_processed += len(posts)
            logger.info("{}/{} commutes processed"
                        .format(num_processed, num_updates))
            _random_pause(delay)


@click.command()
@click.option('--destination', multiple=True, required=True)
@click.option('--transit-mode', multiple=True, default=['driving', 'transit'])
@click.option('--depart-time', default="1 January 2018 7:30 AM")
@click.option('--batch-size', default=20)
@click.option('--download-delay', default=5)
def main(destination, transit_mode, depart_time, batch_size, download_delay):
    from dateutil.parser import parse

    depart_time = parse(depart_time)

    update_commutes(list(destination),
                    transit_mode,
                    depart_time,
                    batch_size,
                    download_delay)


if __name__ == '__main__':
    main()
