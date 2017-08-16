LED_NUM = 8

MAP_TOP_OFFSET = 150
MAP_LEFT_OFFSET = 0
LIGHT_SIZE = 50
PICTURE_ZOOM_RATE = 0.25
MAP_WIDTH = 2510
MAP_HEIGHT = 1495

from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from restaurant.models import *
import json
import django
django.setup()

# Create your views here.

def floortrans(a):
    if a>0:
        return str(a)+'F'
    else:
        return 'B'+str(-a)+'F'

def restaurant(request):
    reserved=[]
    currentcall_infor={}
    if_login = False
    if request.user.is_authenticated():
        if_login = True
        user = User.objects.get(name = request.user.username)
        restaurantlist = user.reserve.filter(is_restaurant = True)
        if len(restaurantlist) > 0:
            for i in restaurantlist:
                tt = i.restaurant.id
                reserved.append(tt)
                currentcall_infor[i.restaurant.id] = i.restaurant_waiting_no

    dict = {}
    dict['if_login'] = if_login

    floor_list = []
    rdata = Restaurant.objects.order_by('floor')
    
    t=[]
    for i in rdata:
        d={}
        thisfloor = i.floor
        d['name'] = i.name
        d['waiting_people'] = i.number_plate - i.current_call
        d['current_call'] = i.current_call
        d['if_cannotreserve'] = not(i.resever_valid)
        if reserved.count(i.id) == 1:
            d['number'] = currentcall_infor[i.id]
            d['if_reserved'] = True
            d['url'] = '/'+request.user.username+'/restaurantcheckin/'+str(i.id)
        else:
            d['number'] = '-'
            d['if_reserved'] = False
            d['url'] = '/'+request.user.username+'/restaurantreserve/'+str(i.id)


        if len(t) == 0:
            t.append(floortrans(i.floor))
            t.append([d])
        elif t[0] != floortrans(i.floor):
            floor_list.append(t)
            t=[]
            t.append(floortrans(i.floor))
            t.append([d])
        else:
            t[1].append(d)

    floor_list.append(t)
    print floor_list
    dict['floor_list'] = floor_list
    dict['title'] = 'Restaurant'
    print request.path_info
    return render(request, 'app/restaurant.html', dict)


def seat(request):
    reserved=[]
    if_login = False
    if request.user.is_authenticated():
        if_login = True
        user = User.objects.get(name = request.user.username)
        seatlist = user.reserve.filter(is_restaurant = False)
        if len(seatlist) > 0:
            for i in seatlist:
                tt = i.seat.no
                reserved.append(tt)

    dict = {}
    dict['if_login'] = if_login

    f = Seat.objects.all()

    seat_list = []
    for i in f:
        if_unlockable = False
        if i.no == -1:
            continue
        elif reserved.count(i.no) == 1:
            light = 'pink'
            if_unlockable = True
        elif int(i.state) == 1:
            light = 'red'
        elif int(i.state) == 2:
            light = 'blue'
        else:
            light = 'green'
        st = [i.x, i.y]
        top = int(st[1])*PICTURE_ZOOM_RATE+MAP_TOP_OFFSET-LIGHT_SIZE/2
        left = int(st[0])*PICTURE_ZOOM_RATE-LIGHT_SIZE/2
        if if_login and light == 'green':
            if_reserveable = True
        else:
            if_reserveable = False
        t = [light, top, left, LIGHT_SIZE, if_reserveable, i.no, if_unlockable]
        seat_list.append(t)
    
    if request.user.is_authenticated():
        user_name = request.user.username
    else:
        user_name = 'NULL'
    
    dict['seat_list'] = seat_list
    dict['w'] = MAP_WIDTH*PICTURE_ZOOM_RATE
    dict['h'] = MAP_HEIGHT*PICTURE_ZOOM_RATE
    dict['users'] = user_name
    dict['top_offset'] = MAP_TOP_OFFSET
    dict['left_offset'] = MAP_LEFT_OFFSET
    dict['title'] = 'Seat'
    return render(request, 'app/seat.html', dict)

@csrf_exempt
def led(request):
    try:
        input_data = json.loads(request.body)

        for i in range(LED_NUM):
            st = str(i)
            f = Seat.objects.get(no=i)
            if f.state == int(input_data[st]):
                pass
            else:
                f.state = int(input_data[st])
                f.save()
    except:
          pass

    d = {}
    for i in range(LED_NUM):
        f = Seat.objects.get(no=i)
        t = f.state
        d[i] = t
    #r = json.dumps({'123':1})
    return JsonResponse(d)

def test(request):
    s = Seat.objects.get(no = 0)
    rr = Restaurant.objects.all()[0]
    reserve = Waiting(is_restaurant = False, seat = s, restaurant_waiting_no = 0, restaurant = rr)
    reserve.save()



