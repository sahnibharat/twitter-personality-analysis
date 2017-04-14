from django.shortcuts import get_object_or_404, redirect, render
from .forms import Query
from .sentiment import TwitterObject
from django.http import HttpResponseRedirect

def home(request):
	form=Query(request.POST or None)
	context = {
		'form': form,
	}
	if form.is_valid():
		request.session['form']=request.POST
		return HttpResponseRedirect('tweetView')
	return render(request,'home.html',context)

def tweetView(request):
	form=Query(request.session.get('form'))
	obj=TwitterObject()
	posTweet=[]
	negTweet=[]
	neutTweet=[]
	posPer=0
	negPer=0
	neutPer=0
	context={
		'posTweet' : posTweet,
		'negTweet' : negTweet,
		'neutTweet' : neutTweet,
		'posPer' : posPer,	
		'negPer' : negPer,
		'neutPer' : neutPer,
	}
	if form.is_valid():
		obj=TwitterObject()
		obj.subj=request.session.get('form')['Query']
		
		obj.fetchTweets()
		ptweets=obj.ptweets 
		ntweets=obj.ntweets
		neutral=obj.neutral

		total=len(ptweets)+len(ntweets)+len(neutral)
		posPer=format(100*len(ptweets)/total)
		negPer=format(100*len(ntweets)/total)
		neutPer=format(100*len(neutral)/total)
		# Positive
		for tweet in ptweets[:100]:
			posTweet.append(tweet['text'])
		# Negative    
		for tweet in ntweets[:100]:
			negTweet.append(tweet['text'])
		# Neutral
		for tweet in neutral[:100]:
			neutTweet.append(tweet['text'])
			
	context={
		'posTweet' : posTweet,
		'negTweet' : negTweet,
		'neutTweet' : neutTweet,
		'posPer' : posPer,	
		'negPer' : negPer,
		'neutPer' : neutPer,
	}
	return render(request,'tweetView.html',context)

	# form = get_object_or_404(str, pk=city_id)
	# deals = Deal.objects.filter(city=city)