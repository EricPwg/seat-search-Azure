

from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from restaurant.models import *
import json
import django
import datetime
import time
django.setup()

LED_NUM = GlobalNum.objects.get(name = 'LED_NUM').value

MAP_TOP_OFFSET = GlobalNum.objects.get(name = 'MAP_TOP_OFFSET').value
MAP_LEFT_OFFSET = GlobalNum.objects.get(name = 'MAP_LEFT_OFFSET').value
LIGHT_SIZE = GlobalNum.objects.get(name = 'LIGHT_SIZE').value
PICTURE_ZOOM_RATE = GlobalNum.objects.get(name = 'PICTURE_ZOOM_RATE').value
MAP_WIDTH = GlobalNum.objects.get(name = 'MAP_WIDTH').value
MAP_HEIGHT = GlobalNum.objects.get(name = 'MAP_HEIGHT').value

# Create your views here.

def seat_find_func(data, valid, people):
	print people
	table = int((people-1)/4)+1
	result_list=[]
	result_list_w=[]
	for i in range(len(data)):
		st = str(i+1)
		if valid[st] == False: 
			continue
		thisdata=data[i]
		sl = thisdata['s']
		wl = thisdata['w']
		sresult=[[i+1]]
		for j in range(len(sl)):
			sresult.append([i+1, sl[j]])
		wresult=[[i+1]]
		for j in range(len(wl)):
			wresult.append([i+1, wl[j]])
		sll=len(sresult)
		wll=len(wresult)
#		print sresult, wresult
		while 1:
#			print i+1
#			print sresult, wresult
#			time.sleep(0.5)
			for j in sresult:
				if len(sresult) > 20:
					break
				if len(j) == 0:
					continue
				jt = data[j[-1]-1]
				ssl = jt['s']
				wwl = jt['w']
				if len(ssl) == 0:
					pass
				elif len(ssl) == 1:
					j.append(ssl[0])
				else:
					j.append(ssl[0])
					for k in ssl[1:]:
						r = j[:]
						r.append(k)
						if len(r)>5:
							continue
						sresult.append(r)
				for k in wwl:
					r=j[:]
					r.append(k)
					if wresult.count(r) == 0 and len(r) < 6:
						wresult.append(r)
			for j in wresult:
				if len(wresult) > 30:
					break
				if len(j) == 0:
					continue
				jt = data[j[-1]-1]
				ssl = jt['s']
				if len(ssl) == 0:
					pass
				elif len(ssl) == 1:
					j.append(ssl[0])
				else:
					j.append(ssl[0])
					for k in ssl[1:]:
						r = j[:]
						r.append(k)
						if len(r) > 5:
							continue
						wresult.append(r)
				
			if len(sresult) == sll and len(wresult) == wll:
				break
			else:
				sll = len(sresult)
				wll = len(wresult)
			if len(sresult)>0:
				if len(sresult[0]) > 30:
					break
	
		print 'ff', i+1, sresult, wresult
		time.sleep(0.001)
		print table
		for j in sresult:
			if len(j) == table:
			    result_list.append(j)
		for j in wresult:
			if len(j) == table:
				result_list_w.append(j)

	print 'rrr', result_list, result_list_w
	if len(result_list) > 0:
		return result_list[0]
	elif len(result_list_w) > 0:
		return result_list_w[0]
	else:
		return []