def personal(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')
    try:
        user = User.objects.get(name = request.user.username)
    except:
        return HttpResponse('Oops!<br>NO authority!!')

    username = user.name
    point = user.point
    dict = {'username':username, 'point':point}

    restaurant_list = []
    if user.if_reserve:
        restaurantlist = user.reserve.filter(is_restaurant = True)
        if len(restaurantlist) == 0:
            if_restaurant = False
        else:
            for i in restaurantlist:
                if_restaurant = True
                name = i.restaurant.name
                floor = floortrans(i.restaurant.floor)
                current = i.restaurant.current_call
                number = i.restaurant_waiting_no
                url = '/'+username+'/restaurantcheckin/'+str(i.restaurant.id)
                t = [name, floor, current, number, url]
                restaurant_list.append(t)
    else:
        if_restaurant = False
    dict['restaurant_list'] = restaurant_list
    dict['if_restaurant'] = if_restaurant

    seat_list=[]
    if user.if_reserve:
        seatlist = user.reserve.filter(is_restaurant = False)
        if len(seatlist) == 0:
            if_seat = False
        else:
            for i in seatlist:
                if_seat = True
                no = i.seat.no
                url = '/'+username+'/seatunlock/'+str(no)
                t = [no, url]
                seat_list.append(t)
    else:
        if_seat = False
    dict['seat_list'] = seat_list
    dict['if_seat'] = if_seat
    dict['title'] = 'Personal'
    return render(request, 'app/personal.html', dict)



def seat_reserve(request, name, seat_no):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')

    try:
        user = User.objects.get(name = request.user.username)
    except:
        return HttpResponse('Oops!<br>NO authority!!')

    if name != user.name:
        return HttpResponse('Oops!<br>NO authority!!')

    seat_no = int(seat_no)

    try:
        s = Seat.objects.get(no = seat_no)
    except:
        return HttpResponse('Oops!<br>Seat ID out of range!!')

    print s.waiting_set.all()
    if len(s.waiting_set.all()) > 0:
        return HttpResponse('Oops!<br>Seat ID'+str(seat_no)+'is already reserved.')
    elif s.state == 1:
        return HttpResponse('Oops!<br>Seat ID '+str(seat_no)+' is occupied.')
    elif s.state == 2:
        return HttpResponse('Oops!<br>Seat ID '+str(seat_no)+' is already reserved.<br>state error')

    rr = Restaurant.objects.all()[0]
    reserve = Waiting(is_restaurant = False, seat = s, restaurant_waiting_no = 0, restaurant = rr)
    reserve.save()
    
    if user.if_reserve == False:
        print 'helloooo'
        st = user.reserve.all()[0]
        user.reserve.remove(st)
        print 'helloooo'
        user.if_reserve = True;
        user.reserve.add(reserve)
        user.save()
    else:
        user.reserve.add(reserve)
        user.save()

    s.state = 2
    s.save()

    return HttpResponseRedirect('/personal')

def seat_unlock(request, name, seat_no):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')

    try:
        user = User.objects.get(name = request.user.username)
    except:
        return HttpResponse('Oops!<br>NO authority!!')

    if name != user.name:
        return HttpResponse('Oops!<br>NO authority!!')

    seat_no = int(seat_no)

    try:
        s = Seat.objects.get(no = seat_no)
    except:
        return HttpResponse('Oops!<br>Seat ID out of range!!')

    seatlist = user.reserve.filter(is_restaurant = False)

    flag = True
    for i in seatlist:
        if i.seat.no == seat_no:
            waitdata = i
            flag = False
            break

    if flag:
        return HttpResponse('Oops!<br>NO resever information!!')

    
    #remove waiting data
    if len(user.reserve.all()) == 1:
        st = Seat.objects.get(no = -1)
        wt = Waiting.objects.filter(seat = st)[0]
        user.if_reserve = False
        user.reserve.add(wt)
        user.reserve.remove(waitdata)
        user.save()
    else:
        user.reserve.remove(waitdata)
        user.save()

    waitdata.delete()

    s.state = 0
    s.save()

    return HttpResponseRedirect('/personal')


def restaurant_reserve(request, name, restaurant_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')

    try:
        user = User.objects.get(name = request.user.username)
        print user
    except:
        return HttpResponse('Oops!<br>Invalid user!!')

    if name != user.name:
        return HttpResponse('Oops!<br>NO authority!!!')

    restaurant_id = int(restaurant_id)

    try:
         r = Restaurant.objects.get(id = restaurant_id)
    except:
        return HttpResponse('Oops!<br>Restaurant id not found!!')

    if r.resever_valid == False:
        return HttpResponse('Oops!<br>This restaurant cannot reseverd')

    ra = user.reserve.all()
    for i in ra:
        if i.is_restaurant and i.restaurant == r:
            return HttpResponse('Oops!<br>You have alreadly reseverd this restaurant.')

    r.number_plate = r.number_plate+1
    rwn = r.number_plate
    

    ss = Seat.objects.get(no = -1)
    reserve = Waiting(is_restaurant = True, seat = ss, restaurant_waiting_no = rwn, restaurant = r)
    reserve.save()

    if user.if_reserve == False:
        st = user.reserve.all()[0]
        user.reserve.remove(st)
        user.if_reserve = True;
        user.reserve.add(reserve)
        user.save()
    else:
        user.reserve.add(reserve)
        user.save()

    r.save()
    return HttpResponseRedirect('/personal')

def restaurant_check_in(request, name, restaurant_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')

    try:
        user = User.objects.get(name = request.user.username)
        print user
    except:
        return HttpResponse('Oops!<br>Invalid user!!')

    if name != user.name:
        return HttpResponse('Oops!<br>NO authority!!!')

    restaurant_id = int(restaurant_id)

    try:
         r = Restaurant.objects.get(id = restaurant_id)
    except:
        return HttpResponse('Oops!<br>Restaurant id not found!!')

    if r.resever_valid == False:
        return HttpResponse('Oops!<br>This restaurant cannot reseverd')

    restaurantlist = user.reserve.filter(is_restaurant = True)

    flag = True
    for i in restaurantlist:
        if i.restaurant == r:
            waitdata = i
            flag = False
            break

    if flag:
        return HttpResponse('Oops!<br>NO resever information!!')

    #remove waiting data
    if len(user.reserve.all()) == 1:
        st = Seat.objects.get(no = -1)
        wt = Waiting.objects.filter(seat = st, is_restaurant = False)[0]
        user.if_reserve = False
        user.reserve.add(wt)
        user.reserve.remove(waitdata)
        user.save()
    else:
        user.reserve.remove(waitdata)
        user.save()

    waitdata.delete()


    return HttpResponseRedirect('/personal')




  