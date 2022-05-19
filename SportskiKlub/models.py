from django.db import models

class Group(models.Model):
    groupId = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)

class Term(models.Model):
    termId = models.CharField(max_length=200, primary_key=True)
    day = models.CharField(max_length=200)
    time = models.CharField(max_length=200)

class Coach(models.Model):
    coachId = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    groups = models.ManyToManyField('Group', related_name='groups')

class Location(models.Model):
    locationId = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    adress = models.CharField(max_length=200)

