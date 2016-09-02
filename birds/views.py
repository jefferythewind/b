from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views import generic
from django.utils import timezone
from .models import Sighting, Subspecies, Comment, Like, SpeciesVote, SpeciesSuggestions, BirdPhoto, Avatar
from django.http import HttpResponse
import json
from django.db.models import Q, IntegerField
from django.db.models.functions import Value



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
		new_sighting = Sighting.objects.create(user_id = request.user.id)
		return redirect('/edit_sighting/'+str(new_sighting.id), pk=new_sighting.id)
# 	return render(request, 'birds/new_sighting.html', {'form': form, 'this_sighting': new_sighting})
	

@login_required
def edit_sighting(request, pk):
	this_sighting = get_object_or_404(Sighting, pk=pk)
	form = SightingsForm( request.POST or None, request.FILES or None, instance=this_sighting )
	if request.method == "POST":
		if this_sighting.user_id != request.user.id:
			return HttpResponseForbidden()
		if form.is_valid():
			form.save()
			return redirect('/view_sighting/'+str(pk), pk=pk)
	elif request.method == "GET":
		return render(request, 'birds/new_sighting.html', { 'form': form, 'this_sighting': this_sighting })

def view_sighting(request, pk):
	this_sighting = get_object_or_404(Sighting, pk=pk)
	species_votes = SpeciesVote.objects.filter( sighting = this_sighting, species = this_sighting.species_tag ).count()
	if request.user.is_authenticated():
		Comment.objects.filter( sighting = this_sighting, sighting__user_id = request.user.id ).all().update(viewed_by_user = True)
		is_liked = Like.objects.filter( user = request.user, sighting = this_sighting ).count()
		is_voted = SpeciesVote.objects.filter( user = request.user, sighting = this_sighting, species = this_sighting.species_tag ).count()	
		return render(request, 'birds/view_sighting.html', { 'sighting': this_sighting, 'is_liked': is_liked, 'is_voted': is_voted,'species_votes': species_votes})
	else:
		return render(request, 'birds/view_sighting.html', { 'sighting': this_sighting, 'species_votes': species_votes})

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
		Comment.objects.create( comment = request.POST.get('new_comment'), sighting_id = request.POST.get('sighting_id'), user_id = request.user.id )
		return HttpResponse(json.dumps({'msg':'success'}), content_type='application/json')
	
@login_required 
def like(request):
	if request.is_ajax():
		if Like.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id') ).count() > 0:
			return HttpResponse(json.dumps({'msg':'you already liked this one'}), content_type='application/json')
		else:
			Like.objects.create( user = request.user, sighting_id = request.POST.get('sighting_id') )
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
		
@login_required 
def up_vote_species(request):
	if request.is_ajax():
		if SpeciesVote.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') ).count() > 0:
			return HttpResponse(json.dumps({'msg':'you have already voted this one'}), content_type='application/json')
		else:
			SpeciesVote.objects.create(  user = request.user, sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') )
			new_votes = SpeciesVote.objects.filter( sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') ).count()
			return HttpResponse(json.dumps({'msg':'success', 'new_votes': new_votes, 'species_id': request.POST.get('species_id')}), content_type='application/json')
		
@login_required 
def down_vote_species(request):
	if request.is_ajax():
		if SpeciesVote.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') ).count() < 1:
			return HttpResponse(json.dumps({'msg':'you have not voted this one'}), content_type='application/json')
		else:
			SpeciesVote.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') ).delete()
			new_votes = SpeciesVote.objects.filter( sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') ).count()
			return HttpResponse(json.dumps({'msg':'success', 'new_votes': new_votes, 'species_id': request.POST.get('species_id')}), content_type='application/json')

@login_required
def suggest_new_species(request):
	if request.is_ajax():  
		if SpeciesSuggestions.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id') ).count() > 0:
			return HttpResponse(json.dumps({'msg':'you have already suggested a species for this post'}), content_type='application/json')
		else:
			SpeciesSuggestions.objects.create( user = request.user, sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id'))
			return HttpResponse(json.dumps({'msg':'success'}), content_type='application/json')

def get_species_suggestions(request):
	if request.is_ajax():
		species_suggestions = SpeciesSuggestions.objects.filter( sighting_id = request.POST.get('sighting_id') ).annotate(is_voted=Value(0, output_field=IntegerField()))
		for suggestion in species_suggestions:
			suggestion.is_voted = SpeciesVote.objects.filter( sighting_id = request.POST.get('sighting_id'), species = suggestion.species, user = request.user ).count()
		return render_to_response('birds/species_suggestions.html', {'species_suggestions': species_suggestions,'user': request.user})
	
@login_required
def add_photo(request):
	if request.is_ajax():
		new_photo = BirdPhoto.objects.create( sighting_id = request.POST.get('sighting_id'), photo = request.FILES.get('bird_photo'), order = 0 )
		return HttpResponse(json.dumps({'msg':'success', 'url': str(new_photo.photo.url)}), content_type='application/json')
	
@login_required
def add_avatar(request):
	if request.is_ajax():
		try:
			new_avatar = request.user.avatar
		except Avatar.DoesNotExist:
			new_avatar = Avatar.objects.create( avatar = request.FILES.get('avatar_photo'), user = request.user )
		else:
			new_avatar.avatar = request.FILES.get('avatar_photo')
			new_avatar.save()
			
		return HttpResponse(json.dumps({'msg':'success', 'url': str(new_avatar.avatar.url)}), content_type='application/json')
	
@login_required
def image_inspect(request):
	if request.is_ajax():
		sighting = Sighting.objects.get(pk = request.POST.get('this_sighting'))
		return render_to_response('birds/image_inspect.html', {'sighting': sighting})
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
