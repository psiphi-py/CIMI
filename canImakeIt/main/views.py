# Welcome to the sh!t show
# function-based views are used as debugging resources are more plentiful
# web-scrapping done using beautifulsoup4 and requests

from django.shortcuts import render
from .models import Kitchen
from django.http import HttpResponseRedirect
from .forms import CreateNewList
from bs4 import BeautifulSoup
import requests

# index instances the user with their unique data id
def index(response, id):
    ls = Kitchen.objects.get(id=id)

    # checks if user has a data id relating to the database
    if ls in response.user.kitchen.all():
        if response.method == 'POST':
            # checks if data is checkbox
            if response.POST.get('save'):
                # checkbox data handling allowing ingredient deletion
                for ingredient in ls.ingredient_set.all():
                    # user data processing to see if applicable to database models
                    if response.POST.get('c'+str(ingredient.id)) == 'clicked':
                        ingredient.delete()

            # adding new ingredients to user data
            elif response.POST.get('newItem'):
                txt = response.POST.get('new')
                # invalid ingredient check
                if len(txt) > 2:
                    ls.ingredient_set.create(text=txt, complete=False)

# sending user's Kitchen data to list.html
        return render(response, 'main/list.html', {'ls': ls})

# if user isn't related to a saved user, returns no user specific data
    return render(response, 'main/view.html', {})

# rendering user's homepage
def home(response):
    return render(response, 'main/home.html', {})

# rendering template and form handling of Kitchen creation
def create(response):
# checking if user has a created kitchen
    if response.user.kitchen.all():
        return render(response, 'main/existing.html', {})
# if no user kitchen exists, create a form via django forms for user kitchen creation
    else:
        if response.method == 'POST':
            form = CreateNewList(response.POST)

# django requirement check for forms before adding to database
            if form.is_valid():
                n = form.cleaned_data['name']
                k = Kitchen(name=n)
                k.save()
                response.user.kitchen.add(k)

# sends user's unique data id to user unique views
            return HttpResponseRedirect('/%i' %k.id)

        else:
            form = CreateNewList()
# return to kitchen creation form
        return render(response, 'main/create.html', {'form': form})

# rendering manage kitchen page
def view(response):
    return render(response, 'main/view.html', {})

# algorithm handling ingredient deletion
def delete(response):
    d = response.user.kitchen.all()
    d.delete()
    return render(response, 'main/delete.html', {})


# ------------------------------------Web-scrapping functions----------------------------------------

# web-scrapper searching google results for www.allrecipes.com
def allrecipes(response):
    # find ingredients stored within the user's Kitchen
    kitch = response.user.kitchen.all()
    # kitch[0] as user only has 1 kitchen
    identity = Kitchen.objects.get(name=kitch[0])
    ing_db = identity.ingredient_set.all()

    # instances keyWord as an empty string
    keyWord = ''

    for word in ing_db:
        if keyWord == '':
            # empty keyWord = 1'st ingredient
            keyWord = word.text

        else:
            # if keyWord isn't empty add '+{ingredient}'
            keyWord = keyWord + "+" + word.text

    # end keyWord with relevant website name to improve search results
    keyWord = keyWord + "+" + "allrecipes"

    # beautifulsoup4 scrape method searching google with keyWord
    res = requests.get('https://google.com/search?q=' + keyWord + '&ie=utf-8&oe=utf-8')
    soup = BeautifulSoup(res.content, 'html.parser')

    # scrape results that are hyperlinks
    found_recipes = soup.find_all("a")

    rec_lst = []

    for item in found_recipes:
        # filters results by recipe site names
        if 'www.allrecipes.com' in str(item):
            item2 = str(item)
        # further filtering of results to only get the recipe names from links
            if 'imgrefurl=' in item2:
                item_url = item2

            elif '/&amp;' in item2:
                item_url = item2.split('/&amp;')

            elif '/?sa=' in item2:
                item_url = item2.split('/?sa')

            item_url1 = item_url[0]
            if '/url?q=' in item_url1:
                item_url2 = item_url1.split('/url?q=')

            elif 'href="' in item_url1:
                item_url2 = item_url1.split('href="')


            elif 'imgrefurl=' in item_url1:
                item_url2 = item_url1.split('.jpg&amp;')

            rec_lst.append(item_url2[1])

    # removes duplicates from results
    recipe_list = list(dict.fromkeys(rec_lst))
    rec_f4f = []

    # further filtration of results to get recipe name and split partial hyperlink
    for name in recipe_list:
        if 'https://www.allrecipes.com/recipe/' in str(name):
            rec_f4 = name.split('https://www.allrecipes.com/recipe/')
            rec_f4f.append(rec_f4[1])

    rec_v = []
    rec_fv = []

# removing unnecessary symbols clouding recipe name
    for name2 in rec_f4f:
        result = ''.join([i for i in name2 if not i.isdigit()])
        result2 = result.replace('-', ' ')
        result3 = result2.replace('/', ' ')
        rec_v.append(result3)

    # joining recipe name with recipe partial hyperlink for reference
    rec_fv = zip(rec_v, rec_f4f)

    # sends results and rendering allrecipes.html page
    return render(response, 'main/results/allrecipes.html', {'rec_fv':rec_fv})


