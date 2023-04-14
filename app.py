from flask import Flask, render_template, jsonify, request
from database import load_items, add_item_from_db

app = Flask(__name__)


@app.route("/")
def home():
  items = load_items()
  return render_template('index.html', items=items)


@app.route("/register")
def register():
  return render_template("/register")


@app.route("/login")
def login():
  return render_template("/login")


@app.route("/add_item", methods=['post'])
def add_item():
  data = request.form
  add_item_from_db(data)
  return jsonify(data)


@app.route("/api/items")
def list_items():
  return jsonify(load_items())


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
