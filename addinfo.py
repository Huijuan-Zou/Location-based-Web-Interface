from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Users, Base, Episodes, Photos
import os
import datetime
import geohash

engine = create_engine('sqlite:///hoodly.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# adding user and some stuff
krishna = Users(id="Krishna Kanth", password = "1234")

session.add(krishna)

session.commit()

temp = geohash.encode(40.7713024, -73.9632393)



episode1 = Episodes(name="Washington Square park", private=False ,latitude=40.7713024, timestamp = datetime.datetime.now(), geohash = temp , longitude=-73.9632393, description="stroll in the park area", user=krishna,  filename= "dog.jpg")

session.add(episode1)


prepath = session.query(Episodes).filter_by(name = "Washington Square park").one()
path = prepath.id





if not os.path.exists("episodes"+"/"+ str(path)):
	os.makedirs("episodes"+"/"+ str(path))

session.commit()

photokrishna = Photos(episode=episode1, filename= "dog.jpg", latitude=40.729340 , longitude=-73.997671, geohash = geohash.encode(40.729340, -73.997671) )
photokrishna2 = Photos(episode=episode1, filename="lion.jpg", latitude=40.729869 , longitude=-73.994494, geohash = geohash.encode(40.729869, -73.994494) )
photokrishna3 = Photos(episode=episode1, filename="squirrel.png", latitude=40.729862 , longitude=-73.994495, geohash = geohash.encode(40.729862, -73.994495) )

session.add(photokrishna)
session.add(photokrishna2)
session.add(photokrishna3)


hoodly = Users(id="Hoodly", password="Hoodly123456")
session.add(hoodly)
session.commit()


bobby = Users(id="Bobby", password="12345")
session.add(bobby)
session.commit()





episodepier = Episodes(name="Pier 45", private=False ,latitude=40.733129, timestamp = datetime.datetime.now(), longitude=-74.013771, description="pier in the afternoon", user=bobby, geohash=geohash.encode(40.733129, -74.013771), filename= "IMG_20160720_192731.jpg",)

session.add(episodepier)


prepath = session.query(Episodes).filter_by(name = "Pier 45").one()
path = prepath.id





if not os.path.exists("episodes"+"/"+ str(path)):
	os.makedirs("episodes"+"/"+ str(path))

session.commit()

a = Photos(episode=episodepier, filename= "IMG_20160720_192731.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
b = Photos(episode=episodepier, filename= "IMG_20160720_192836.jpg", latitude=40.733242 , longitude=-74.013550, geohash = geohash.encode(40.733242, -74.013550) )
c = Photos(episode=episodepier, filename= "IMG_20160720_193414.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
d = Photos(episode=episodepier, filename= "IMG_20160720_194100.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
e = Photos(episode=episodepier, filename= "IMG_20160720_194123.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
f = Photos(episode=episodepier, filename= "IMG_20160720_194126.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
g = Photos(episode=episodepier, filename= "IMG_20160720_194149.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
h = Photos(episode=episodepier, filename= "IMG_20160720_194218.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
i = Photos(episode=episodepier, filename= "IMG_20160720_194230.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
j = Photos(episode=episodepier, filename= "IMG_20160720_194239.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
k = Photos(episode=episodepier, filename= "IMG_20160720_194252.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
l = Photos(episode=episodepier, filename= "IMG_20160720_194315.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
m = Photos(episode=episodepier, filename= "IMG_20160720_194452.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
n = Photos(episode=episodepier, filename= "IMG_20160720_194459.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
o = Photos(episode=episodepier, filename= "IMG_20160720_194518.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
p = Photos(episode=episodepier, filename= "IMG_20160720_195054.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
q = Photos(episode=episodepier, filename= "IMG_20160720_195317.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
r = Photos(episode=episodepier, filename= "IMG_20160720_195401.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
s = Photos(episode=episodepier, filename= "IMG_20160720_195625.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
t = Photos(episode=episodepier, filename= "IMG_20160720_200214.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
u = Photos(episode=episodepier, filename= "IMG_20160720_200221.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
v = Photos(episode=episodepier, filename= "IMG_20160720_200643.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
x = Photos(episode=episodepier, filename= "IMG_20160720_200646.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
y = Photos(episode=episodepier, filename= "IMG_20160720_200651.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
z = Photos(episode=episodepier, filename= "IMG_20160720_200658.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
aa = Photos(episode=episodepier, filename= "IMG_20160720_201048.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
bb = Photos(episode=episodepier, filename= "IMG_20160720_201132.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
cc = Photos(episode=episodepier, filename= "IMG_20160720_201321.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
dd = Photos(episode=episodepier, filename= "IMG_20160720_213148.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )
ee = Photos(episode=episodepier, filename= "IMG_20160720_213326.jpg", latitude=40.733207 , longitude=-74.013719, geohash = geohash.encode(40.733207, -74.013719) )


session.add(a)
session.add(b)
session.add(c)
session.add(d)
session.add(e)
session.add(f)
session.add(g)
session.add(h)
session.add(i)
session.add(j)
session.add(k)
session.add(l)
session.add(m)
session.add(n)
session.add(o)
session.add(p)
session.add(q)
session.add(r)
session.add(s)
session.add(t)
session.add(u)
session.add(v)
session.add(x)
session.add(y)
session.add(z)
session.add(aa)
session.add(bb)
session.add(cc)
session.add(dd)
session.add(ee)
session.commit()



alyssa = Users(id="alyssa", password="12345")
session.add(alyssa)
session.commit()




episodecity = Episodes(name="Albertina", private=False ,latitude=48.203258, timestamp = datetime.datetime.now(), longitude=16.368382, description="walk around the city", user=alyssa, geohash=geohash.encode(48.203258, 16.368382),  filename= "IMG_0787.jpg")


session.add(episodecity)


prepath = session.query(Episodes).filter_by(name = "Albertina").one()
path = prepath.id





if not os.path.exists("episodes"+"/"+ str(path)):
	os.makedirs("episodes"+"/"+ str(path))

session.commit()

ax = Photos(episode=episodecity, filename= "IMG_0787.jpg", latitude=48.226181 , longitude=16.509059, geohash = geohash.encode(48.226181, 16.509059) )
bx = Photos(episode=episodecity, filename= "IMG_0789.jpg", latitude=48.203215 , longitude=16.36673, geohash = geohash.encode(48.203215, 16.36673) )
cx = Photos(episode=episodecity, filename= "IMG_0790.jpg", latitude=48.204309 , longitude=16.368457, geohash = geohash.encode(48.204309, 16.368457) )
dxa = Photos(episode=episodecity, filename= "IMG_0808.jpg", latitude=48.204502 , longitude=16.368962 , geohash = geohash.encode(48.204502 , 16.368962 ))
dxb = Photos(episode=episodecity, filename= "IMG_0791.jpg", latitude=48.204902 , longitude=16.368962 , geohash = geohash.encode(48.204502 , 16.368962))
dxc = Photos(episode=episodecity, filename= "IMG_0793.jpg", latitude=48.205031 , longitude=16.368736 , geohash = geohash.encode(48.204902 , 16.368736))
dxe = Photos(episode=episodecity, filename= "IMG_0794.jpg", latitude=48.204402 , longitude=16.367256 , geohash = geohash.encode(48.205031 , 16.367256))
dxi = Photos(episode=episodecity, filename= "IMG_0795.jpg", latitude=48.202664 , longitude=16.367063 , geohash = geohash.encode(48.204402 , 16.367063))
dxj = Photos(episode=episodecity, filename= "IMG_0796.jpg", latitude=48.203951 , longitude=16.368168 , geohash = geohash.encode(48.202664 , 16.368168))
dxk = Photos(episode=episodecity, filename= "IMG_0797.jpg", latitude=48.204287 , longitude=16.368962 , geohash = geohash.encode(48.203951 , 16.368962))
dxl = Photos(episode=episodecity, filename= "IMG_0798.jpg", latitude=48.203959 , longitude=16.368254 , geohash = geohash.encode(48.204287 , 16.368254))
dxm = Photos(episode=episodecity, filename= "IMG_0799.jpg", latitude=48.203662 , longitude=16.368929 , geohash = geohash.encode(48.203959 , 16.368929))
dxn = Photos(episode=episodecity, filename= "IMG_0806.jpg", latitude=48.203858 , longitude=16.370174 , geohash = geohash.encode(48.203662 , 16.370174))


session.add(ax)
session.add(bx)
session.add(cx)
session.add(dxa)
session.add(dxb)
session.add(dxc)
session.add(dxe)
session.add(dxi)
session.add(dxj)
session.add(dxk)
session.add(dxl)
session.add(dxm)
session.add(dxn)

session.commit()

episodepark = Episodes(name="Aspern Seestadt", private=False ,latitude=48.226181, timestamp = datetime.datetime.now(), longitude=16.509059, description="walk around the park", user=alyssa, geohash=geohash.encode(48.226181, 16.509059), filename = "IMG_0564.jpg")



session.add(episodepark)


prepath = session.query(Episodes).filter_by(name = "Aspern Seestadt").one()
path = prepath.id





if not os.path.exists("episodes"+"/"+ str(path)):
	os.makedirs("episodes"+"/"+ str(path))

session.commit()

ay = Photos(episode=episodepark, filename="IMG_0564.jpg", latitude=48.226181 , longitude=16.509059, geohash = geohash.encode(48.203258, 16.368382) )
aa = Photos(episode=episodepark, filename= "IMG_0571.jpg", latitude=48.226445 , longitude=16.509059, geohash = geohash.encode(48.226181, 16.509059) )
ad = Photos(episode=episodepark, filename= "IMG_0575.jpg", latitude=48.226781 , longitude=16.509059, geohash = geohash.encode(48.226181, 16.509059) )
af = Photos(episode=episodepark, filename= "IMG_0577.jpg", latitude=48.22651 , longitude=16.509059, geohash = geohash.encode(48.226181, 16.509059) )
ag = Photos(episode=episodepark, filename= "IMG_0578.jpg", latitude=48.227303 , longitude=16.509059, geohash = geohash.encode(48.226181, 16.509059) )
ah = Photos(episode=episodepark, filename= "IMG_0588.jpg", latitude=48.225988 , longitude=16.509059, geohash = geohash.encode(48.226181, 16.509059) )



session.add(ay)
session.add(aa)
session.add(ad)
session.add(af)
session.add(ag)
session.add(ah)

session.commit()

print "added episode items!"
