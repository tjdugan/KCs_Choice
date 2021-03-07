from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm
import random

# Helper functions------------------------------------------
#-----------------------------------------------------------

# Simple function that takes a comma-seperated
# string argument and returns a list 
def parse_to_array(csv):
    return_list = csv.split(",")
    return return_list

# Function takes two arguments. The first argument
# is a list of objects. The second argument is a
# list of integers to be used as pointers for an
# order to arrange the objects (i.e. Ranking objects
# 1 through 10). Function returns the re-ordered
# list of objects  
def arrange_list(the_list, order):
    the_order = []
    initial_list = []
    ordered_list = []
    if len(order) != len(the_list):
        print('ERROR - List Lenghts Do Not Match')
        for i in range(len(the_list)):
            the_order.append(i+1)
    else:
        the_order = order
   
    for l in the_list:
        initial_list.append(l.title)

    for o in the_order:
        ordered_list.append(initial_list[int(o)-1])
    
    return ordered_list

# Simple function that returns a list of 2
# random integers between 1 and length of
# argument
def get_random(objs):
    retry = False
    rand_list = []
    count = len(objs)
    rand_num1 = random.randint(1, count-1)
    rand_num2 = random.randint(1, count-1)

    if rand_num1 == rand_num2:
        retry = True
        while retry:
            rand_num1 = random.randint(0, count-1)
            rand_num2 = random.randint(0, count-1)
            if rand_num1 != rand_num2:
                retry = False
    rand_list.append(objs[rand_num1-1])
    rand_list.append(objs[rand_num2-1])
    return rand_list

# Simple function that returns a subset of full_list
# by indexes stored in objs_to_return (index+1). I wrote this
# helper function for the vote page because I had a hard
# time figuring out how to get the song names to appear 
# based on objs_to_return values using template tags
def get_objects_to_compare(full_list, objs_to_return):
    returned_list = []

    for obj in objs_to_return:
        returned_list.append(full_list[int(obj)-1])

    return returned_list

# This function takes in the randomly-generated options
# that were created prior to POST and compares them to
# the selected option. If the selected object is greater
# than (ranked lower than) the other option, it calls
# the re_order_list function which updated CurrentRatings
# object
def update_current_ratings(opt1, opt2, selected, pointer_list):
    updated_string = convert_to_string(pointer_list)
    
    if int(selected) != int(opt1):
        if int(selected) > int(opt1):
            updated_string = re_order_list(selected, opt1, pointer_list) # reorder list
    else:
        if int(selected) > int(opt2):
            updated_string = re_order_list(selected, opt2, pointer_list) # reorder list
    
    return updated_string

def re_order_list(item_to_update, item_to_move_ahead_of, pointer_list):
    updated_list = []
    item_to_update_index = 0
    item_to_move_ahead_of_index = 0
    
    for i in range(len(pointer_list)):
        if i+1 == int(item_to_update):
            item_to_update_index = i
        if i+1 == int(item_to_move_ahead_of):
            item_to_move_ahead_of_index = i
    
    for p in pointer_list:
        updated_list.append(p)
    updated = updated_list.pop(item_to_update_index)
    updated_list.insert(item_to_move_ahead_of_index, updated)
    
    updated_string = convert_to_string(updated_list)
    return updated_string

# A simple function to convert a list to
# a csv string
def convert_to_string(a_list):
    returned_string = ",".join(a_list)
    return returned_string
    

# Views-----------------------------------------------------
#-----------------------------------------------------------

@login_required(login_url='login')
def home(request):
    item_group = ItemGroup.objects.all()
    context = {'item_group' : item_group}
    return render(request, 'kcs_choice/home.html', context)

@login_required(login_url='login')
def create(request):
    context = {}
    return render(request, 'kcs_choice/create.html', context)

@login_required(login_url='login')
def results(request):
    if request.method == 'POST':
        rated_items = RatedItem.objects.all() #Grab all items. Right now thats okay - only beatles in RatedItems. Will need to filter objects in the future
        curr_rating = CurrentRating.objects.get(pk=1)
        current_rating = parse_to_array(curr_rating.ratingOrder)
        arranged_list = arrange_list(rated_items, current_rating)
        option_1 = request.POST['choices-1']
        option_2 = request.POST['choices-2']
        selected_option = request.POST['item']
        
        curr_rating.ratingOrder = update_current_ratings(option_1, option_2, selected_option, current_rating)
        curr_rating.save()
    context = {'arranged' : arranged_list}
    return render(request, 'kcs_choice/results.html', context)

@login_required(login_url='login')
def vote(request, id=None):
    rated_items = RatedItem.objects.all() #Grab all items. Right now thats okay - only beatles in RatedItems. Will need to filter objects in the future
    curr_rating = CurrentRating.objects.get(pk=1) #Grabs the first object in CurrentRating, which is pointer list to beatles ratings. Wlii need to be dynamic in future
    current_rating = parse_to_array(curr_rating.ratingOrder)
    arranged_list = arrange_list(rated_items, current_rating)
    compare_random = get_random(current_rating)
    objects_to_compare = get_objects_to_compare(arranged_list, compare_random)
    context = {'rated' : rated_items, 
               'current' : current_rating, 
               'arranged' : arranged_list, 
               'compare' : compare_random,
               'compared_objs' : objects_to_compare}

    return render(request, 'kcs_choice/vote.html', context)

@login_required(login_url='login')
def recorded(request):
    context = {}
    return render(request, 'kcs_choice/recorded.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is Incorrect')

    context = {}
    return render(request, 'kcs_choice/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'User ' + user + ' successfully created.')
            return redirect('login')

    context = {'form': form}
    return render(request, 'kcs_choice/register.html', context)