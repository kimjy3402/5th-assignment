from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog
#model 사용하겠다는 거 알려줘야 함
from django.core.paginator import Paginator
from .forms import BlogPost, CommentForm #추가된 부분

def blog(request):
    blogs = Blog.objects #pylint: disable=E1101
    #모델로부터 받아 처리할 수 있게끔
    #쿼리셋(을 기능적으로 처리하게 해주는 방법 --> 메소드)
    #모델이름.쿼리셋(objects).메소드()
    blog_list = Blog.objects.all() #블로그 모든 글들을 대상으로 #pylint: disable=E1101
    paginator = Paginator(blog_list, 3) #블로그 객체 세개를 한 페이지로 자르기
    page = request.GET.get('page') #request된 페이지가 뭔지를 알아내고
    posts = paginator.get_page(page) #request된 페이지(page변수)를 얻어온 뒤 return해 준다.
    return render(request, 'blog.html', {'blogs' : blogs, 'posts':posts})

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    # comment = get_object_or_404(Comment, pk=blog_id)
    return render(request, 'blog/detail.html', {'blog': blog_detail})

def new(request):
    return render(request, 'blog/new.html')

def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/' + str(blog.id)) #pylint: disable=E1101
    # render가 '요청이 들어오면 이 html 파일을 보여줘 라는 녀석'이였다면,
    # redirect는 '요청을 들어오면 저쪽 url로 보내버려' 하는 녀석

def blogpost(request):
    if request.method == 'POST' :
        form = BlogPost(request.POST)
        if form.is_valid():
                post = form.save(commit=False)
                post.pub_date = timezone.now()
                post.save()
                return redirect('blog')

    #2. 빈 페이지를 띄워주는 기능
    else:
            form = BlogPost()
    return render(request, 'blog/new.html', {'form':form})

#추가된 부분
def newcomment(request, blog_id):
    
    post = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            # return redirect('detail', pk=blog_id)
            return redirect('/' + str(post.id))
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})