#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import psycopg2
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
	__tablename__ = 'Venues'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	city = db.Column(db.String(120))
	state = db.Column(db.String(120))
	address = db.Column(db.String(120))
	phone = db.Column(db.String(120))
	genres = db.Column(db.String)
	image_link = db.Column(db.String(500))
	website = db.Column(db.String(120))
	facebook_link = db.Column(db.String(120))
	seeking_talent = db.Column(db.Boolean, default=False)
	seeking_description = db.Column(db.String)

	shows = db.relationship('Show', backref='Venues')

class Artist(db.Model):
	__tablename__ = 'Artists'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	city = db.Column(db.String(120))
	state = db.Column(db.String(120))
	phone = db.Column(db.String(120))
	genres = db.Column(db.String(120))
	image_link = db.Column(db.String(500))
	website = db.Column(db.String(120))
	facebook_link = db.Column(db.String(120))
	seeking_venue = db.Column(db.Boolean, default=False)
	seeking_description = db.Column(db.String)

	shows = db.relationship('Show', backref='Artists')

class Show(db.Model):
	__tablename__ = 'Shows'

	id = db.Column(db.Integer, primary_key=True)
	start_time = db.Column(db.DateTime)
	artist_id = db.Column(db.Integer, db.ForeignKey('Artists.id'), nullable=False)
	venue_id = db.Column(db.Integer, db.ForeignKey('Venues.id'), nullable=False)

	venue = db.relationship('Venue')
	artist = db.relationship('Artist')


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
	date = dateutil.parser.parse(value)
	if format == 'full':
		format="EEEE MMMM, d, y 'at' h:mma"
	elif format == 'medium':
		format="EE MM, dd, y h:mma"
	return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
	return render_template('pages/home.html')


#	Venues
#	----------------------------------------------------------------

