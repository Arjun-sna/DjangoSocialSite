from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from friends.models import friend_req_status
from friends.models import friends
import json

# Create your views here.
def send_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	username = request.session['username']
	email = request.session['email']
	uid = request.session['id']
	if 'friendname' in request.GET:
		friendname = request.GET['friendname']
		if friendname == username:
			return HttpResponse("You cannot send request to youself")
		countuser = User.objects.filter(username__iexact = friendname).count()
		if countuser <= 0:
			return HttpResponse("No user exists with username " + friendname)
		frienddetails = User.objects.get(username__iexact = friendname)
	if 'email' in request.GET:
		fdemail = request.GET['email']
		if fdemail == email:
			return HttpResponse("You cannot send request to youself")
		countuser = User.objects.filter(email__iexact = fdemail).count()
		if countuser <= 0:
			return HttpResponse("No user exists with email " + fdemail)
		frienddetails = User.objects.get(email__iexact = fdemail)
	friendid = frienddetails.id
	friendname = frienddetails.username
	count1 = friends.objects.filter(uid=uid,friendid=friendid).count()
	count2 = friend_req_status.objects.filter(uid=uid,friendid=friendid).count()
	count3 = friend_req_status.objects.filter(uid=friendid,friendid=uid).count()
	if count1 > 0:
		return HttpResponse("You and " + friendname + " are already friends")
	if count2 > 0:
		return HttpResponse("You have already sent a request to " + friendname)
	if count3 > 0:
		return HttpResponse("You already have a friend request form " + friendname)
	storedata = friend_req_status(uid=uid,friendid=friendid)
	storedata.save()
	return HttpResponse("Request Sent to " + friendname)
	
	
def get_friend_requests(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	username = request.session['username']
	email = request.session['email']
	uid = request.session['id']
	reqcount = friend_req_status.objects.filter(friendid=uid).count()
	if reqcount <= 0:
		return HttpResponse("No request")
	allrequests = friend_req_status.objects.filter(friendid=uid).values('uid')
	jsonObj = {}
	for arequest in allrequests:
		fid = arequest['uid'];
		frienddetails = User.objects.get(id__iexact = fid)
		friendname = frienddetails.username
		jsonObj[fid]=[friendname]
	return HttpResponse(json.dumps(jsonObj),content_type="application/json")
	
def accept_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	if 'id' in request.GET:
		friendid = request.GET['id']
	username = request.session['username']
	email = request.session['email']
	uid = request.session['id']
	frienddetails = User.objects.get(id__iexact = friendid)
	friendname = frienddetails.username
	storedata = friends(uid=uid,friendid=friendid,friendname=friendname)
	storedata.save();
	storedata = friends(uid=friendid,friendid=uid,friendname=username)
	storedata.save();
	todelete = friend_req_status.objects.filter(friendid=uid, uid=friendid)
	todelete.delete();
	return HttpResponse(friendname)
	
def reject_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	if 'id' in request.GET:
		friendid = request.GET['id']
	username = request.session['username']
	email = request.session['email']
	uid = request.session['id']
	todelete = friend_req_status.objects.filter(friendid=uid ,uid=friendid)
	todelete.delete();
	return HttpResponse("Rejected")
	
def autocompleteusers_name(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	if request.is_ajax():
		iptext = request.GET.get('term', '')
	username = request.session['username']
	userdetails = User.objects.filter(username__contains=iptext).exclude(username__contains=username)
	result = []
	for auser in userdetails:
		result.append(auser.username)
	data = json.dumps(result)
	return HttpResponse(data,content_type="application/json")
	
def autocompleteusers_email(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	if request.is_ajax():
		iptext = request.GET.get('term', '')
	username = request.session['username']
	userdetails = User.objects.filter(email__contains=iptext).exclude(username__contains=username)
	result = []
	for auser in userdetails:
		result.append(auser.email)
	data = json.dumps(result)
	return HttpResponse(data,content_type="application/json")

def get_all_friends(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	username = request.session['username']
	email = request.session['email']
	uid = request.session['id']
	allfriends = friends.objects.filter(uid=uid).exclude(friendname__iexact=username)
	jsonObj = {}
	for afriend in allfriends:
		jsonObj[afriend.friendid] = [afriend.friendname]
	return HttpResponse(json.dumps(jsonObj),content_type="application/json")
