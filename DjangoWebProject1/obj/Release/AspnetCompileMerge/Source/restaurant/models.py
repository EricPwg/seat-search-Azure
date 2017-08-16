from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length = 50)
    floor = models.DecimalField(max_digits = 3, decimal_places = 0, default = -3)
    number_plate = models.DecimalField(max_digits = 5, decimal_places = 0)
    current_call = models.DecimalField(max_digits = 5, decimal_places = 0, default = 0)
    resever_valid = models.BooleanField(default = False)

    def __unicode__(self):
        t = str(self.current_call)
        return 'restarrant: '+self.name+': '+t

class Seat(models.Model):
    no = models.DecimalField(max_digits = 2, decimal_places = 0)
    state = models.DecimalField(max_digits = 1, decimal_places = 0)
    x = models.DecimalField(max_digits = 5, decimal_places = 0)
    y = models.DecimalField(max_digits = 5, decimal_places = 0)
#    tt = models.ForeignKey(Restaurant, default='')

    def __unicode__(self):
        t = str(self.state)
        return 'seat: '+str(self.no)+': '+t


class Waiting(models.Model):
    is_restaurant = models.BooleanField(default = False)
    restaurant_waiting_no = models.DecimalField(max_digits = 2, decimal_places = 0)
    restaurant = models.ForeignKey(Restaurant, default='')
    seat = models.ForeignKey(Seat, default='')

    def __unicode__(self):
        if self.is_restaurant:
            rt = 'RE_restaurant'
            st = self.restaurant.name
        else:
            rt = 'RE_seat'
            st = self.seat.no

        return str(rt)+' '+str(st)
            


class User(models.Model):
    name = models.CharField(max_length = 50)
    point = models.DecimalField(max_digits = 10, decimal_places = 0, default = 100)
    if_reserve = models.BooleanField(default = False)
    reserve = models.ManyToManyField(Waiting, default='')

    def __unicode__(self):
        return self.name


class GlobalNum(models.Model):
    name = models.CharField(max_length = 50)
    value = models.DecimalField(max_digits = 20, decimal_places = 10)

    def __unicode__(self):
        return self.name+': '+str(self.value)

