"""
this file contains maintanence functions.
These are not designed to be public available via crossbar endpoints.

"""

from functools import reduce
from sqlalchemy import text
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Session

from iracelog_service_manager.persistence.util import tx_connection
from iracelog_service_manager.persistence.util import tx_session
from iracelog_service_manager.db.schema import Event, Speedmap


@tx_session
def dev_fix_speedmaps(s: Session, eventId: int):
    """fix speedmap during development"""
    # function is no longer used, stays as "what has been done " MP 2022-11-20

    event = s.query(Event).filter_by(id=eventId).first()

    sessionManifest = event.data['manifests']['session']

    extra = get_speedmap_extra_data(eventId)
    # print(f"{extra}\n")
    speedmaps = s.query(Speedmap).filter_by(eventId=eventId).order_by(Speedmap.id).all()
    print(f"len: {len(speedmaps)}")
    for sm in speedmaps:
        newData = {'type': sm.data['type'], 'timestamp': sm.data['timestamp'],
                   'payload': {
            'trackLength': sm.data['payload']['trackLength'],
            'chunkSize': sm.data['payload']['chunkSize'],
            'currentPos': sm.data['payload']['currentPos'],
            'sessionTime': extra[sm.id][sessionManifest.index('sessionTime')],
            'timeOfDay': extra[sm.id][sessionManifest.index('timeOfDay')],
            'trackTemp': extra[sm.id][sessionManifest.index('trackTemp')],
            'data': {k: {'chunkSpeeds': v,
                         'laptime': compute_laptime(v, sm.data['payload']['chunkSize'])} for k, v in sm.data['payload']['data'].items()},

        }}
        sm.data = newData
        # print(f"{newData}")


def compute_laptime(chunks, size) -> float:
    """computes the laptime for each class in this entry(row)"""
    if 0 in chunks:
        return 0
    ret: float = reduce(lambda prev, cur: prev + size / (cur / 3.6), chunks, 0)
    return ret


@tx_connection
def get_speedmap_extra_data(con: Connection, eventId: int):
    res = con.execute(text("""
WITH smData AS
(
  SELECT s.id AS sId,
         TO_TIMESTAMP((s.data -> 'timestamp')::DECIMAL) AS smCur
  FROM speedmap s
  WHERE s.event_id = :eventId
  ORDER BY s.id
),
wData AS
(
  SELECT w.id AS wId,
         TO_TIMESTAMP((w.data -> 'timestamp')::DECIMAL) AS wmCur
  FROM wampdata w
  WHERE w.event_id = :eventId
  ORDER BY w.id
)
SELECT y.sId,
       w.data -> 'payload' -> 'session'
FROM wampdata w
  JOIN (SELECT x.sId,
               x.wId,
               x.rnk
        FROM (SELECT smData.sId,
                     wData.wId,
                     RANK() OVER (PARTITION BY smData.smCur ORDER BY ABS(EXTRACT(milliseconds FROM smData.smCur - wData.wmCur)) ASC) AS rnk
              FROM wData
                CROSS JOIN smData
              WHERE wData.wmCur BETWEEN smData.smCur -INTERVAL '1 seconds' AND smData.smCur +INTERVAL '1 seconds') x
        WHERE rnk = 1) y ON y.wId = w.id
ORDER BY y.sid
;

    """).bindparams(eventId=eventId))
    return {row[0]: row[1] for row in res}
