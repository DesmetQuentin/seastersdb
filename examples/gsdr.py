import logging

import seastersdb as sdb

logging.basicConfig(
    format="[%(asctime)s]%(levelname)s:%(funcName)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

con = sdb.connect()
log.info("Connection completed")

res = con.execute("""
SELECT r.timestamp, r.station_id, r.Precipitation
FROM gsdr() AS r
JOIN gsdr_stations() AS s USING (station_id)
WHERE
    s.lat BETWEEN 0 AND 20
    AND s.lon BETWEEN 100 AND 120
    AND r.timestamp BETWEEN TIMESTAMP '2000-01-01' AND TIMESTAMP '2015-02-15'
    AND r.Precipitation IS NOT NULL
ORDER BY r.station_id, r.timestamp
""")
log.info("Executed query.")

df = res.df()
log.info("Extracted DataFrame.")

print(df)
