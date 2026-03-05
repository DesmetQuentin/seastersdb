"""
Examples for accessing the database using the BSRN network.
Executing the query is the basement of the workflow.

Recommendations would be to work in a Jupiter Notebook
or interactive Python shell to query the database and refine
one's filter little by little (commands with the .show()
method below). Once one knows exactly what one's wants to
extract, one can actually extract the data from the database
with, e.g., .df() (requires pandas). Then, one can process
the data normally using pandas, or scaling up with xarray.
Exportation can be done with, e.g., .to_csv(file_name) or
.to_parquet(file_name) (requires pyarrow/fastparquet).
"""

import logging

import seastersdb as sdb

logging.basicConfig(
    format="[%(asctime)s]%(levelname)s:%(funcName)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

con = sdb.connect()
log.info("Connection completed")

# Access metadata
con.sql("SELECT * FROM bsrn_stations()").show()
log.info("Executed request 1.")
con.sql(
    "SELECT * FROM bsrn_stations() WHERE lat BETWEEN -10 AND 0"
).show()  # This should show the MAN station
log.info("Executed request 2.")
con.sql("SELECT * FROM bsrn_var() ORDER BY dataset").show()
log.info("Executed request 3.")
con.sql("SELECT * FROM bsrn_var() WHERE dataset = 'radiation'").show()
log.info("Executed request 4.")

# Access data
res = con.sql("""
    SELECT timestamp, station_id, DIF
    FROM bsrn('radiation') JOIN bsrn_stations() USING (station_id)
    WHERE lat BETWEEN -10 AND 0 AND timestamp BETWEEN TIMESTAMP '2008-01-01' AND TIMESTAMP '2010-01-01'
    ORDER BY timestamp
""")
log.info("Executed request 5.")

# Show/export
res.show()
df = res.df()  # Extract data from the database to a DataFrame (requires pandas)
log.info("Extracted into DataFrame.")
log.debug(df)
# df.to_csv("test.csv")
# df.to_parquet("test.parquet")  # Requires parquet engine (pyarrow/fastparquet)
# log.info("Exported.")