def foodnetwork(response):
    # find ingredients stored within the user's Kitchen
    kitch = response.user.kitchen.all()
    # kitch[0] as user only has 1 kitchen
    identity = Kitchen.objects.get(name=kitch[0])
    ing_db2 = identity.ingredient_set.all()

    # instances keyWord as an empty string
    keyWord2 = ''
    rec_lst2 =[]

    for word2 in ing_db2:
        if keyWord2 == '':
            # empty keyWord = 1'st ingredient
            keyWord2 = word2.text

        # if keyWord isn't empty add '+{ingredient}'
        else:
            keyWord2 = keyWord2 + "+" + word2.text

    # end keyWord with relevant website name to improve search results
    keyWord2 = keyWord2 + "+" + "foodnetwork"

    # beautifulsoup4 scrape method searching google with keyWord
    res2 = requests.get('https://google.com/search?q=' + keyWord2 + '&ie=utf-8&oe=utf-8')
    soup = BeautifulSoup(res2.content, 'html.parser')

    # scrape results that are hyperlinks
    found_recipes = soup.find_all("a")

    for item in found_recipes:
        # filters results by recipe site names
        if 'www.foodnetwork.com' in str(item):
            # further filtering of results to only get the recipe names from links
            item2 = str(item)
            if 'url?q=' in item2:
                item_s1 = item2.split('url?q=')
                item_s2 = item_s1[1].split('&amp')
                rec_lst2.append(item_s2[0])

    # removes duplicates from results
    rec_f = list(dict.fromkeys(rec_lst2))
    rec_f4f4 = []

    # further filtration of results to get recipe name and split partial hyperlink
    for name0 in rec_f:
        if 'https://www.foodnetwork.com/recipes/' in str(name0):
            rec_f5 = name0.split('https://www.foodnetwork.com/recipes/')
            rec_f4f4.append(rec_f5[1])
    rec_v = []
    rec_fv = []

    # removing unnecessary symbols clouding recipe name
    for name2 in rec_f4f4:
        result = ''.join([i for i in name2 if not i.isdigit()])
        result2 = result.replace('-', ' ')
        result3 = result2.replace('/', ' ')
        rec_v.append(result3)

    # joining recipe name with recipe partial hyperlink for reference
    rec_fv = zip(rec_v, rec_f4f4)

    # sends results and rendering foodnetwork.html page
    return render(response, 'main/results/foodnetwork.html', {'rec_fv':rec_fv})

def food_com(response):
    # find ingredients stored within the user's Kitchen
    kitch = response.user.kitchen.all()
    # kitch[0] as user only has 1 kitchen
    identity = Kitchen.objects.get(name=kitch[0])
    ing_db3 = identity.ingredient_set.all()
    # instances keyWord as an empty string
    keyWord3 = ''
    rec_lst3 = []

    for word2 in ing_db3:
        # empty keyWord = 1'st ingredient
        if keyWord3 == '':
            keyWord3 = word2.text

        else:
            # if keyWord isn't empty add '+{ingredient}'
            keyWord3 = keyWord3 + "+" + word2.text

    # end keyWord with relevant website name to improve search results
    keyWord3 = keyWord3 + "+" + "food.com"

    # end keyWord with relevant website name to improve search results
    res3 = requests.get('https://google.com/search?q=' + keyWord3 + '&ie=utf-8&oe=utf-8')
    soup = BeautifulSoup(res3.content, 'html.parser')

    # scrape results that are hyperlinks
    found_recipes = soup.find_all("a")

    # filters results by recipe site names
    for item in found_recipes:
        if 'www.food.com' in str(item):
            item2 = str(item)
            # further filtering of results to only get the recipe names from links
            if 'url?q=' in item2:
                item_s1 = item2.split('url?q=')
                item_s2 = item_s1[1].split('&amp')
                rec_lst3.append(item_s2[0])

    # removes duplicates from results
    rec_f3 = list(dict.fromkeys(rec_lst3))
    rec_f4f = []

    # further filtration of results to get recipe name and split partial hyperlink
    for name in rec_f3:
        if 'https://www.food.com/recipe/' in str(name):
            rec_f4 = name.split('https://www.food.com/recipe/')
            rec_f4f.append(rec_f4[1])

    rec_v = []
    rec_fv = []

    # removing unnecessary symbols clouding recipe name
    for name2 in rec_f4f:
        result = ''.join([i for i in name2 if not i.isdigit()])
        result2 = result.replace('-', ' ')
        rec_v.append(result2)

    # joining recipe name with recipe partial hyperlink for reference
    rec_fv = zip(rec_v, rec_f4f)

    # sends results and rendering food_com.html page
    return render(response, 'main/results/food_com.html', {'rec_fv':rec_fv})

# rendering about template
def about(response):
    return render(response, 'main/about.html', {})

# rendering contact template
def contact(response):
    return render(response, 'main/contact.html', {})