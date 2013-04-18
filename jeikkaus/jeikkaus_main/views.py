from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from jeikkaus import models
from jeikkaus.forms import GuessModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from jeikkaus.models import Guess

@login_required
def match_list(request):
    matches = models.Match.objects.all().order_by('closing_time')
    
    matchlist = []
    for m in matches:
        m.get_guess_for_user(user=request.user) # Populate cache
        matchlist.append(m)
        
    return render_to_response('jeikkaus/matchlist.html', { 'matchlist' : matchlist }, 
                context_instance=RequestContext(request))

def match_details(request, id):
    match = get_object_or_404(models.Match, pk=id)
    
    if match.is_open:
        return HttpResponseRedirect(reverse('match_list'))

    return render_to_response('jeikkaus/matchdetails.html', { 'match' : match }, 
                context_instance=RequestContext(request))
    
def guess(request, id):
    match = get_object_or_404(models.Match, pk=id)
    
    if not match.is_open:
        return HttpResponseRedirect(reverse('match_details', kwargs={'id' : id}))
        
    guess = match.get_guess_for_user(user=request.user)
    
    if request.method == 'POST':
        form = GuessModelForm(data=request.POST, instance=guess)
        if form.is_valid():
            guess = form.save(commit=False)
            guess.user = request.user
            guess.match = match
            guess.save()
            return HttpResponseRedirect(reverse('match_list'))
    else:
        form = GuessModelForm(instance=guess)
        
    return render_to_response('jeikkaus/guessform.html', { 'form' : form },
                context_instance=RequestContext(request))

def scoreboard(request):
    users_with_guesses = User.objects.filter(guess__isnull=False).distinct()
    matches = models.Match.objects.all().order_by('closing_time')
    
    user_total_points = []
    for user in users_with_guesses:
        total_points = reduce(lambda x,y: x+y, map(lambda x: x.points(), user.guess_set.all()))
        user_total_points.append((user, total_points))
        
    user_total_points.sort(key=lambda x: x[1], reverse=True)
    
    scoreboard_dict = {}
    scoreboard_dict['users'] = user_total_points
      
    match_list = []
    for match in matches:
        if match.is_open:
            continue
        
        guesses = []
        for user, points in user_total_points:
            try:
                guess = user.guess_set.get(match=match)
            except Guess.DoesNotExist:
                guess = None
            guesses.append(guess)
        match_list.append((match, guesses,))
    
    scoreboard_dict['matches'] = match_list

    return render_to_response('jeikkaus/scoreboard.html',
                              {'scoreboard' : scoreboard_dict, },
                              context_instance=RequestContext(request))
    