def seat_find(request):
    LED_NUM = GlobalNum.objects.get(name = 'LED_NUM').value
    valid={}
    for i in range(LED_NUM):
        s = Seat.objects.get(no = i+1)
        if s.state == 0:
            valid[str(i+1)] = True
        else:
            valid[str(i+1)] = False

    f=open('data.txt', 'r')
    f=f.readlines()

    data=[]
    for i in range(len(f)):
        g = f[i].split()
        sl=[]
        wl=[]
        flag = True
        for j in range(len(g)-1):
            if valid[str(i+1)] == False:
                break
            if g[j+1] == 'w':
                flag = False
            elif flag:
                if valid[g[j+1]]:
                    sl.append(int(g[j+1]))
            else:
                if valid[g[j+1]]:
                    wl.append(int(g[j+1]))
        dic={}
        dic['no'] = i+1
        dic['w'] = wl
        dic['s'] = sl
        data.append(dic)
    print 'qqq'
    print data
    print valid
    dict = {}
    if len(request.GET) == 0:
        find_result = []
        print find_result
        dict['if_find'] = False
    else:
        dict['if_find'] = True
        print 'eee'
        print request.GET['people']
        people = int(request.GET['people'])
        find_result = seat_find_func(data, valid, int(people))
        dict['find_num'] = people
        if len(find_result) == 0:
            dict['if_not_found'] = True
        else:
            dict['if_not_found'] = False
        print find_result

    check_seat()
    LED_NUM = GlobalNum.objects.get(name = 'LED_NUM').value

    MAP_TOP_OFFSET = GlobalNum.objects.get(name = 'MAP_TOP_OFFSET').value
    MAP_LEFT_OFFSET = GlobalNum.objects.get(name = 'MAP_LEFT_OFFSET').value
    LIGHT_SIZE = GlobalNum.objects.get(name = 'LIGHT_SIZE').value
    PICTURE_ZOOM_RATE = GlobalNum.objects.get(name = 'PICTURE_ZOOM_RATE').value
    MAP_WIDTH = GlobalNum.objects.get(name = 'MAP_WIDTH').value
    MAP_HEIGHT = GlobalNum.objects.get(name = 'MAP_HEIGHT').value
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

    
    dict['if_login'] = if_login

    if if_login:
        dict['point'] = user.point

    f = Seat.objects.all()

    if if_login:
        if user.point < 10:
            dict['if_point'] = False
            dict['ifnot_point'] = True
        else:
            dict['if_point'] = True
            dict['ifnot_point'] = False
    
    find_list=[]

    for i in find_result:
        s = Seat.objects.get(no = i)
        st = [s.x, s.y]
        top = int(st[1])*PICTURE_ZOOM_RATE+MAP_TOP_OFFSET-LIGHT_SIZE
        left = int(st[0])*PICTURE_ZOOM_RATE-LIGHT_SIZE
        find_list.append([top, left, LIGHT_SIZE*2])

    dict['find_list'] = find_list

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
    dict['LIGHT_SIZE'] = LIGHT_SIZE
    return render(request, 'app/seat_search.html', dict)




def check_seat():
    waitdata = Waiting.objects.filter(is_restaurant = False)
    print waitdata
    now = time.time()
    for i in waitdata:
        if i.if_action == False:
            continue
        print now, i.reserve_time, GlobalNum.objects.get(name = 'SEAT_MAX_TIME_SEC').value
        if int(now) - i.reserve_time > GlobalNum.objects.get(name = 'SEAT_MAX_TIME_SEC').value:
            user = i.user_set.all()[0]
            s = i.seat
            s.state = 0
            s.save()
            if len(user.reserve.all()) == 1:
                st = Seat.objects.get(no = -1)
                wt = Waiting.objects.filter(seat = st).filter(is_restaurant = False)
                user.if_reserve = False
                user.reserve.add(wt[0])
                user.reserve.remove(i)
                user.save()
            else:
                user.reserve.remove(i)
                user.save()
            i.delete()
    return HttpResponse('OK')


def floortrans(a):
    if a>0:
        return str(a)+'F'
    else:
        return 'B'+str(-a)+'F'

def restaurant(request):
    check_seat()
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
        if i.floor == 0:
            continue
        d['name'] = i.name
        waitingnumberlist = i.waiting_set.filter(if_action = True)
        d['waiting_people'] = len(waitingnumberlist)
        d['current_call'] = i.current_call
        d['if_cannotreserve'] = not(i.resever_valid)
        d['rurl'] = i.url
        if reserved.count(i.id) == 1:
            d['number'] = currentcall_infor[i.id]
            d['if_reserved'] = True
            d['url'] = '/'+request.user.username+'/restaurantcancel/'+str(i.id)
            if d['current_call'] < d['number']:
                if_cancelable = True
            else:
                if_cancelable = False
            print 'qqqww'
            print if_cancelable
            d['if_cancelable'] = if_cancelable
        else:
            d['number'] = '-'
            d['if_reserved'] = False
            d['url'] = '/'+request.user.username+'/handlereserve/'+str(i.id)


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


