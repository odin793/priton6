from models import Person, Phrase, Comics 
from django.views.decorators.cache import cache_page 
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from random import sample
from annoying.decorators import render_to
        
def main_redirect(request):
    return redirect('/patients/')   # main page


def simple_render(request, template, dict):
    return render_to_response(template, RequestContext(request, dict))


#@cache_page(60*15)
@render_to('patients_list.html')
def persons_list(request, page_type):
    is_doctors=False   # by default the page is patients_list
    if page_type == 'doctors':
        is_doctors=True
    random_int = sample(range(1,100), 1)
    persons_list = Person.objects.filter(doctor=is_doctors).order_by('sort')
    phrases_id_list = [obj.id for obj in Phrase.objects.filter(author__doctor=is_doctors)]
    phrases_random_id_list = sample(phrases_id_list, 2)
    random_phrases = Phrase.objects.filter(pk__in=phrases_random_id_list)
    return {
        'persons_list': persons_list,
        'random_phrases': random_phrases,
        'r': random_int,
    }


@cache_page(20)
def bla(request):
    random_int = sample(range(1,100), 1)
    return simple_render(request, 'bla.html', {'r': random_int})


@render_to('comics_list.html')
def comics_list(request):
    comics_list = Comics.objects.order_by('sort')[:2] # dev version
    return {'comics_list': comics_list}


@render_to('single_comics.html')
def comics(request, comics_id):
    comics = get_object_or_404(Comics, id=comics_id)
    prev_comics = Comics.objects.filter(id__lt=comics.id).order_by('-id')
    prev_comics = prev_comics[0] if prev_comics.count() != 0 else comics
    next_comics = Comics.objects.filter(id__gt=comics.id)
    next_comics = next_comics[0] if next_comics.count() != 0 else comics
    
    patients = comics.participants.filter(doctor=False).all()
    patients_blocks = [patients[i:i+3] for i in range(0, len(patients), 3)]
    doctors = comics.participants.filter(doctor=True).all()
    doctors_blocks = [doctors[i:i+3] for i in range(0, len(doctors), 3)]
    essenses = comics.essenses_list.all()
    essenses_blocks = [essenses[i:i+3] for i in range(0, len(essenses), 3)]
    
    return {
        'comics': comics,
        'patients_blocks': patients_blocks,
        'doctors_blocks': doctors_blocks,
        'essenses_blocks': essenses_blocks,
        'prev_comics': prev_comics,
        'next_comics': next_comics,
    }

@render_to('ajax_comics_list.html')
def ajax_comics_loader(request):
    last_page_id = request.POST.get('last_page_id', 'page_1')
    last_comics_id = request.POST.get('last_item_id', 'comics_1')
    last_comics_db_id = int(last_comics_id[-1])
    last_page_id_num = int(last_page_id[-1])
    new_page_id = last_page_id[:-1] + str(last_page_id_num + 1)
    count = request.POST.get('count', 5)
    
    new_comics = Comics.objects.filter(id__gt=last_comics_db_id)[:count]
    return {
        'comics_list': new_comics,
        'new_page_id': new_page_id,
    }
