import os
from sqlalchemy import create_engine, text
import hashlib, secrets

my_secret = os.environ['PASS_SALT']
db_conn_str = os.environ['DB_CONN_STR']
engine = create_engine(db_conn_str, connect_args={"ssl": {"ssl_ca": ""}})


# Extract all items and returns a list of dictionaries (each item in a seperate dictionary)
def load_items():
  with engine.connect() as conn:
    result = conn.execute(text("select * from items"))

  items = []
  for row in result.all():
    item_dict = {
      "id": row[0],
      "name": row[1],
      "price": str(row[2]) + row[3],
      "image_url": row[4],
      "description": row[5]
    }
    items.append(item_dict)
  return (items)


def add_item_to_db(item):
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


# def edit_item_from_db(item):
#   with engine.connect() as conn:
#     result = conn.execute(
#       text("DELETE FROM items WHERE (id = :id)").bindparams(id=item))
#     return


def del_item_from_db(item):
  with engine.connect() as conn:
    result = conn.execute(
      text("DELETE FROM items WHERE (id = :id)").bindparams(id=item))
    return


def search_db(table, column, params, grep='*', validate_caps=True):
  tmp = ''
  if validate_caps:
    tmp = 'BINARY'
  with engine.connect() as conn:
    query = text(f"SELECT {grep} FROM {table} WHERE {tmp} {column} = :params")
    query = query.bindparams(params=params)
    result = conn.execute(query)
  return result.all()


def register_user(username, password):
  with engine.connect() as conn:
    query = text("SELECT * FROM users WHERE username = :username")
    query = query.bindparams(username=username)
    result = conn.execute(query)
    existing_user = result.fetchone()
    if existing_user:
      return 'User already exist!'
    else:
      hashed_string = hashlib.sha512(my_secret.encode() +
                                     password.encode()).hexdigest()
      query = text(
        "INSERT INTO users (username, password, type) VALUES (:username, :password, 'user')"
      ).bindparams(username=username, password=hashed_string)

      result = conn.execute(query)
      return 'User created successfully'


def authenticate(username, password):
  with engine.connect() as conn:
    hashed_string = hashlib.sha512(my_secret.encode() +
                                   password.encode()).hexdigest()
    query = text(
      "SELECT * FROM users WHERE BINARY username = :username AND BINARY password = :password"
    )
    query = query.bindparams(username=username, password=hashed_string)
    result = conn.execute(query)
    try:
      a = result.all()[0]
      cookie = secrets.token_hex(16)
      query = text(
        "UPDATE users SET cookie = :cookie WHERE username = :username")
      query = query.bindparams(cookie=cookie, username=username)
      conn.execute(query)
      return cookie
    except:
      return ''
