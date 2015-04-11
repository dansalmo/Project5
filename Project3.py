from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)
app.secret_key = 'something_nobody_else_knows_slndv84#4'

# import database ORM and setup libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, User

from flask import session as login_session
import random, string

from functools import wraps

#IMPORTS FOR OAUTH2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
  open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME= "Project3"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#temp global for login
auth = False

categories = ['Soccer', 'Basketball', 'Baseball', 'Football', 'Tiddlywinks', 'Misc']

# login_required decorator definition
def login_required(f):
    @wraps(f)
    def dec_fn(*args, **kwargs):
        if auth:
            return f(*args, **kwargs)
        else:
            next_url = request.url
            login_url = '{}?next={}'.format(url_for('login'), next_url)
            flash('You must be logged in to change anything %s' % login_url)
            print next_url
            return redirect(login_url)
    return dec_fn

@app.route('/login/')
def login():
	'''interstitial login page'''
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', next=request.referrer, STATE=login_session['state'])

#Create anti-forgery state token
@app.route('/login')
def showLogin():
  return "The current session state is %s" % login_session['state']

@app.route('/loggedin/')
def loggedin():
	global auth
	auth = True
	if request.args.get('next'):
		return redirect(request.args.get('next'))
	else:
		return redirect(url_for('showCatalog'))