@app.route('/venues')
def venues():
	uniqueLocations = db.session.query(Venue.city,Venue.state).order_by(Venue.state, Venue.city).distinct().all()
	venues = Venue.query.order_by(Venue.name).all()
	data = []
	CITY_IDX = 0
	STATE_IDX = 1
	index = 0

	for location in uniqueLocations:
		data.append({
			"city": location[CITY_IDX],
			"state": location[STATE_IDX],
			"venues": []
		})

		for venue in venues:
			if venue.city == location[CITY_IDX] and venue.state == location[STATE_IDX]:
				data[index]['venues'].append({
					"id": venue.id,
					"name": venue.name,
					"num_upcoming_shows": 1
				})
		
		index += 1

	return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
	searchString = request.form['search_term']
	venueList = Venue.query.filter(Venue.name.ilike(f'%{searchString}%')).all()
	data = []

	for venue in venueList:

		data.append({
			"id": venue.id,
			"name": venue.name,
			"num_upcoming_shows": 0
		})

	response={
	"count": len(venueList),
	"data": data
	}

	return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

	venue = Venue.query.get(venue_id)

	print( venue.genres )

	data={
	"id": venue.id,
	"name": venue.name,
	"genres": venue.genres.split( ',' ),
	"city": venue.city,
	"state": venue.state,
	"phone": venue.phone,
	"seeking_talent": venue.seeking_talent,
	"image_link": venue.image_link,
	"past_shows": [{
		"venue_id": 3,
		"venue_name": "Park Square Live Music & Coffee",
		"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
		"start_time": "2019-06-15T23:00:00.000Z"
	}],
	"upcoming_shows": [{
		"venue_id": 3,
		"venue_name": "Park Square Live Music & Coffee",
		"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
		"start_time": "2035-04-01T20:00:00.000Z"
	}, {
		"venue_id": 3,
		"venue_name": "Park Square Live Music & Coffee",
		"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
		"start_time": "2035-04-08T20:00:00.000Z"
	}, {
		"venue_id": 3,
		"venue_name": "Park Square Live Music & Coffee",
		"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
		"start_time": "2035-04-15T20:00:00.000Z"
	}],
	"past_shows_count": 1,
	"upcoming_shows_count": 3,
	}

	return render_template('pages/show_venue.html', venue=data)

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
	form = VenueForm()
	return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
	success = False

	try:
		newVenue = Venue()

		newVenue.name = request.form['name']
		newVenue.city = request.form['city']
		newVenue.state = request.form['state']
		newVenue.address = request.form['address']
		newVenue.phone = request.form['phone']
		newVenue.genres = ",".join(request.form.getlist('genres'))
		newVenue.image_link = request.form['image_link']
		newVenue.website = request.form['website']
		newVenue.facebook_link = request.form['facebook_link']
		newVenue.seeking_talent = False
		if 'seeking_talent' in request.form:
			newVenue.seeking_talent = True
		newVenue.seeking_description = request.form['seeking_description']

		success = True
		db.session.add(newVenue)
		db.session.commit()
		flash(request.form['name'] + ' was successfully listed as a venue!')
	except:
		db.session.rollback()
		print(sys.exc_info())
		flash(request.form['name'] + ' could not be listed as a venue!')
	finally:
		db.session.close()

	if( success ):
		return render_template('pages/home.html')
	else:
		return redirect('/venues/create')

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
	form = VenueForm()
	venue = Venue.query.get(venue_id)

	return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
	success = False
	try:
		updatedVenue = Venue.query.get(venue_id)

		updatedVenue.name = request.form['name']
		updatedVenue.city = request.form['city']
		updatedVenue.state = request.form['state']
		updatedVenue.address = request.form['address']
		updatedVenue.phone = request.form['phone']
		updatedVenue.genres = ",".join(request.form.getlist('genres'))
		updatedVenue.image_link = request.form['image_link']
		updatedVenue.website = request.form['website']
		updatedVenue.facebook_link = request.form['facebook_link']
		updatedVenue.seeking_talent = False
		if 'seeking_talent' in request.form:
			updatedVenue.seeking_talent = True
		updatedVenue.seeking_description = request.form['seeking_description']

		success = True
		db.session.commit()
		flash(request.form['name'] + ' was successfully listed as a venue!')
	except:
		db.session.rollback()
		print(sys.exc_info())
		flash(request.form['name'] + ' could not be listed as a venue!')
	finally:
		db.session.close()

	if( success ):
		return redirect(url_for('show_venue', venue_id=venue_id))
	else:
		return redirect('/venues/' + venue_id + '/edit')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
	success = False

	try:
		Venue.query.filter_by(id=venue_id).delete()
		db.session.commit()
		success = True
		flash('Your venue was successfully removed!')
	except:
		db.session.rollback()
		flash('Your venue could not be removed!')
	finally:
		db.session.close()

	return jsonify({'success': success})

