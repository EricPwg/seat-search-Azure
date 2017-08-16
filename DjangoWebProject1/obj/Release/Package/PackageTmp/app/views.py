"""
Definition of views.
"""

LED_NUM = 8

MAP_TOP_OFFSET = 100
LIGHT_SIZE = 50
PICTURE_ZOOM_RATE = 0.25
MAP_WIDTH = 2510
MAP_HEIGHT = 1495

from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django import template
import json
import requests
#from pylab import *
'''
def draw(request):
    plot([1, 2, 3], [8, 6, 7])
    savefig('YA.png')
    return HttpResponse('YA~~')
'''

@csrf_exempt
def led(request):
    input_data = json.loads(request.body)
    f=open('seat_data.txt', 'w')
    
    for i in range(len(input_data)):
        ts = str(i)
        f.write(str(input_data[ts]))
        f.write('\n')
    f.close()
    f=open('seat_data.txt', 'r')
    f = f.readlines()
    d = {}
    for i in range(len(f)):
        t = f[i].split()[0]
        d[i] = t
    #r = json.dumps({'123':1})
    zz = 1
    r = {'123':zz}
    print type(r)
    print r
    return JsonResponse(d)

def seat(request):
    f = open('seat_data.txt', 'r')
    f = f.readlines()

    s = open('seat_locate.txt', 'r')
    s = s.readlines()
    seat_list = []
    for i in range(len(f)):
        if int(f[i].split()[0]) == 1:
            light = 'red'
        else:
            light = 'green'
        st = s[i].split()
        top = int(st[1])*PICTURE_ZOOM_RATE+MAP_TOP_OFFSET-LIGHT_SIZE/2
        left = int(st[0])*PICTURE_ZOOM_RATE-LIGHT_SIZE/2
        t = [light, top, left, LIGHT_SIZE]
        seat_list.append(t)
    return render_to_response('app/seat.html', {'seat_list':seat_list, 'w': MAP_WIDTH*PICTURE_ZOOM_RATE, 'h': MAP_HEIGHT*PICTURE_ZOOM_RATE})

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
 #           'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
#            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    status = requests.get('https://www.google.com', verify=False)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
 #           'year':datetime.now().year,
        }
    )

def test(request):
    print request.GET
    if len(request.GET) == 0:
        pp=0
    else:
        pp=1
    print pp
    return render_to_response('app/table_2.html', {'p1':pp})

def restaurant(request):
    r0 = 100
    r1 = 200
    r2 = 300
    #with open('app/table.html', 'r') as reader:
    #    t = template.Template(reader.read())
    #c = template.Context({'r0':r0, 'r1':r1, 'r2':r2})
    #print c
    #return HttpResponse(t.render(c))
    #r = u'\u9910\u5ef3'
    r = 100
    return render_to_response('app/table.html'.encode('utf-8'), {'r0':r, 'r1':r1, 'r2':r2})

def image(request):
    response = HttpResponse(content_type="image/png")
    img = Image.open(book.png)
    img.save(response,'png')
    return response

def add(request, a, b):
    draw()
    f=open('req.txt', 'a')
    f.write('req\n')
    f.close()
    return HttpResponse(str(int(a)+int(b)))

@csrf_exempt
def messages(request):
    f=open('meg.txt', 'a')
    f.write('meg\n')

    payload = 'grant_type=client_credentials&client_id=441fff01-ae54-4985-beaa-3c0517524d25&client_secret=8BWQfZdZewg3yv4sWBuA5gf&scope=https%3A%2F%2Fapi.botframework.com%2F.default'
    status = requests.post('https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token', verify=True, headers={"Content-Type": "application/x-www-form-urlencoded", "Host" : "login.microsoftonline.com", 'Connection': 'Keep-Alive' }, data = payload)
    print status.json()
    dictt = status.json()
    authtt = dictt['token_type']
    authat = dictt['access_token']

    print 'Step 3'
    authat = authat.encode("ascii", "ignore")
    headers = {"Authorization" : 'Bearer '+authat, "Content-Type": "application/json"}
    response_msg = json.dumps({"header": { "typ" : "JWT", "alg" : "RS256", "x5t" : "EricBotTest", "kid" : "EricBotTest"}, "payload" : { "aud" : "https://api.botframework.com", "iss" : "https://sts.windows.net/d6d49420-f39b-4df7-a1dc-d59a935871db/", "nbf" : 1481049243, "exp" : 1481053143, "appid" : "441fff01-ae54-4985-beaa-3c0517524d25"} , "type" : "message"})
    status = requests.post('https://smba.trafficmanager.net/apis/v3/conversations/12345/activities', headers = headers, data = response_msg)
    print status
    print status.json()
    #print request.body
    #print request.method
    #print type(request.method)
    try:
        input_data = json.loads(request.body)
        f.write(str(input_data)+'\n')
    except ValueError:
        return HttpResponse('qq')
        
    #print input_data
    #print type(input_data)
    
    print input_data['serviceUrl']
    print input_data['from']
    print input_data['recipient']

    data = { 'text' : 'hello' }

    if input_data['type'] == "conversationUpdate":
        f.close()
        return HttpResponse(data)

    serviceUrl = input_data['serviceUrl']
    conversations_id = input_data['conversation']['id']
    conversations = input_data['conversation']
    replyid = input_data['id']
    reply_from = input_data['recipient']
    reply_recipient = input_data['from']
    reply_id = input_data['id']

    f.write('before text\n')
    in_text = input_data['text']
    f.write('after text\n')

    in_split = in_text.split('+')
    if len(in_split) != 2:
        recevied_message = 'Wrong format. format:\"a+b\". a and b are two numbers!!'
    else:
        try:
            a = float(in_split[0])
            b = float(in_split[1])
            recevied_message = str(a+b)
        except ValueError:
            recevied_message = 'Wrong format. format:\"a+b\". a and b are two numbers!!'

    post_message_url = serviceUrl+'/v3/conversations/'+conversations_id+'/activities/'+replyid
    #fbid = json_data['id']
    f.write('before send\n')
    #recevied_message = 'hello!!!'
    f.write(str(post_message_url)+'\n')
    f.write(str(reply_from)+'\n')

    imagelist=[{"contentType": "image/jpg","contentUrl": "http://mydeploy.azurewebsites.net/matsu.jpg","name": "matsu.jpg"}]
    condict = { "text": "What kind of sandwich would you like on your sandwich? ", "buttons": [{"type": "imBack","title": "BLT","value": "1"},{"type": "imBack","title": "Black Forest Ham","value": "2"},{"type": "imBack","title": "Buffalo Chicken","value": "3"}] }
    carddict = { "contentType": "application/vnd.microsoft.card.hero", "content": condict} 
    imagelist.append(carddict)
    response_msg = json.dumps({"text":recevied_message, "type": "message", "from" : reply_from, "conversation":conversations, "recipient":reply_recipient, "replyToId":reply_id, "attachments":imagelist})
    f.write(str(response_msg))
    f.write('after send0\n')
    #status = requests.post(post_message_url,data=response_msg)
    #status = requests.post(post_message_url, auth=('user', 'pass'))
    #print status
    #print status.json()
    headers = {"Authorization" : 'Bearer '+authat, "Content-Type": "application/json"}
    status = requests.post(post_message_url, headers=headers , data=response_msg,verify=False)
    f.write('after send\n')
    #response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}}, "type": "message")
    #status = requests.post(post_message_url,data=response_msg)
    print status
    print status.json()
    f.write(str(status)+'\n')
    ##print status.json()
    f.write('after send1\n')
    f.close()
    return HttpResponse(response_msg)

