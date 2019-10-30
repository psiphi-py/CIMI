from django.shortcuts import render
from .models import Kitchen
from django.http import HttpResponseRedirect
from .forms import CreateNewList
from bs4 import BeautifulSoup
import requests

def index(response, id):
    ls = Kitchen.objects.get(id=id)

    if ls in response.user.kitchen.all():
        if response.method == 'POST':
            if response.POST.get('save'):
                for ingredient in ls.ingredient_set.all():
                    if response.POST.get('c'+str(ingredient.id)) == 'clicked':
                        ingredient.delete()

            elif response.POST.get('newItem'):
                txt = response.POST.get('new')
                if len(txt) > 2:
                    ls.ingredient_set.create(text=txt, complete=False)

        return render(response, 'main/list.html', {'ls': ls})

    return render(response, 'main/view.html', {})

def home(response):
    return render(response, 'main/home.html', {'name': 'test'})

def create(response):

    if response.user.kitchen.all():
        return render(response, 'main/existing.html', {})

    else:
        if response.method == 'POST':
            form = CreateNewList(response.POST)

            if form.is_valid():
                n = form.cleaned_data['name']
                k = Kitchen(name=n)
                k.save()
                response.user.kitchen.add(k)


            return HttpResponseRedirect('/%i' %k.id)

        else:
            form = CreateNewList()

        return render(response, 'main/create.html', {'form': form})

def view(response):
    return render(response, 'main/view.html', {})

def delete(response):
    d = response.user.kitchen.all()
    d.delete()
    return render(response, 'main/delete.html', {})


def allrecipes(response):
    kitch = response.user.kitchen.all()
    identity = Kitchen.objects.get(name=kitch[0])
    ing_db = identity.ingredient_set.all()

    keyWord = ''

    for word in ing_db:
        if keyWord == '':
            keyWord = word.text

        else:
            keyWord = keyWord + "+" + word.text

    keyWord = keyWord + "+" + "allrecipes"

    res = requests.get('https://google.com/search?q=' + keyWord + '&ie=utf-8&oe=utf-8')
    soup = BeautifulSoup(res.content, 'html.parser')

    found_recipes = soup.find_all("a")

    rec_lst = []

    for item in found_recipes:
        if 'www.allrecipes.com' in str(item):
            item2 = str(item)

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

    recipe_list = list(dict.fromkeys(rec_lst))
    rec_f4f = []

    for name in recipe_list:
        if 'https://www.allrecipes.com/recipe/' in str(name):
            rec_f4 = name.split('https://www.allrecipes.com/recipe/')
            rec_f4f.append(rec_f4[1])

    rec_v = []
    rec_fv = []

    for name2 in rec_f4f:
        result = ''.join([i for i in name2 if not i.isdigit()])
        result2 = result.replace('-', ' ')
        result3 = result2.replace('/', ' ')
        rec_v.append(result3)

    rec_fv = zip(rec_v, rec_f4f)

    return render(response, 'main/results/allrecipes.html', {'rec_fv':rec_fv})


def foodnetwork(response):
    kitch = response.user.kitchen.all()
    identity = Kitchen.objects.get(name=kitch[0])
    ing_db2 = identity.ingredient_set.all()

    keyWord2 = ''
    rec_lst2 =[]

    for word2 in ing_db2:
        if keyWord2 == '':
            keyWord2 = word2.text

        else:
            keyWord2 = keyWord2 + "+" + word2.text

    keyWord2 = keyWord2 + "+" + "foodnetwork"

    res2 = requests.get('https://google.com/search?q=' + keyWord2 + '&ie=utf-8&oe=utf-8')
    soup = BeautifulSoup(res2.content, 'html.parser')

    found_recipes = soup.find_all("a")

    for item in found_recipes:
        if 'www.foodnetwork.com' in str(item):
            item2 = str(item)
            if 'url?q=' in item2:
                item_s1 = item2.split('url?q=')
                item_s2 = item_s1[1].split('&amp')
                rec_lst2.append(item_s2[0])

    rec_f = list(dict.fromkeys(rec_lst2))
    rec_f4f4 = []

    for name0 in rec_f:
        if 'https://www.foodnetwork.com/recipes/' in str(name0):
            rec_f5 = name0.split('https://www.foodnetwork.com/recipes/')
            rec_f4f4.append(rec_f5[1])
    rec_v = []
    rec_fv = []

    for name2 in rec_f4f4:
        result = ''.join([i for i in name2 if not i.isdigit()])
        result2 = result.replace('-', ' ')
        result3 = result2.replace('/', ' ')
        rec_v.append(result3)

    rec_fv = zip(rec_v, rec_f4f4)

    return render(response, 'main/results/foodnetwork.html', {'rec_fv':rec_fv})

def food_com(response):
    kitch = response.user.kitchen.all()
    identity = Kitchen.objects.get(name=kitch[0])
    ing_db3 = identity.ingredient_set.all()
    keyWord3 = ''
    rec_lst3 = []

    for word2 in ing_db3:
        if keyWord3 == '':
            keyWord3 = word2.text

        else:
            keyWord3 = keyWord3 + "+" + word2.text

    keyWord3 = keyWord3 + "+" + "food.com"

    res3 = requests.get('https://google.com/search?q=' + keyWord3 + '&ie=utf-8&oe=utf-8')
    soup = BeautifulSoup(res3.content, 'html.parser')

    found_recipes = soup.find_all("a")

    for item in found_recipes:
        if 'www.food.com' in str(item):
            item2 = str(item)
            if 'url?q=' in item2:
                item_s1 = item2.split('url?q=')
                item_s2 = item_s1[1].split('&amp')
                rec_lst3.append(item_s2[0])

    rec_f3 = list(dict.fromkeys(rec_lst3))
    rec_f4f = []

    for name in rec_f3:
        if 'https://www.food.com/recipe/' in str(name):
            rec_f4 = name.split('https://www.food.com/recipe/')
            rec_f4f.append(rec_f4[1])

    rec_v = []
    rec_fv = []

    for name2 in rec_f4f:
        result = ''.join([i for i in name2 if not i.isdigit()])
        result2 = result.replace('-', ' ')
        rec_v.append(result2)

    rec_fv = zip(rec_v, rec_f4f)

    return render(response, 'main/results/food_com.html', {'rec_fv':rec_fv})

def about(response):
    return render(response, 'main/about.html', {})

def contact(response):
    return render(response, 'main/contact.html', {})