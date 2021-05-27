from django.shortcuts import render, redirect
from django.views import View

from .models import Topic

# Create your views here.

class BbsView(View):

	def get(self, request, *args, **kwargs):

		topics	= Topic.objects.all()
		context = { "topics":topics }
		
		return render(request, "bbs/index.html",context)
	def post(self, request, *args, **kwargs):
		
		posted	= Topic( comment = request.POST["comment"] )
		posted.save()

		return redirect("bbs:index")

index		= BbsView.as_view()

