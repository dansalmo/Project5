from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)
app.secret_key = 'something_nobody_else_knows'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

categories = ['Soccer', 'Basketball', 'Baseball', 'Football', 'Tiddlywinks', 'Misc']

#API end points
@app.route('/catalog.json')
def catalogJSON():
	catalog = session.query(Catalog).all()
	return jsonify(Catalog=[i.serialize for i in catalog])

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
	return render_template('catalog.html', catalog=catalog, categories=categories)

@app.route('/catalog/add/', methods=['GET','POST'])
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
		return render_template('addItem.html', categories=categories)

@app.route('/catalog/<int:item_id>/edit/', methods=['GET','POST'])
def editItem(item_id):
	'''This page will edit an item to the catalog'''
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
		return render_template('editItem.html', categories=categories, item=item)

@app.route('/catalog/<int:item_id>/delete/', methods=['GET','POST'])
def deleteItem(item_id):
	'''This page will delete an item from the catalog'''
	item = session.query(Catalog).filter_by(id = item_id).one()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash('{} was deleted'.format(item.name))
		return redirect(url_for('showCatalog'))
	else:
		return render_template('deleteItem.html', item = item)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
