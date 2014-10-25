from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from posts.models import userposts
from friends.models import friends
from django.contrib.auth import authenticate,login
import json
import datetime
# Create your views here.

def login_success(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	username = request.session['username']
	email = request.session['email']
	uid = request.session['id']
	posts=[]
	friend = friends.objects.filter(uid=uid).values('friendid')
	for fnd in friend:
		posts += userposts.objects.filter(uid=fnd['friendid'])
	return render(request,'home.html',{'username':username,'allposts':posts})

def get_all_posts(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')	
	uid = request.session['id']
	jsonObj = {}
	friend = friends.objects.filter(uid=uid).values('friendid')
	posts = userposts.objects.filter(uid__in = friend)
	for apost in posts:
		posteddate = apost.post_date
		curdate = datetime.datetime.now()
		returnstr = ''
		postedyear = posteddate.year
		curyear = curdate.year
		
		postedmonth = posteddate.month
		curmonth = curdate.month
		
		postedday = posteddate.day
		curday = curdate.day
		
		postedhr = posteddate.hour
		curhr = curdate.hour
		
		postedmin = posteddate.minute
		curmin = curdate.minute
		
		if postedyear == curyear:
			if postedmonth == curmonth:
				if postedday == curday:
					if postedhr == curhr:
						returnstr = str(curmin - postedmin) + (' min ago' if (curmin - postedmin) < 2 else ' mins ago')
					else:
						returnstr = str(curhr - postedhr) + (' hour ago' if (curhr - postedhr) < 2 else ' hours ago')
				else:
					returnstr = str(curday - postedday) + (' day ago' if (curday - postedday) < 2 else ' days ago')
			else:
				returnstr = str(curmonth - postedmonth) + (' month ago' if (curmonth - postedmonth) < 2 else ' months ago')
		else:
			returnstr = str(curyear - postedyear) + (' year ago' if (curyear - postedyear) < 2 else ' years ago')
		
		row = apost.post + "," + apost.postedby + "," + returnstr
		jsonObj[apost.id] = [row]
	return HttpResponse(json.dumps(jsonObj),content_type="application/json")
	
def update_post(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	username = request.session['username']
	email = request.session['email']
	uid = request.session['id']
	if 'post' in request.POST:
		postdata = request.POST['post']
		postdata = '<br>'.join(postdata.split('\n'))
		storedata = userposts(uid=uid,postedby=username,post=postdata)
		storedata.save()
	return HttpResponseRedirect('/login_success')

