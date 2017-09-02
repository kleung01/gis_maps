# srid: 4326 (wgs84: match gMaps)
# django cannot have a model without a PK but dd_node has no PK

from django.db import models
from django.contrib.gis.db import models

class userInput(models.Model):
	address = models.CharField(max_length=200)

class roads(models.Model):
	# necessary to create nodes
	source = models.IntegerField(null=True)
	target = models.IntegerField(null=True)
	# costs
	speed_kmh = models.SmallIntegerField()
	dist_km = models.DecimalField(decimal_places=5,max_digits=10)
	cost_min = models.DecimalField(decimal_places=5,max_digits=10)
	# necessary statscan info
	street_type = models.CharField(max_length=6, null=True)
	street_class = models.SmallIntegerField
	ngduid = models.IntegerField()
	# geodjango fields
	the_geom = models.MultiLineStringField(srid=4326)

	class Meta:
		db_table = "maps_roads"

class node(models.Model):
	# node fields
	cnt = models.IntegerField(null=True)
	chk = models.IntegerField(null=True)
	ein = models.IntegerField(null=True)
	eout = models.IntegerField(null=True)
	# geodjango geom
	the_geom = models.PointField(srid=4326)

	class Meta:
		db_table = "maps_node"

class dd_node(models.Model):
	# unique session
	session = models.CharField(max_length=50)
	# node fields
	'''
	cnt = models.IntegerField(null=True)
	chk = models.IntegerField(null=True)
	ein = models.IntegerField(null=True)
	eout = models.IntegerField(null=True)
	seq = models.IntegerField(null=True)
	node = models.BigIntegerField(null=True)
	'''
	edge = models.BigIntegerField(null=True)
	cost = models.FloatField(null=True)
	agg_cost = models.FloatField(null=True)
	# geodjango geom
	the_geom = models.PointField(srid=4326)

class dd_poly(models.Model):
	# unique session
	# session = models.ForeignKey(dd_node, on_delete=models.CASCADE,primary_key=True)
	# geodjango geom
	session = models.CharField(max_length=50, primary_key=True)
	pgr_pointsaspolygon = models.GeometryField(srid=4326)


	#class Meta:
		#db_table = "maps_roads_nodes"

'''
class userLocation(models.Model):
    location = models.CharField(max_length=200)

class userLocationManager(models.Manager):
    def create_loc(self, user_loc):
        loc = self.create(user_loc=user_loc)
        # do something with the book
        return book

class Book(models.Model):

    objects = BookManager()

book = Book.objects.create_book("Pride and Prejudice")
'''