@app.route('/logout/')
def logout():
	global auth
	auth = False
	nextURL = request.referrer
	# change next URL if logout happend on a page that requires login
	toCheck = ['/add/', '/edit/', '/delete/']
	if [path for path in toCheck if path in nextURL]:
		nextURL = nextURL.replace('/add/', '')
		nextURL = nextURL.replace('/edit/', '/show/')
		nextURL = nextURL.replace('/delete/', '/show/')
		
	return redirect(nextURL)

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
  if request.args.get('state') != login_session['state']:
    response = make_response(json.dumps('Invalid state parameter.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  access_token = request.data
  print "access token received %s "% access_token

  #Exchange client token for long-lived server-side token
 ## GET /oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-lived-token} 
  app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
  app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
  url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id,app_secret,access_token)
  h = httplib2.Http()
  result = h.request(url, 'GET')[1]

  #Use token to get user info from API 
  userinfo_url =  "https://graph.facebook.com/v2.2/me"
  #strip expire tag from access token
  token = result.split("&")[0]
  
  url = 'https://graph.facebook.com/v2.2/me?%s' % token
  h = httplib2.Http()
  result = h.request(url, 'GET')[1]
  #print "url sent for API access:%s"% url
  #print "API JSON result: %s" % result
  data = json.loads(result)
  login_session['provider'] = 'facebook'
  login_session['username'] = data["name"]
  login_session['email'] = data["email"]
  login_session['facebook_id'] = data["id"]
  

  #Get user picture
  url = 'https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200&width=200' % token
  h = httplib2.Http()
  result = h.request(url, 'GET')[1]
  data = json.loads(result)

  login_session['picture'] = data["data"]["url"]
  
  # see if user exists
  user_id = getUserID(login_session['email'])
  if not user_id:
    user_id = createUser(login_session)
  login_session['user_id'] = user_id
    
  output = ''
  output +='<h1>Welcome, '
  output += login_session['username']

  output += '!</h1>'
  output += '<img src="'
  output += login_session['picture']
  output +=' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '


  flash ("Now logged in as %s" % login_session['username'])
  return output

@app.route('/fbdisconnect')
def fbdisconnect():
  facebook_id = login_session['facebook_id']
  url = 'https://graph.facebook.com/%s/permissions' % facebook_id
  h = httplib2.Http()
  result = h.request(url, 'DELETE')[1] 
  return "you have been logged out"
@app.route('/gconnect', methods=['POST'])
def gconnect():
#Validate state token 
  if request.args.get('state') != login_session['state']:
    response = make_response(json.dumps('Invalid state parameter.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  #Obtain authorization code
  code = request.data
  
  try:
    # Upgrade the authorization code into a credentials object
    oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)
  except FlowExchangeError:
    response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  
  # Check that the access token is valid.
  access_token = credentials.access_token
  url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
         % access_token)
  h = httplib2.Http()
  result = json.loads(h.request(url, 'GET')[1])
  # If there was an error in the access token info, abort.
  if result.get('error') is not None:
    response = make_response(json.dumps(result.get('error')), 500)
    response.headers['Content-Type'] = 'application/json'

    
  # Verify that the access token is used for the intended user.
  gplus_id = credentials.id_token['sub']
  if result['user_id'] != gplus_id:
    response = make_response(
        json.dumps("Token's user ID doesn't match given user ID."), 401)
    response.headers['Content-Type'] = 'application/json'
    return response

  # Verify that the access token is valid for this app.
  if result['issued_to'] != CLIENT_ID:
    response = make_response(
        json.dumps("Token's client ID does not match app's."), 401)
    print "Token's client ID does not match app's."
    response.headers['Content-Type'] = 'application/json'
    return response

  stored_credentials = login_session.get('credentials')
  stored_gplus_id = login_session.get('gplus_id')
  if stored_credentials is not None and gplus_id == stored_gplus_id:
    response = make_response(json.dumps('Current user is already connected.'),
                             200)
    response.headers['Content-Type'] = 'application/json'
    return response
    
  # Store the access token in the session for later use.
  login_session['credentials'] = credentials.access_token
  login_session['gplus_id'] = gplus_id
 
  
  #Get user info
  userinfo_url =  "https://www.googleapis.com/oauth2/v1/userinfo"
  params = {'access_token': credentials.access_token, 'alt':'json'}
  answer = requests.get(userinfo_url, params=params)
  
  data = answer.json()

  login_session['username'] = data['name']
  login_session['picture'] = data['picture']
  login_session['email'] = data['email']
  #ADD PROVIDER TO LOGIN SESSION
  login_session['provider'] = 'google'
 
  #see if user exists, if it doesn't make a new one
  user_id = getUserID(data["email"])
  if not user_id:
    user_id = createUser(login_session)
  login_session['user_id'] = user_id


  output = ''
  output +='<h1>Welcome, '
  output += login_session['username']
  output += '!</h1>'
  output += '<img src="'
  output += login_session['picture']
  output +=' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
  flash("you are now logged in as %s"%login_session['username'])
  print "done!"
  return output

#User Helper Functions
def createUser(login_session):
  newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
  session.add(newUser)
  session.commit()
  user = session.query(User).filter_by(email = login_session['email']).one()
  return user.id

def getUserInfo(user_id):
  user = session.query(User).filter_by(id = user_id).one()
  return user

def getUserID(email):
  try:
      user = session.query(User).filter_by(email = email).one()
      return user.id
  except:
      return None

#DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
  #Only disconnect a connected user.
  credentials = login_session.get('credentials')
  if credentials is None:
    response = make_response(json.dumps('Current user not connected.'),401)
    response.headers['Content-Type'] = 'application/json'
    return response 
  access_token = credentials.access_token
  url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
  h = httplib2.Http()
  result = h.request(url, 'GET')[0]
  if result['status'] != '200':
    # For whatever reason, the given token was invalid.
    response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    response.headers['Content-Type'] = 'application/json'
    return response

  #API end points
@app.route('/catalog.json')
def catalogJSON():
	catalog = session.query(Catalog).all()
	return jsonify(Catalog=[i.serialize for i in catalog])

@app.route('/catalog.xml')
def catalogXML():
	"""Generate xmlfeed - Makes a list of items from catalog."""
	items = session.query(Catalog).all()
	sitemap_xml = render_template('xmlfeed.xml', items=items)
	response = make_response(sitemap_xml)
	response.headers["Content-Type"] = "application/xml"
	print ', '.join("%s" % vars(i) for i in items)   
	return response

#HTML end points
@app.route('/')
@app.route('/catalog/')
@app.route('/catalog/<string:category>/')
def showCatalog(category=None):
	'''This page will show my catalog items'''
	if category:
		catalog = session.query(Catalog)\
			.filter_by(category=category)\
			.all()
	else:
		catalog = session.query(Catalog)\
			.order_by(Catalog.id.desc())\
			.limit(10)\
			.all()
	return render_template('catalog.html', catalog=catalog, categories=categories, category=category, auth=auth)


@app.route('/catalog/add/', methods=['GET','POST'])
@login_required
def addItem():
	'''This page will add a new item to the catalog'''
	if request.method == 'POST':
		newItem = Catalog(
					name = request.form['name'], 
					description = request.form['description'], 
					category = request.form['category'], 
					)
		session.add(newItem)
		session.commit()
		flash('{} was successfully added to the catalog'.format(request.form['name']))
		return redirect(url_for('showCatalog'))
	else:
		return render_template('addItem.html', categories=categories, auth=auth)

@app.route('/catalog/<int:item_id>/show/', methods=['GET','POST'])
def showItem(item_id):
	'''This page will show an item from the catalog'''
	item = session.query(Catalog).filter_by(id = item_id).one()
	return render_template('showItem.html', item=item, auth=auth, next=request.url)

@app.route('/catalog/<int:item_id>/edit/', methods=['GET','POST'])
@login_required
def editItem(item_id):
	'''This page will edit an item in the catalog'''
	item = session.query(Catalog).filter_by(id = item_id).one()
	if request.method == 'POST':
		#update only fields that have new values
		for field in request.form:
			if request.form[field]:
				setattr(item, field, request.form[field])
		session.commit()
		flash('{} was successfully changed'.format(request.form['name']))
		return redirect(url_for('showCatalog'))
	else:
		return render_template('editItem.html', categories=categories, item=item, auth=auth)

@app.route('/catalog/<int:item_id>/delete/', methods=['GET','POST'])
@login_required
def deleteItem(item_id):
	'''This page will delete an item from the catalog'''
	item = session.query(Catalog).filter_by(id = item_id).one()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash('{} was deleted'.format(item.name))
		return redirect(url_for('showCatalog'))
	else:
		return render_template('deleteItem.html', item=item, auth=auth)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
