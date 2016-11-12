from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import json
import decimal
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
import django.utils.timezone

class Category(models.Model):
    category = models.CharField(max_length=20)
    regexp = models.CharField(max_length=400, default='')
    user = models.ForeignKey(User)

    def setReg(self, x):
        self.regexp = json.dumps(x)

    def getReg(self):
        return json.loads(self.regexp)

    def __str__(self):
        return self.category

class Account(models.Model):
    IBAN = models.CharField(max_length=34, default='XY12123412341234123412')
    name = models.CharField(max_length=50, default='Bank XY')
    description = models.CharField(max_length=200, default='Main Girokonto')
    user = models.ForeignKey(User)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default = 0)

    def __str__(self):
        return self.IBAN

class Transaction(models.Model):
    user = models.ForeignKey(User)
    account = models.ForeignKey(Account)
    date = models.DateField(default=django.utils.timezone.now())
    ref = models.CharField(max_length=200, default='Reference')
    opp_name = models.CharField(max_length=80, default='Unknown')
    opp_account = models.CharField(max_length=26, default= '----')
    amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    currency = models.CharField(max_length=20, default= 'EUR')
    category = models.CharField(max_length=50, default='Unknown')
    comment = models.CharField(max_length=100, default='')
	
