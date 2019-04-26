from django.shortcuts import render, redirect
from .models import News
from ..login.models import User
from django.contrib import messages
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bsoup
import re

def index(request):
    this_user = User.objects.get(id=request.session['id'])
    site_links = []
    site_headlines = []
    user_list = this_user.news.all()
    first_item = this_user.news.first()
    if first_item != None:
        categories = [first_item.list_name]
    else:
        categories = []
    links_dict={}




#Generate list of all of the users news categories
    for list_name in user_list: 

        for category in categories:
            if categories == [] or category != list_name.list_name:
                print('in IF')
                categories.append( list_name.list_name )
            else:
                print('in ELSE')
                continue
    # print('////////////////////////////////////', categories)


#Generate an object where there is a key for each category and it's value will be a list of valuable links

    for category in categories:
        content_list = []
        for entry in user_list:
            site_list = []
            site_links = []
            site_headlines = []
            if entry.list_name == category:
                #open connection to page, copy html as local variable, close connection
                uClient = uReq(f'{ entry.site }')
                page_html = uClient.read()
                uClient.close()
                site_list.append( entry.site )
                #BeautifulSoup Magic
                soup = bsoup( page_html, 'html.parser' )
                for story in soup.find_all('a'):
                    # print('//////////// entry.site = ', entry.site)
                    # print(story.get('href'))
                    if story.get('href') == None:
                        continue
                    if entry.site in story.get('href') and re.search(r'\b[0-9]{4}\b', story.get('href')) != None:
                        site_links.append(story.get('href'))
                        # print('{{{{{{{{{{{{', story.text)
                        for h1 in soup.find_all('a'):
                            for h1 in story.find_all('h1'):
                                values = h1.text
                        for h2 in soup.find_all('a'):
                            for h2 in story.find_all('h2'):
                                values = h2.text
                        for h3 in soup.find_all('a'):
                            for h3 in story.find_all('h3'):
                                values = h3.text
                        for h4 in soup.find_all('a'):
                            for h4 in story.find_all('h4'):
                                values = h4.text
                        if values != '':
                            site_headlines.append(values)

            #Write the links and headlines to the context. 
            print('================', len(site_headlines), len(site_links))

            for content in range(len(site_headlines)):
                content_list.append([site_headlines[content], site_links[content]])
            links_dict.update({ f'{category}': content_list})




            # context.update({ f'{i}_links': site_links })
            # context.update({ f'{i}_headlines': site_headlines})

    
    context={ 'links_dict': links_dict, 'categories': categories}
    print('/////////////context = ', context)

    return render(request, 'tracker/dashboard.html', context)

def new_list(request):
    return render(request, 'tracker/new_list.html')

def create_list(request):
    errors = News.objects.validator(request.POST)


    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/tracker/new_list', request)

    else:
        this_list = News.objects.create(
                                        list_name=request.POST['list_name'],
                                        site=request.POST['url'],
                                        )
        this_user = User.objects.get(id=request.session['id'])
        this_list.users.add(this_user)
        messages.success(request, 'News List Successfully Created')
        return redirect('/tracker', request,)