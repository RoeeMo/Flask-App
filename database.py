from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
load_dotenv()

engine = create_engine(os.getenv("db_conn_str"), 
                       connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}}
                       )

# Extract all items from DB and stores them in a dictionary
def load_items():
  with engine.connect() as conn:
    result = conn.execute(text("select * from items"))

  result_dict = {"name": [], "price": [], "image_url": []}

  for row in result.all():
    result_dict.setdefault("name", []).append(row[1])
    result_dict.setdefault("price", []).append(str(row[2]) + row[3])
    result_dict.setdefault("image_url", []).append(row[4])

  return(result_dict)