#	Artists
#	----------------------------------------------------------------
@app.route('/artists')
def artists():
	data = Artist.query.all()

	return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
	searchString = request.form['search_term']
	artistList = Artist.query.filter(Artist.name.ilike(f'%{searchString}%')).all()
	data = []

	for artist in artistList:

		data.append({
			"id": artist.id,
			"name": artist.name,
			"num_upcoming_shows": 0
		})

	response={
	"count": len(artistList),
	"data": data
	}

	return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
	artist = Artist.query.get(artist_id)

	data={
	"id": artist.id,
	"name": artist.name,
	"genres": artist.genres.split( ',' ),
	"city": artist.city,
	"state": artist.state,
	"phone": artist.phone,
	"seeking_venue": artist.seeking_venue,
	"image_link": artist.image_link,
	"past_shows": [{
		"venue_id": 3,
		"venue_name": "Park Square Live Music & Coffee",
		"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
		"start_time": "2019-06-15T23:00:00.000Z"
	}],
	"upcoming_shows": [{
		"venue_id": 3,
		"venue_name": "Park Square Live Music & Coffee",
		"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
		"start_time": "2035-04-01T20:00:00.000Z"
	}, {
		"venue_id": 3,
		"venue_name": "Park Square Live Music & Coffee",
		"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
		"start_time": "2035-04-08T20:00:00.000Z"
	}, {
		"venue_id": 3,
		"venue_name": "Park Square Live Music & Coffee",
		"venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
		"start_time": "2035-04-15T20:00:00.000Z"
	}],
	"past_shows_count": 1,
	"upcoming_shows_count": 3,
	}

	return render_template('pages/show_artist.html', artist=data)

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
	form = ArtistForm()
	return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
	success = False
	try:
		newArtist = Artist()

		newArtist.name = request.form['name']
		newArtist.city = request.form['city']
		newArtist.state = request.form['state']
		newArtist.phone = request.form['phone']
		newArtist.genres = ",".join(request.form.getlist('genres'))
		newArtist.image_link = request.form['image_link']
		newArtist.website = request.form['website']
		newArtist.facebook_link = request.form['facebook_link']
		newArtist.seeking_venue = False
		if 'seeking_venue' in request.form:
			newArtist.seeking_venue = True
		newArtist.seeking_description = request.form['seeking_description']

		success = True
		db.session.add(newArtist)
		db.session.commit()
		flash(request.form['name'] + ' was successfully listed as an artist!')
	except:
		db.session.rollback()
		print(sys.exc_info())
		flash(request.form['name'] + ' could not be listed as an artist!')
	finally:
		db.session.close()

	if( success ):
		return render_template('pages/home.html')
	else:
		return redirect('/artists/create')

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
	form = ArtistForm()
	artist = Artist.query.get(artist_id)

	return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
	success = False
	try:
		updateArtist = Artist.query.get(artist_id)

		updateArtist.name = request.form['name']
		updateArtist.city = request.form['city']
		updateArtist.state = request.form['state']
		updateArtist.phone = request.form['phone']
		updateArtist.genres = ",".join(request.form.getlist('genres'))
		updateArtist.image_link = request.form['image_link']
		updateArtist.website = request.form['website']
		updateArtist.facebook_link = request.form['facebook_link']
		updateArtist.seeking_venue = False
		if 'seeking_venue' in request.form:
			updateArtist.seeking_venue = True
		updateArtist.seeking_description = request.form['seeking_description']

		success = True
		db.session.add(updateArtist)
		db.session.commit()
		flash(request.form['name'] + ' was successfully listed as an artist!')
	except:
		db.session.rollback()
		print(sys.exc_info())
		flash(request.form['name'] + ' could not be listed as an artist!')
	finally:
		db.session.close()

	if( success ):
		return redirect(url_for('show_artist', artist_id=artist_id))
	else:
		return redirect('/artists/' + artist_id + '/edit')

#	Shows
#	----------------------------------------------------------------

@app.route('/shows')
def shows():
	# displays list of shows at /shows
	# TODO: replace with real venues data.
	#		 num_shows should be aggregated based on number of upcoming shows per venue.
	data=[{
	"venue_id": 1,
	"venue_name": "The Musical Hop",
	"artist_id": 4,
	"artist_name": "Guns N Petals",
	"artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
	"start_time": "2019-05-21T21:30:00.000Z"
	}, {
	"venue_id": 3,
	"venue_name": "Park Square Live Music & Coffee",
	"artist_id": 5,
	"artist_name": "Matt Quevedo",
	"artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
	"start_time": "2019-06-15T23:00:00.000Z"
	}, {
	"venue_id": 3,
	"venue_name": "Park Square Live Music & Coffee",
	"artist_id": 6,
	"artist_name": "The Wild Sax Band",
	"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
	"start_time": "2035-04-01T20:00:00.000Z"
	}, {
	"venue_id": 3,
	"venue_name": "Park Square Live Music & Coffee",
	"artist_id": 6,
	"artist_name": "The Wild Sax Band",
	"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
	"start_time": "2035-04-08T20:00:00.000Z"
	}, {
	"venue_id": 3,
	"venue_name": "Park Square Live Music & Coffee",
	"artist_id": 6,
	"artist_name": "The Wild Sax Band",
	"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
	"start_time": "2035-04-15T20:00:00.000Z"
	}]
	return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
	# renders form. do not touch.
	form = ShowForm()
	return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
	# called to create new shows in the db, upon submitting new show listing form
	# TODO: insert form data as a new Show record in the db, instead

	# on successful db insert, flash success
	flash('Show was successfully listed!')
	# TODO: on unsuccessful db insert, flash an error instead.
	# e.g., flash('An error occurred. Show could not be listed.')
	# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
	return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
	return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
	return render_template('errors/500.html'), 500


if not app.debug:
	file_handler = FileHandler('error.log')
	file_handler.setFormatter(
		Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
	)
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
	app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
'''
