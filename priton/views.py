from models import Person, Phrase, Comics 
from django.views.decorators.cache import cache_page 
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from random import sample, shuffle
from annoying.decorators import render_to
from django.core.exceptions import ObjectDoesNotExist
        
def main_redirect(request):
    return redirect('/patients/')   # main page

# random.sample wrap
def my_sample(id_list, seq_len, results=None):
    if id_list == []:
        raise AttributeError('first arg should be non-empty list')
    if results is not None:
        random_id_list = results
    else:
        random_id_list = []
    l = len(id_list)
    if seq_len > l:
        random_id_list += sample(id_list, l)
        seq_len = seq_len - l
        my_sample(id_list, seq_len, random_id_list)
    else:
        random_id_list += sample(id_list, seq_len)
    return random_id_list        

@render_to('patients_list.html')
def persons_list(request, page_type):
    is_doctors=False   # by default the page is patients_list
    if page_type == 'doctors':
        is_doctors=True
    persons_list = Person.objects.filter(doctor=is_doctors).order_by('id')[:10]
    phrases_id_list = [obj.id for obj in Phrase.objects.filter(\
        author__doctor=is_doctors)]
    phrases = Phrase.objects.filter(pk__in=phrases_id_list)
    phrases_list = list(phrases)
    try:
        random_phrases_list = my_sample(phrases_list, persons_list.count())
    except AttributeError:
        random_phrases_list = []
    data_tuple = zip(persons_list, random_phrases_list)
    return {
        'data_tuple': data_tuple,
        'is_doctors': is_doctors,
    }

#@cache_page(20)
#def bla(request):
#    random_int = sample(range(1,100), 1)
#    return simple_render(request, 'bla.html', {'r': random_int})

@render_to('comics_list.html')
def comics_list(request):
    comics_list = Comics.objects.all()[:5]
    return {'comics_list': comics_list}

@render_to('single_comics.html')
def comics(request, comics_id):
    comics = get_object_or_404(Comics, id=comics_id)
    prev_comics = Comics.objects.filter(id__lt=comics.id).order_by('id')
    prev_comics = prev_comics[0] if prev_comics.count() != 0 else 'first'
    next_comics = Comics.objects.filter(id__gt=comics.id)
    next_comics = next_comics[0] if next_comics.count() != 0 else 'last'
    
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
    last_comics_db_id = int(last_comics_id.split('_')[1])
    count = request.POST.get('count', 5)
    
    new_comics = Comics.objects.filter(id__gt=last_comics_db_id).order_by('id')[:count]
    return {
        'comics_list': new_comics,
    }

@render_to('ajax_patients_list.html')
def ajax_patients_loader(request):
    last_page_id = request.POST.get('last_page_id', 'page_1')
    last_person_id = request.POST.get('last_item_id', 'patient_1')
    last_person_db_id = int(last_person_id.split('_')[1])
    try:
        # check type of the last person on the page
        last_person = Person.objects.get(id=last_person_db_id)
        is_doctors = last_person.doctor
        # now we know the page type: patients or doctors.
    except ObjectDoesNotExist:
        is_doctors = False
    count = request.POST.get('count', 10)
    
    new_persons_list = Person.objects.filter(doctor=is_doctors).filter(\
        id__gt=last_person_db_id).order_by('id')[:count]
    phrases_id_list = [obj.id for obj in Phrase.objects.filter(\
        author__doctor=is_doctors)]
    phrases = Phrase.objects.filter(pk__in=phrases_id_list)
    phrases_list = list(phrases)
    random_phrases_list = my_sample(phrases_list, new_persons_list.count())
    data_tuple = zip(new_persons_list, random_phrases_list)
    return {
        'data_tuple': data_tuple,
    }