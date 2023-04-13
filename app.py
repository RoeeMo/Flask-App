from flask import Flask, render_template
from database import load_items

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


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
