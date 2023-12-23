'''
to render html web pages
'''
import random
from django.http import HttpResponse
from django.template.loader import render_to_string
from articles.models import Article



def home_view(request,id = None,*args,**kwargs):
    '''
    take in a request (django sends request)
    return HTML as a response (we pick to return the response)
    '''
    print(id)
    #print(args,kwargs)
    name  = 'Abhijeet' #HARD CODED
    random_id = random.randint(1,4) #api call (PSEUDO RANDOM)
    #from the dataaabase ??
    
    article_obj = Article.objects.get(id=random_id)
    article_queryset = Article.objects.all()
    #my_list = article_list #[2,5,3,6,3]
    context = {
        "object_list": article_queryset,
        "object": article_obj,
        "title": article_obj.title,
        "id": article_obj.id,
        "content": article_obj.content
    }
    #Django templates

    HTML_STRING = render_to_string("home-view.html",context = context)
    #H1_STRING = '''
    #<h1>hello {title}-{id}</h1>
    #'''.format(**context) 
    #P_STRING = '''
    #<h1> hi {content}-{id}</h1>
    #'''.format(**context)
    #HTML_STRING = H1_STRING + P_STRING
    return HttpResponse(HTML_STRING) 