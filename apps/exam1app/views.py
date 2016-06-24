
from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import User,Poke
import bcrypt

def index(request):
	return render(request,'exam1app/index.html')

def register(request):	
	context={"nm":request.POST['nm'],"al":request.POST['al'],"em":request.POST['em'],"pw":request.POST['pw'],"pw2":request.POST['pw2'],"db":request.POST['db']}
	userinformation=User.userManager.register(context['nm'],context['al'],context['em'],context['pw'],context['pw2'],context['db'])
	
	errormessages = userinformation[1]
	request.session['name']=userinformation[1].name
	if userinformation[0]==True:
		return redirect('/show')
	else:
		for key, errormessage in errormessages.iteritems():
			messages.error(request, errormessage)	
		return redirect('/')


def login(request):
	context={"em":request.POST['em'],"pw":request.POST['pw']}
	userinformation=User.userManager.login(context['em'],context['pw'])

	errormessages = userinformation[1]
	# print userinformation[0]
	# print '8'*60
	request.session['name']=userinformation[1].name
	if userinformation[0]==True:
		return redirect('/show')
	else:
		for key, errormessage in errormessages.iteritems():
			messages.error(request, errormessage)	
		return redirect('/')

def poke(request):
	context={'pokedid':request.POST['pokeid'],'pokecount':1,'pokerid':request.POST['pokerid']}
	pokerinfo=Poke.pokeManager.poke(context['pokeid'],context['pokecount'],context['pokerid'])
	returnedpokecount=pokerinfo.pokecount
	return redirect('/show')

def show(request):
	pokers=User.objects.all()+Poke.objects.all()

	return render(request,'exam1app/mypoker.html',{'pokers':pokers})
	