#from vue_film_times import vue_film_list
import time
from datetime import datetime, timedelta
import re

film1_dict = {'Title':'Peter Rabbit 2', 'Film length':'1hr 33min', 'Times':['13:00','15:00','15:30','16:45','17:00']}# vue_film_list
film2_dict = {'Title':'Godzilla', 'Film length':'2hr 3min', 'Times':['13:15','15:15','15:30','16:45','17:40']}
film3_dict = {'Title':'Stuff 4', 'Film length':'1hr 21min', 'Times':['13:30','15:30','15:30','16:40','17:20']}

film_list = [film1_dict, film2_dict, film3_dict]

def convert_time(time_string):
    time_var = datetime.strptime(time_string, '%H:%M')
    return time_var




def add_time_obj(film_time_list, orig_dict):
    new_dict = {'Converted Times': []}
    for film_time in film_time_list:
        time_obj = convert_time(film_time)
        new_dict['Converted Times'].append(time_obj)
    return orig_dict.update(new_dict)




def convert_duration_vue(film_dict, film_length):
    hour_length = re.findall(r"(\d+)hr", film_length)
    hour_length = int(hour_length[0])*60
    min_length = re.findall(r"(\d+)min", film_length)
    film_dur = hour_length + int(min_length[0])
    film_dur = int(film_dur)
    return update_film_length_int(film_dur, film_dict)

def update_film_length_int(length_int, orig_dict):
    orig_dict['Film length'] = length_int
    return orig_dict




def add_startfin(film_dict):
    film_dict.update({'start_fin': []})
    for film_time in film_dict['Converted Times']:
        film_dur_dict = {'start': [], 'finish': []}
        film_dur_dict['start'] = film_time
        finish_time = film_time + timedelta(minutes=film_dict['Film length'])
        film_dur_dict['finish'] = finish_time # Works to add finish times!!
        film_dict['start_fin'].append([film_time, film_dur_dict]) # Complex data structures here, can I neaten up?
    return film_dict


for film in film_list:
    add_time_obj(film['Times'], film)
    convert_duration_vue(film ,film['Film length'])
    add_startfin(film)



def calculate_watch_list(film_profile_list):
    film_range = len(film_profile_list)
    film_1 = film_profile_list[0]['Converted Times'][0]
    f1finish_time = film_1 + timedelta(minutes=film_profile_list[0]['Film length'])
    for f_times in film_profile_list[1]['Converted Times']:
        if f1finish_time > f_times:
            continue
        else:
            film_2 = f_times
            f2_finish_time = film_2 + timedelta(minutes=film_profile_list[1]['Film length'])
            for f2_time in film_profile_list[2]['Converted Times']:
                if f2_finish_time > f2_time:
                    continue
                else:
                    film_3 = f2_time
                    print(f'Film 1 {film_profile_list[0]["Title"]} at {film_1.strftime("%H:%M")}')
                    print(f'Film 2 {film_profile_list[1]["Title"]} at {film_2.strftime("%H:%M")}')
                    print(f'Film 3 {film_profile_list[2]["Title"]} at {film_3.strftime("%H:%M")}')
                    break
            break

calculate_watch_list(film_list)



def watch_list(films_to_watch): # Needs to be simplified and has type error, see below
    first_film = films_to_watch[0]
    second_film = films_to_watch[1]
    third_film = films_to_watch[2]

    first_film_startfin = first_film.get('start_fin')[0]
    first_film_finish = first_film_startfin[1]['finish']
    first_film_start = first_film_startfin[1]['start']

    second_film_times = second_film.get('start_fin')
    third_film_times = third_film.get('start_fin')

    for film_time in second_film_times:
        if first_film_finish > film_time[1]['start']:
            continue
        else:
            second_film_time = {second_film.get('Title'): film_time[0].strftime("%H:%M")}
            second_film_finish = film_time[1]['finish']
            for film2_time in third_film_times:
                if second_film_finish > film2_time[1]['start']: # Type error here for sting indice neds to interger?
                    continue
                else:
                    third_film_times = {third_film.get('Title'): film2_time[0].strftime("%H:%M")}
                    print(f'first watch {first_film.get("Title")} at {first_film_start.strftime("%H:%M")}')
                    print(f'then watch {second_film_time}, then {third_film_times}')
                    break


