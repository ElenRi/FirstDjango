from django.shortcuts import render, HttpResponse
from django.http import HttpResponseNotFound
import json
import string
import sqlite3
from django.core.paginator import Paginator
from MainApp.models import Countries


with open('//country-by-languages.json') as json_file:
    data = json.load(json_file)

# letters = list(string.ascii_uppercase)

countries = {}
countries_alphabetical_list = set()
language_list = []

countries_bd = Countries.objects.all()
for countries_object in countries_bd:
    contry_name = countries_object.country
    letter = contry_name[0]
    countries_alphabetical_list.add(letter)
    countries[contry_name] = []
    languages = countries_object.languages.split(',')
    language_list.extend(languages)
    countries[countries_object.country].extend(languages)

language_list.sort()
countries_alphabetical_list.sort()

def main_page(request):
    return render(request, 'index.html')


def countries_list(request):
    page = request.GET.get('page')
    pag = Paginator(list(countries.keys()), 10)
    page_obj = pag.get_page(page)
    context = {
        "page": page,
        "page_obj": page_obj,
        'countries_alphabetical_list': countries_alphabetical_list,
    }
    return render(request, 'countries-list.html', context)


def country_page(request, country: str):
    languages = countries[country]
    context = {
        'country': country,
        'languages': languages
    }
    return render(request, 'countries-page.html', context)


def countries_letter(request, letter: str):
    countries_list = []

    for country in countries:
        if country.startswith(letter):
            countries_list.append(country)

    context = {
        'letter': letter,
        'countries_list': countries_list
    }
    return render(request, 'countries-lettr.html', context)


def language_page(request):
    context = {
        'language_list': language_list
    }
    return render(request, 'languages.html', context)


def language_use(request, language:str):
    countries_list = list()
    for country in countries:
        if countries[country].count(language) > 0:
            countries_list.append(country)
        countries_list.sort()

    context = {
        'language': language,
        'countries_list': countries_list
    }
    return render(request, 'language_use.html', context)


