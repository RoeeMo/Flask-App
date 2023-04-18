from flask import Flask, render_template, url_for, jsonify, request, flash, make_response, redirect
from database import load_items, add_item_to_db, register_user, search_db, authenticate, del_item_from_db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'somesecretkeyfordev'
permsObj = {'user': ['view', 'edit']}


@app.route('/')
def home():
  items = load_items()
  return render_template('index.html',
                         items=items,
                         username=is_authorized(
                           request.cookies.get('sess_cookie')))


@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if len(username) < 4:
      flash('Username need to be longer than 4 characters', category='error')
    elif password1 != password2:
      flash('Passwords don\'t match', category='error')
    elif len(password1) < 7:
      flash('Password must be atleast 7 characters', category='error')
    else:
      res = register_user(username, password1)
      if 'exist' in res:
        flash(res, category='error')
        return render_template('register.html')
      return redirect(url_for('home'))
    return render_template('register.html')
  return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  else:
    data = request.form
    cookie = authenticate(data.get('username'), data.get('password'))
    if cookie:
      resp = make_response(redirect('/'))
      resp.set_cookie('sess_cookie', cookie)
      return resp

    flash('Username Or Password Was Incorrect', category='error')
    return render_template('login.html')


@app.route('/add_item', methods=['POST'])
def add_item():
  if is_authorized(request.cookies.get('sess_cookie'), 'add'):
    data = request.form
    add_item_to_db(data)
    resp = make_response(redirect('/'))
    return resp
  flash('Not Enough Permissions', category='error')
  resp = make_response(redirect('/'))
  return resp


# @app.route('/edit_item', methods=['POST'])
# def edit_item():
#   if is_authorized(request.cookies.get('sess_cookie'), 'edit'):
#     data = request.form


@app.route('/del_item', methods=['POST'])
def del_item():
  if is_authorized(request.cookies.get('sess_cookie'), 'del'):
    del_item_from_db(request.form.get('item_id'))
    resp = make_response(redirect('/'))
    return resp
  flash('Not Enough Permissions', category='error')
  resp = make_response(redirect('/'))
  return resp


@app.route('/api/items')
def list_items():
  return jsonify(load_items())


def is_authorized(cookie, action="null"):
  try:
    type = search_db('users', 'cookie', cookie, grep='type')[0][0]
    user = search_db('users', 'cookie', cookie, grep='username')[0][0]
    if (type == 'admin') or (action in permsObj[type]):
      return user
    else:
      return False
  except:
    return


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
