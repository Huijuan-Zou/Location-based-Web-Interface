    #import statements
    from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, flash, session, g
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from database_setup import Base, Users, Episodes, Photos
    import copy
    import os
    import datetime
    import geohash
    #create the application object
    app = Flask(__name__)

    #img manipulation
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS

    #setup database
    engine = create_engine('sqlite:///hoodly.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    @app.route('/upload', methods=['GET', 'POST'])        
    def upload():
        if g.user:
            if request.method == 'POST':

                #geting user foreign key for Episode
                username = g.user

                user = dbsession.query(Users).filter_by(id = username).one()
                #episode attributes

                name = request.form['episodename']

                description = request.form['description']
                #extracting first image to put in episode
                images = request.files.getlist("file")
                firstImage = images[0]
                img = Image.open(firstImage)
                try:
                    exif_data = get_exif_data(img)

                except AttributeError:
                    flash("picture(s) " + firstImage.filename + " missing Exif data")
                    return redirect(url_for('upload'))

                coordinates = get_lat_lon(exif_data)
                lat = coordinates[0]
                lon = coordinates[1]
                if lat == None and lon == None:
                    flash("picture(s) " + firstImage.filename + " missing GPS data")
                    return redirect(url_for('upload'))
                else:
                    episode = Episodes(name=name , private=False ,latitude=lat, timestamp = datetime.datetime.now(), geohash = geohash.encode(lat, lon) , longitude=lon, description=description, user=user,  filename= firstImage.filename)
                    dbsession.add(episode)
                    dbsession.commit()

                #adding photos
                target = os.path.join(APP_ROOT, 'episodes/' + str(episode.id))
                
                if not os.path.isdir(target):
                    os.mkdir(target)    
                #add first image
                filename = firstImage.filename
                destination = "/".join([target, filename])

                img.save(destination)
                dbsession.add(Photos(episode=episode, filename= filename, latitude=lat , longitude=lon, geohash = geohash.encode(lat, lon)))
                for image in images[1:]:
                    filename = image.filename
                    img = Image.open(image)
                    try:
                        exif_data = get_exif_data(img)
                    except AttributeError:
                        flash("picture " + image.filename + " missing Exif data it was not included in  the episode")
                        continue

                    coordinates = get_lat_lon(exif_data)
                    if lat == None and lon == None:
                        flash("picture(s) " + firstImage.filename + " missing GPS data it was not included in  the episode")
                        continue
                    else:
                        lat = coordinates[0]
                        lon = coordinates[1]
                        destination = "/".join([target, filename])
                        img.save(destination)
                        #print(lat)
                        #print(lon)
                        dbsession.add(Photos(episode=episode, filename= filename, latitude=lat , longitude=lon, geohash = geohash.encode(lat, lon)))
                        #print(destination)
                dbsession.commit()
                flash("new episode " + episode.name + " created!")
                return redirect(url_for('index'))
            return render_template('upload.html')
        else:
            return redirect(url_for('login'))



    #login page
    @app.route('/', methods=['GET', 'POST'])
    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            session.pop('user', None)
            username = request.form['username'] 
            password = request.form['password']
            correctUser = dbsession.query(Users).filter_by(id=username).first()
            if correctUser is None or password != correctUser.password:
                flash("Error invalid credentials.")
            else:
                session['user'] = request.form['username']
                return redirect(url_for('index'))
        return render_template('javascript_login.html')

    @app.route('/index')
    def index():
        if g.user:
            return render_template('index.html')

        return render_template(url_for('login'))

    @app.before_request
    def before_request():
        g.user = None
        if 'user' in session:
            g.user = session['user']

    @app.route('/photo/<episode_id>/<path>')
    def photo(episode_id, path):
        if g.user:
            return send_file("episodes/" + episode_id +"/" + path)
        else:
            return redirect(url_for('login'))






    @app.route('/newUser', methods=['GET', 'POST'])
    def newUser():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if(dbsession.query(Users).filter_by(id=username).count() != 1):
                newUser = Users(id=username, password=password)
                dbsession.add(newUser)
                dbsession.commit()
                flash("new user created!")
                return redirect(url_for('login'))
            else:
                flash("This username " + username + " is already taken, please choose another. taken please choose another")
                return redirect(url_for('newUser'))
        else:
            return render_template('newuser.html')

    #Making an API Endpoint (GET Request)
    @app.route('/episodes/JSON')
    def episodesJSON():
        if g.user:
            episodes = dbsession.query(Episodes).all()
            return jsonify(episodes=[e.serializeEpisode for e in episodes])

        return redirect(url_for('login'))


    @app.route('/photos/<int:episode_id>/JSON')
    def photosJSON(episode_id):
        if g.user:
            episodes = dbsession.query(Episodes).filter_by(id=episode_id)
            photos = dbsession.query(Photos).filter_by(episode_id=episode_id).all()
            return jsonify(photos=[p.serializePhoto for p in photos])

        return redirect(url_for('login'))

    @app.route('/dropsession')
    def dropsession():
        session.pop('user', None)
        return 'Dropped!'






    ###image manipulation########################

    def get_exif_data(image):
        """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
        exif_data = {}
        info = image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value


        return exif_data

    def _get_if_exist(data, key):
        if key in data:
            return data[key]
            
        return None
        
    def _convert_to_degress(value):
        """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)

    def get_lat_lon(exif_data):
        """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
        lat = None
        lon = None

        if "GPSInfo" in exif_data:      
            gps_info = exif_data["GPSInfo"]

            gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
            gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
            gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
            gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = _convert_to_degress(gps_latitude)
                if gps_latitude_ref != "N":                     
                    lat = 0 - lat

                lon = _convert_to_degress(gps_longitude)
                if gps_longitude_ref != "E":
                    lon = 0 - lon

        return lat, lon



    if __name__ == '__main__':
        app.secret_key = 'super_secret_key'

        app.debug = True

        app.run(host='0.0.0.0', port=5000)