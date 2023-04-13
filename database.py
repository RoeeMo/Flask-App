from sqlalchemy import create_engine, text
# from dotenv import load_dotenv
import os
# load_dotenv()

db_conn_str = os.environ['db_conn_str']
engine = create_engine(db_conn_str, connect_args={"ssl": {"ssl_ca": ""}})


# Extract all items and returns a list of dictionaries (each item in a seperate dictionary)
def load_items():
  with engine.connect() as conn:
    result = conn.execute(text("select * from items"))

  items = []
  for row in result.all():
    item_dict = {
      "name": row[1],
      "price": str(row[2]) + row[3],
      "image_url": row[4]
    }
    items.append(item_dict)
  return (items)
