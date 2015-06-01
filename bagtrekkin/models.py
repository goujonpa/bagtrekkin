# from datetime import timedelta, datetime

# from django.contrib.auth.models import User
# from django.db import models
# from tastypie.models import create_api_key


# class Compagny(models.Model):
#     name = models.CharField(max_length=64)

#     def __unicode__(self):
#         return unicode('%s' % self.name)


# class Employee(models.Model):
#     FUNCTION_CHOICES = (
#         ('checkin', 'Check-In'),
#     )

#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('active', 'Active'),
#         ('blocked', 'Blocked'),
#     )
#     fullname = models.CharField(max_length=64)
#     district = models.CharField(max_length=64)
#     token = models.CharField(max_length=255)
#     status = models.CharField(max_length=32, choices=STATUS_CHOICES)
#     function = models.CharField(max_length=32, choices=FUNCTION_CHOICES)
#     company = models.ForeignKey(Compagny)
#     user = models.ForeignKey(User)

#     def __unicode__(self):
#         return unicode('%s <%s>' % (self.fullname, self.company))


# class Passenger(models.Model):
#     GENDER_CHOICES = (
#         ('m', 'M'),
#         ('f', 'F')
#     )
#     email = models.CharField(max_length=255, unique=True)
#     firstname = models.CharField(max_length=64)
#     lastname = models.CharField(max_length=64)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#     pnr = models.CharField(max_length=6, unique=True)
#     tel = models.CharField(max_length=20)

#     def __unicode__(self):
#         return unicode('%s <%s>' % (self.fullname, self.email))

#     @property
#     def fullname(self):
#         return '%s %s %s' % (self.gender, self.firstname, self.lastname)


# class Eticket(models.Model):
#     ticket_number = models.CharField(max_length=14, unique=True)
#     summary = models.CharField(max_length=64)
#     passenger = models.ForeignKey(Passenger)

#     def __unicode__(self):
#         return unicode('%s <%s>' % (self.passenger, self.eticket))


# class Flight(models.Model):
#     airline = models.CharField(max_length=6)
#     aircraft = models.CharField(max_length=64)
#     departure_loc = models.CharField(max_length=255)
#     departure_time = models.TimeField()
#     arrival_loc = models.CharField(max_length=255)
#     arrival_time = models.TimeField()
#     flight_date = models.DateField()
#     duration = models.TimeField()
#     eticket = models.ForeignKey(Eticket)
#     company = models.ForeignKey(Compagny)

#     def __unicode__(self):
#         return unicode('%s <%s - %s>' % (self.eticket, self.airline, self.company))


# class Material(models.Model):
#     material_number = models.CharField(max_length=16)
#     datetime = models.DateTimeField(auto_now_add=True)
#     is_already_read = models.BooleanField(default=False)

#     def __unicode__(self):
#         return unicode('%s <%s>' % (self.material_number, self.datetime.strftime('%d, %b %Y @ %H:%m')))

#     def save(self):
#         '''Fetch materials since one hour with the given material number'''
#         materials = Materials.objects.filter(
#             datetime__gte=datetime.now()-timedelta(hours=1),
#             material_number=self.material_number
#         )
#         if not materials:
#             super(Material, self).save()

#     def get_unreads():
#         '''Fetch all unread materials ordered by dateime DESC'''
#         return Materials.objects.filter(
#             is_already_read=False
#         ).order_by('-datetime')


# class Luggage(models.Model):
#     material = models.ForeignKey(Material)
#     passenger = models.ForeignKey(Passenger)

#     def __unicode__(self):
#         return unicode('%s <%s>' % (self.passenger, self.material))


# class Log(models.Model):
#     horodator = models.DateTimeField(auto_now_add=True)
#     localisation = models.CharField(max_length=255)
#     employee = models.ForeignKey(Employee)
#     luggage = models.ForeignKey(Luggage)
#     flight = models.ForeignKey(Flight)

#     def save(self):
#         '''Add employee district as default localisation'''
#         if not self.localisation:
#             self.localisation = self.employee.district
#             super(Log, self).save()


# def create_employee(sender, instance, created, **kwargs):
#     profile = Employee()
#     profile.user = instance
#     profile.save()


# models.signals.post_save.connect(create_employee, sender=User)
# models.signals.post_save.connect(create_api_key, sender=User)