def stall(request):

    dict = {}

    sdata = Stall.objects.all()
    
    t=[]
    for i in sdata:
        d={}
        if i.floor == 0:
            continue
        d['name'] = i.name
        d['waiting_people'] = i.number_plate - i.current_call
        d['current_call'] = i.current_call
        d['rurl'] = i.url
        t.append(d)

    dict['stall_list'] = t
    dict['title'] = 'Stall'
    return render(request, 'app/stall.html', dict)


def seat(request):
    check_seat()
    LED_NUM = GlobalNum.objects.get(name = 'LED_NUM').value

    MAP_TOP_OFFSET = GlobalNum.objects.get(name = 'MAP_TOP_OFFSET').value
    MAP_LEFT_OFFSET = GlobalNum.objects.get(name = 'MAP_LEFT_OFFSET').value
    LIGHT_SIZE = GlobalNum.objects.get(name = 'LIGHT_SIZE').value
    PICTURE_ZOOM_RATE = GlobalNum.objects.get(name = 'PICTURE_ZOOM_RATE').value
    MAP_WIDTH = GlobalNum.objects.get(name = 'MAP_WIDTH').value
    MAP_HEIGHT = GlobalNum.objects.get(name = 'MAP_HEIGHT').value
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

    if if_login:
        dict['point'] = user.point

    f = Seat.objects.all()

    if if_login:
        if user.point < 10:
            dict['if_point'] = False
            dict['ifnot_point'] = True
        else:
            dict['if_point'] = True
            dict['ifnot_point'] = False

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
    dict['LIGHT_SIZE'] = LIGHT_SIZE
    return render(request, 'app/seat.html', dict)

@csrf_exempt
def led(request):
    check_seat()
    LED_NUM = GlobalNum.objects.get(name = 'LED_NUM').value
    try:
        input_data = json.loads(request.body)

        for i in range(LED_NUM):
            print i+1
            st = str(i+1)
            f = Seat.objects.get(no=i+1)
            if f.state == int(input_data[st]):
                pass
            elif f.state == 2:
                pass
            else:
                f.state = int(input_data[st])
                f.save()
    except:
          pass

    d = {}
    for i in range(LED_NUM):
        print i+1
        f = Seat.objects.get(no=i+1)
        t = f.state
        d[i+1] = t
    #r = json.dumps({'123':1})
    return JsonResponse(d)

def test(request):
    s = Seat.objects.get(no = 0)
    rr = Restaurant.objects.all()[0]
    reserve = Waiting(is_restaurant = False, seat = s, restaurant_waiting_no = 0, restaurant = rr)
    reserve.save()



def personal(request):
    check_seat()
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
                url = '/'+username+'/restaurantcancel/'+str(i.restaurant.id)
                if current < number:
                    if_cancelable = True
                else:
                    if_cancelable = False
                t = [name, floor, current, number, url, if_cancelable]
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
                timestring = i.reserve_time_string
                now = time.time()
                least = int(round((float(now) - float(i.reserve_time))))
                gg = int(GlobalNum.objects.get(name = 'SEAT_MAX_TIME_SEC').value)
                least = gg-least
                print float(now) ,  float(i.reserve_time)
                t = [no, url, timestring, least]
                seat_list.append(t)
    else:
        if_seat = False
    dict['seat_list'] = seat_list
    dict['if_seat'] = if_seat
    dict['title'] = 'Personal'

    rehearsal_list=[]
    rehearsallist = user.rehearsal.all()
    if len(rehearsallist) <= 1:
        if_rehearsal = False
    else:
        if_rehearsal = True
        for i in rehearsallist:
            if i.is_restaurant == False:
                continue
            d={}
            d['date'] = i.reserve_time_string
            d['restaurant'] = i.restaurant.name
            rehearsal_list.append(d)

    dict['if_rehearsal'] = if_rehearsal
    dict['rehearsal_list'] = rehearsal_list

    dict['rehearsal_time'] = len(rehearsallist)-1

    return render(request, 'app/personal.html', dict)

