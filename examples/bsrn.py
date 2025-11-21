import logging

import seastersdb as sdb

logging.basicConfig(
    format="[%(asctime)s]%(levelname)s:%(funcName)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

con = sdb.connect()
log.info("Connection completed")

res = con.execute(
    """
    SELECT r.timestamp, r.station_id, r.DIF
    FROM bsrn('radiation') as r
    JOIN bsrn_stations() AS s USING (station_id)
    WHERE
        r.timestamp BETWEEN TIMESTAMP '2000-01-01' AND TIMESTAMP '2015-02-15'
        AND r.DIF IS NOT NULL
    ORDER BY r.station_id, r.timestamp
"""
)
log.info("Executed query.")

df = res.df()
log.info("Extracted DataFrame.")

print(df)
