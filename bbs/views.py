from django import forms
from django.shortcuts import get_object_or_404, render, redirect
# from django.views import View
from django.views import generic
# from .models import Topic
from .models import Post, Comment

# Create your views here.

# class BbsView(View):

# 	def get(self, request, *args, **kwargs):

# 		topics	= Topic.objects.all()
# 		context = { "topics":topics }
		
# 		return render(request, "bbs/index.html",context)
# 	def post(self, request, *args, **kwargs):
		
# 		posted	= Topic( comment = request.POST["comment"] )
# 		posted.save()

# 		return redirect("bbs:index")

# index		= BbsView.as_view()

## 20210603 add to new line
CommentForm = forms.modelform_factory(Comment, fields=('text', ))

class PostList(generic.ListView):
	"""記事一覧"""
	model = Post

class PostDetail(generic.DetailView):
	"""記事詳細"""
	model = Post

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		#どのコメントにも紐付かないコメント=生地自体へのコメントを取得
		context['comment_list'] = self.object.comment_set.filter(parent__isnull=True)
		return context

def comment_create(request, post_pk):
	"""記事へのコメント作成"""
	post = get_object_or_404(Post, pk=post_pk)
	form = CommentForm(request.POST or None)

	if request.method == 'POST':
		comment = form.save(commit=False)
		comment.post = post
		comment.save()
		# return redirect('blog:post_detail', pk=post.pk)
		return redirect('bbs:post_detail', pk=post.pk)

	context = {
		'form' : form,
		'post' : post
	}
	# return render(request, 'blog/comment_form.html', context)
	return render(request, 'bbs/comment_form.html', context)

def reply_create(request, comment_pk):
	"""コメントへの返信"""
	comment = get_object_or_404(Comment, pk=comment_pk)
	post = comment.post
	form = CommentForm(request.POST or None)

	if request.method == 'POST':
		reply = form.save(commit=False)
		reply.parent = comment
		reply.post = post
		reply.save()	
		# return redirect('blog:post_detail', pk=post.pk)
		return redirect('bbs:post_detail', pk=post.pk)

	context = {
		'form' : form,
		'post' : post,
		'comment' : comment,
	}
	# return render(request, 'blog/comment_form.html', context)
	return render(request, 'bbs/comment_form.html', context)