def restaurant_admin(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')
    try:
        adminuser = User.objects.get(name = request.user.username)
        print adminuser
    except:
        return HttpResponse('Oops!<br>Invalid user!!')
    if adminuser.if_clerk == False:
        return HttpResponse('Oops!<br>NO authority!!!')

    r = adminuser.managed_restaurant

    if r.resever_valid == False:
        return HttpResponse('Oops!<br>This restaurant cannot reseverd')

    dict={}
    dict['adminuser'] = adminuser.name
    dict['restaurant_name'] = r.name
    
    dict['restaurant_id'] = r.id
    dict['current_call'] = r.current_call

    reserve_list=r.waiting_set.filter(if_action = True)
    numt=0
    for i in reserve_list:
        if i.restaurant_waiting_no > r.current_call:
            numt = numt+1
    dict['waiting_people'] = len(reserve_list)

    reservedatalist=[]
    for i in reserve_list:
        d={}
        d['number'] = i.restaurant_waiting_no
        d['if_online_reserve'] = i.if_online_reserve
        d['reserve_people'] = i.restaurant_reserve_people
        tt = i.user_set.all()
        if len(tt) == 1:
            d['id'] = tt[0]
        if i.restaurant_waiting_no <= r.current_call:
            d['called'] = True
        else:
            d['called'] = False
        reservedatalist.append(d)
        dict['reservedatalist'] = reservedatalist

    return render(request, 'app/restaurantadmin.html', dict)

#def seat_check_overtime(request, seat_no):


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
    now = time.time()
    nowstring = time.strftime("%Y-%m-%d %H:%M:%S")
    reserve = Waiting(if_action = True, is_restaurant = False, if_online_reserve = True, restaurant_waiting_no = 0, restaurant = rr, reserve_time = now, reserve_time_string = nowstring, seat = s)
    reserve.save()
    
    user.point = user.point-10

    if user.if_reserve == False:
        st = user.reserve.all()[0]
        user.reserve.remove(st)
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
        wt = Waiting.objects.filter(seat = st).filter(is_restaurant = False)
        user.if_reserve = False
        user.reserve.add(wt[0])
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
    if len(request.GET) == 0:
        return HttpResponse('Oops!<br>People number did not define!!')
    reserve_people = int(request.GET['reserve_people'][0])

    r.number_plate = r.number_plate+1
    rwn = r.number_plate
    
    ss = Seat.objects.get(no = -1)
    now = time.time()
    nowstring = time.strftime("%Y-%m-%d %H:%M:%S")
    reserve = Waiting(if_action = True, is_restaurant = True, if_online_reserve = True, restaurant_waiting_no = rwn, restaurant_reserve_people = reserve_people,restaurant = r, reserve_time = now, reserve_time_string = nowstring, seat = ss)
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

def handle_reserve(request, name, restaurant_id):
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
    

    if user.point < 10:
        point_error = True
    else:
        point_error = False

    rehearsal = user.rehearsal.all()
    if len(rehearsal) > 3:
        if_rehearsal = True
    else:
        if_rehearsal = False

    url = '/'+str(name)+'/restaurantreserve/'+str(restaurant_id)+'/'
    return render(request, 'app/reservepeople.html', {'url':url, 'restaurant_name':r.name, 'if_rehearsal' : if_rehearsal, 'point_error' : point_error})

def restaurant_call(request, name, restaurant_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')
    try:
        adminuser = User.objects.get(name = request.user.username)
        print adminuser
    except:
        return HttpResponse('Oops!<br>Invalid user!!')
    if adminuser.if_clerk == False:
        return HttpResponse('Oops!<br>NO authority!!!')

    restaurant_id = int(restaurant_id)

    r = adminuser.managed_restaurant
    if r.id != restaurant_id:
        return HttpResponse('Oops!<br>Wrong restaurant ID.<br>NO authority!!!')

    if r.resever_valid == False:
        return HttpResponse('Oops!<br>This restaurant cannot reseverd')

    r.current_call = r.current_call+1
    r.save()
    return HttpResponseRedirect('/restaurantadmin')

def restaurant_site_reserve(request, name, restaurant_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')
    try:
        adminuser = User.objects.get(name = request.user.username)
        print adminuser
    except:
        return HttpResponse('Oops!<br>Invalid user!!')
    if adminuser.if_clerk == False:
        return HttpResponse('Oops!<br>NO authority!!!')

    restaurant_id = int(restaurant_id)

    try:
         r = Restaurant.objects.get(id = restaurant_id)
    except:
        return HttpResponse('Oops!<br>Restaurant id not found!!')

    if r.resever_valid == False:
        return HttpResponse('Oops!<br>This restaurant cannot reseverd')

    if len(request.GET) == 0:
        return HttpResponse('Oops!<br>People number did not define!!')
    reserve_people = int(request.GET['reserve_people'][0])

    r.number_plate = r.number_plate+1
    rwn = r.number_plate
    r.save()
    
    ss = Seat.objects.get(no = -1)
    now = time.time()
    nowstring = time.strftime("%Y-%m-%d %H:%M:%S")
    reserve = Waiting(if_action = True, is_restaurant = True, if_online_reserve = False, restaurant_waiting_no = rwn, restaurant_reserve_people = reserve_people, restaurant = r, reserve_time = now, reserve_time_string = nowstring, seat = ss)
    reserve.save()

    return HttpResponseRedirect('/restaurantadmin')

def restaurant_site_cancel(request, name, restaurant_id, waiting_no):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')
    try:
        adminuser = User.objects.get(name = request.user.username)
        print adminuser
    except:
        return HttpResponse('Oops!<br>Invalid user!!')
    if adminuser.if_clerk == False:
        return HttpResponse('Oops!<br>NO authority!!!')

    restaurant_id = int(restaurant_id)

    try:
         r = Restaurant.objects.get(id = restaurant_id)
    except:
        return HttpResponse('Oops!<br>Restaurant id not found!!')

    if r.resever_valid == False:
        return HttpResponse('Oops!<br>This restaurant cannot reseverd')

    waitdata = r.waiting_set.filter(restaurant_waiting_no = waiting_no)
    if len(waitdata) == 0:
        return HttpResponse('Oops!<br>Reserve number '+str(waiting_no)+' not found!!')
    elif len(waitdata) > 1:
        return HttpResponse('Oops!<br>Found more than one reserve number '+str(waiting_no)+'!!')

    waitdata = waitdata[0]
    waitdata.delete()
    return HttpResponseRedirect('/restaurantadmin')

def restaurant_cancel(request, name, restaurant_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')

    try:
        user = User.objects.get(name = name)
        print user
    except:
        return HttpResponse('Oops!<br>Invalid user!!')

#    if name != user.name:
#        return HttpResponse('Oops!<br>NO authority!!!')

    restaurant_id = int(restaurant_id)

    try:
         r = Restaurant.objects.get(id = restaurant_id)
    except:
        return HttpResponse('Oops!<br>Restaurant id not found!!')

    if r.resever_valid == False:
        return HttpResponse('Oops!<br>This restaurant cannot reseverd')

    restaurantlist = user.reserve.filter(is_restaurant = True)
    print restaurantlist
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

def restaurant_rehearsal(request, name, restaurant_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')

    try:
        adminuser = User.objects.get(name = request.user.username)
        print adminuser
    except:
        return HttpResponse('Oops!<br>Invalid user!!')

    if adminuser.if_clerk == False:
        return HttpResponse('Oops!<br>NO authority!!!')

    restaurant_id = int(restaurant_id)
    user = User.objects.get(name = name)

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

    #move waiting data
    if len(user.reserve.all()) == 1:
        st = Seat.objects.get(no = -1)
        wt = Waiting.objects.filter(seat = st, is_restaurant = False)[0]
        user.if_reserve = False
        user.reserve.add(wt)
        user.reserve.remove(waitdata)
        user.rehearsal.add(waitdata)
        user.save()
    else:
        user.reserve.remove(waitdata)
        user.rehearsal.add(waitdata)
        user.save()

    waitdata.if_action = False
    waitdata.save()

    return HttpResponseRedirect('/restaurantadmin')