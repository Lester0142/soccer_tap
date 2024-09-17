import sqlalchemy as sal
from sqlalchemy.orm import sessionmaker
import pandas as pd

# create engine
engine = sal.create_engine("sqlite:////home/lester/repos/soccer_tap/src/db.sqlite3")

# initialize metadata obj
meta = sal.MetaData()
meta.reflect(bind=engine)

# create tables in database if they don't exist
meta.create_all(engine)

# bind session
Session = sessionmaker(bind=engine)
session = Session()

# delete smth
RESULT = meta.tables['backend_team']
obj = session.query(RESULT).filter(RESULT.c.id > 4).first()
print(obj)

# Results viewing
sql = sal.text("SELECT * from backend_team")
with engine.connect() as conn:
    result = conn.execute(sql).fetchall()
print(result)


df = pd.read_sql("SELECT * FROM 'backend_team'", engine)
print(df)