from sqlalchemy import create_engine, text
import os

db_conn_str = os.environ['DB_CONN_STR']
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
      "image_url": row[4],
      "description": row[5]
    }
    items.append(item_dict)
  return (items)


def add_item_from_db(item):

  with engine.connect() as conn:
    query = text(
      "INSERT INTO items (name, price, currency, image_url, description) VALUES (:name, :price, :currency, :image_url, :description)"
    )
    query = query.bindparams(name=item['name'],
                             price=item['price'],
                             currency=item['currency'],
                             image_url=item['image_url'],
                             description=item['description'])

    conn.execute(query)
