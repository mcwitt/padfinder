import click
import googlemaps
import itertools
import logging
from random import random
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
from secret import GOOGLE_MAPS_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

G = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


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

    origins = [(p.latitude, p.longitude) for p in posts]
    depart_ts = time.mktime(depart_time.timetuple())
    depart_time = get_or_create(session,
                                DepartureTime,
                                ts=depart_time.isoformat())

    for mode_name in modes:
        response = G.distance_matrix(origins,
                                     list(destinations),
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
                    batch_size,
                    download_delay,
                    max_batches):
    """
    Look up commute distances and times from Google Maps API for posts in the
    database that have lat/lon but are missing commute information.
    """

    engine = connect()
    Session = sessionmaker(bind=engine)

    with session_scope(Session) as session:

        # get posts with location information
        posts_to_update = (session
                           .query(ApartmentPost)
                           .outerjoin(ApartmentPost.commutes)
                           .filter(ApartmentPost.latitude != None,
                                   ~ApartmentPost.commutes.any())
                           .order_by(ApartmentPost.posted_ts.desc()))

        num_updates = posts_to_update.count()
        num_processed = 0

        for i, posts in enumerate(_grouper(posts_to_update, batch_size), 1):
            _process_batch(session, posts, destinations, modes, depart_time)
            num_processed += len(posts)
            logger.info("batch {}: {}/{} commutes processed"
                        .format(i, num_processed, num_updates))
            if i == max_batches:
                logger.warn('reached max_batches=={}; stopping'.format(max_batches))
                break
            _random_pause(download_delay)


@click.command()
@click.option('--destination', multiple=True, required=True)
@click.option('--transit-mode', multiple=True, required=True)
@click.option('--depart-time', default="1 January 2018 7:30 AM")
@click.option('--batch-size', default=20)
@click.option('--download-delay', default=5)
@click.option('--max-batches', default=9999)
def main(destination, transit_mode, depart_time, **kwargs):
    from dateutil.parser import parse
    depart_time = parse(depart_time)
    update_commutes(destinations=destination,
                    modes=transit_mode,
                    depart_time=depart_time,
                    **kwargs)


if __name__ == '__main__':
    main()
