from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Cylinder(models.Model):
	stachoice=[
	('Fill','fill'),
	('Empty','empty') 
	]
	substachoice=[
	('Available','available'), 
	('Unavailable','unavailable'),
	('Issued','issued') 
	
	]
	cylinderId=models.CharField(max_length=50,primary_key=True,null=False)
	gasName=models.CharField(max_length=200)
	cylinderSize=models.CharField(max_length=30)
	Status=models.CharField(max_length=40,choices=stachoice,default='fill')
	Availability=models.CharField(max_length=40,choices=substachoice,default="Available")
	EntryDate=models.DateTimeField(default=timezone.now)
	issue_Date=models.DateTimeField(null=True)
	issue_user=models.CharField(max_length=70,null=True)
	return_Date=models.DateTimeField(null=True)
	

	def get_absolute_url(self):
		return reverse('cylinderDetail',args=[(self.cylinderId)])

	def __str__(self):
		return str(self.cylinderId)
	class Meta:
		db_table='cylinders'

class Issue(models.Model):
	cylinder=models.ManyToManyField('Cylinder')
	userName=models.CharField(max_length=60,null=False)
	issueDate=models.DateTimeField(default=timezone.now)
	
		
	def __str__(self):
		
		return str(self.userName) 

	class Meta:
		db_table='issues'


class Return(models.Model):
	fill=[
	('Fill','fill'),
	('Empty','empty'),
	('refill','Refill')
	]

	ava=[
	('yes','YES'),
	('no','NO')
	]
	cylinder=models.ManyToManyField('Cylinder')
	availability=models.CharField(max_length=20,choices=ava)
	status=models.CharField(max_length=10,choices=fill)
	returnDate=models.DateTimeField(default=timezone.now)
	

	def __str__(self):
		return str(self.cylinder)

	class Meta:
		db_table='returns'