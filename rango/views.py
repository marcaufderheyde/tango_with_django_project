from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    # Query the database for a list of ALL categories currently stored
    # Order the categories by the number of likes in descending order
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict so that it will be passed to 
    # the tempalate engine.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{boldmessage}} in the template.
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    #Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Marc Auf der Heyde.'}
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # Raises exception if it can't find a category name slug with the givn name
        category = Category.objects.get(slug=category_name_slug)
        
        # Returns associated pages
        pages = Page.objects.filter(category=category)
        
        # Adds the results to the context_dict
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:    
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'rango/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request,question_id):
    return HttpResponse("You're voting on question %s." % question_id)

