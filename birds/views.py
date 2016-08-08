from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views import generic
from django.utils import timezone
from .models import Sighting, Subspecies, Comment, Like
from django.http import HttpResponse
import json
from django.db.models import Q



from .forms import SightingsForm

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden

def about(request):
	return render(request, 'birds/about.html')

def user(request, pk):
	return render(request, 'birds/user.html')

@login_required
def new_sighting(request):
	if request.method == "POST":
		form = SightingsForm(request.POST, request.FILES)
		if form.is_valid():
			s = form.save(commit=False)
			s.user_id = request.user.id
			s.save()
			return redirect('/view_sighting/'+str(s.pk), pk=s.pk)
	else:
		form = SightingsForm()
	return render(request, 'birds/new_sighting.html', {'form': form})

@login_required
def edit_sighting(request, pk):
	this_sighting = get_object_or_404(Sighting, pk=pk)
	if this_sighting.user_id != request.user.id:
		return HttpResponseForbidden()
	form = SightingsForm( request.POST or None, request.FILES or None, instance=this_sighting )
	if request.method == "POST":
		if form.is_valid():
			form.save()
			return redirect('/view_sighting/'+str(pk), pk=pk)
		
	return render(request, 'birds/new_sighting.html', { 'form': form })

def view_sighting(request, pk):
	this_sighting = get_object_or_404(Sighting, pk=pk)
	Comment.objects.filter( sighting = this_sighting, sighting__user_id = request.user.id ).all().update(viewed_by_user = True)
	is_liked = Like.objects.filter( user = request.user, sighting = this_sighting ).count()
	return render(request, 'birds/view_sighting.html', { 'sighting': this_sighting, 'is_liked': is_liked })

def index_view(request):
	latest_sighting_list = Sighting.objects.filter(sighting_date__lte=timezone.now()).order_by('-post_ts')[:10]
	return render(request, 'birds/index.html', { 'latest_sighting_list': latest_sighting_list})
		
def species_query(request):
	if request.method == "GET":
		term = request.GET.get('term')
		l = list(Subspecies.objects.filter( Q(subspecies__icontains=term) | Q(species__species__icontains=term) | Q(species__species_english__icontains=term) ).order_by('subspecies')[:10])
		l2 = [{'value':unicode(i), 'id':i.pk} for i in l]
		data = json.dumps(l2)
		return HttpResponse(data, content_type='application/json')

def get_comments(request):
	if request.is_ajax():
		comments = Comment.objects.filter( sighting = request.POST.get('this_sighting') ).order_by('post_ts')
		return render_to_response('birds/comments.html', {'comments': comments})

@login_required
def get_new_comments_for_user(request):
	if request.is_ajax():
		comments = Comment.objects.filter( sighting__user_id = request.user.id, viewed_by_user = False ).order_by('-post_ts')
		return render_to_response('birds/user_comments.html', {'comments': comments})
		

@login_required
def new_comment(request):
	if request.is_ajax():
		comment = Comment()
		comment.comment = request.POST.get('new_comment')
		comment.sighting_id = request.POST.get('sighting_id')
		comment.user_id = request.user.id
		comment.save()
		return HttpResponse(json.dumps({'msg':'success'}), content_type='application/json')
	
@login_required 
def like(request):
	if request.is_ajax():
		if Like.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id') ).count() > 0:
			return HttpResponse(json.dumps({'msg':'you already liked this one'}), content_type='application/json')
		else:
			like = Like()
			like.user = request.user
			like.sighting_id = request.POST.get('sighting_id')
			like.save()
			new_likes = Sighting.objects.get( pk = request.POST.get('sighting_id') ).num_likes
			return HttpResponse(json.dumps({'msg':'success', 'new_likes': new_likes}), content_type='application/json')
		
@login_required 
def unlike(request):
	if request.is_ajax():
		if Like.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id') ).count() < 1:
			return HttpResponse(json.dumps({'msg':'you have not liked this one'}), content_type='application/json')
		else:
			Like.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id') ).delete()
			new_likes = Sighting.objects.get( pk = request.POST.get('sighting_id') ).num_likes
			return HttpResponse(json.dumps({'msg':'success', 'new_likes': new_likes}), content_type='application/json')
	
#import urllib2
#import json
# def weather(req):
# 	if 'ids' in req.GET and 'appid' in req.GET:
# 		cities = req.GET.get('ids').split(',')
# 		json_output = "["
# 		for city in cities:
# 			result = urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast/city?id='+city+'&APPID='+req.GET.get("appid"))
# 			content = result.read()
# 			content_dict = json.loads(content)
# 			json_output += '{"city":"'+content_dict['city']['name']+'","desc":"'+content_dict['list'][0]['weather'][0]['description']+'","icon":"'+content_dict['list'][0]['weather'][0]['icon']+'"},'
# 
# 		return HttpResponse(json_output[:-1]+"]", content_type='application/json')
# 	else:
# 		return HttpResponse('{"error":"need to supply city and appid."}', content_type='application/json')
