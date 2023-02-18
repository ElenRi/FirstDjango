from django.shortcuts import render, HttpResponse
from django.http import HttpResponseNotFound
import json
import string
from django.core.paginator import Paginator

with open('/home/student/Projects/DjangoCountriess/country-by-languages.json') as json_file:
    data = json.load(json_file)

letters = list(string.ascii_uppercase)



def main_page(request):
    return render(request, 'index.html')

def countries_list(request):
    countries = []
    for countries_b in data:
        countries.append(countries_b['country'])
    word = request.GET.get('word')
    if word:
        countries = list(filter(lambda name: name[0] == word, countries))
    countries = sorted(countries)
    p = Paginator(countries, 15)
    page_number = request.GET.get('page')
    page_countries = p.get_page(page_number)
    return render(request, 'countries-list.html', {'page_countries': page_countries, 'letters': letters, 'word': word})


def languages(request):
    languages_list = set()
    for lang in data:
        languages_list.update(lang['languages'])

    return render(request, 'languages.html', {'languages': sorted(languages_list)})


def country(request, country_name):
    info_about_country = {}

    for country_info in data:
        if country_info['country'] == country_name:
            info_about_country['country'] = country_info['country']
            info_about_country['languages'] = country_info['languages']
            return render(request, 'countries-page.html', {'country': info_about_country})


def language_in_countries(request, language):
    country_name = []
    for countries in data:
        if language in countries['languages']:
            country_name.append(countries['country'])
    country_names = country_name
    return render(request, 'language-use.html', {'country': country_names, 'language': language})


def languages_countries(request, language):
    country_name = []
    for countries in data:
        if language in countries['languages']:
            country_name.append(countries['country'])
    country_names = country_name
    return render(request, 'language-use.html', {'country': country_names, 'language': language})

