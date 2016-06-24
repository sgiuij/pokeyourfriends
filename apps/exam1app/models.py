from __future__ import unicode_literals

from django.db import models
from django.contrib import messages

import bcrypt
import re

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class UserManager(models.Manager):
	def register(self,name,alias,email,password,password2,dateofbirth):		
		user=self.filter(email=email)
		errors={}
		
		if not user:
			if not alias:
				if password!=password2:
					errors['passwords']="passwords don't matach"
				if len(password)<8:
					errors['passwordlength']="Password is too short!"
				if len(email) < 1:
					errors['emaillength']="Email cannot be blank!"
				if len(name) < 2:
					errors['fnlength']="Name has to be at least 2 characters!"		
				if not EMAIL_REGEX.match(email):
					errors['emailmatch']="Not a valid email"
			else:
				errors['aliasmatch']= "alias already exist!"
		else:
			errors['emailmatch']="user already exists, please login"
		if errors:
			return (False,errors)
		password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
		User.objects.create(name=name,alias=alias,email=email,password=password,birthdate=dateofbirth)
		return (True,self.filter(email__iexact=email)[0])

	# def register(self, **kwargs):
	#	print ("Register a user here")
	#	print ("If successful pass back a tuple with (True, user))")
	#	print ("If unsuccessful return a tuple with (False, 'Registration unsuccessful')")
	#	pass
	def login(self,email,password):
		errors={}
		user=self.filter(email=email)

		if not user:
			errors['emailmatch']="User doesn't exist, please register!"
		else:
			user=user[0]
			# if bcrypt.hashpw(user.password,password)==user.password:
			if bcrypt.hashpw(password.encode("utf-8"), user.password.encode("utf-8")) == user.password.encode("utf-8"):
				return(True,self.filter(email__iexact=email)[0])
			else:
				errors['passowrdmatch']="wrong password!"
		return(False,errors)

class PokeManager(models.Manager):
	def poke(self,pokedid, pokerid):
		thispoker=self.filter(poker=pokerid)
		if not thispoker:
			Poker.objects.create(poked=pokedid,pokecount=1,poker=id,poketotal=poketotal+1)
		else:
			pokerid=Poke.objects.filter(pokerid=pokerid)
			pokecount=pokecount+1
		return (self.filter(poker=pokerid)[0])

class User(models.Model):
	name = models.CharField(max_length=100)
	alias = models.CharField(max_length=20)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	# dateofbirth = models.DateField(input_formats=settings.DATE_INPUT_FORMATS)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	userManager = UserManager()
    # Re-adds objects as a manager
	objects = models.Manager()

class Poke(models.Model):
	poked=models.ForeignKey(User, related_name='p')
	poke=models.IntegerField
	poker=models.ForeignKey(User, related_name='pkr')
	poketotal=models.IntegerField
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	pokeManager = PokeManager()
    # Re-adds objects as a manager
	objects = models.Manager()
