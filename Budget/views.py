from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import RequestContext
from datetime import datetime, date
from django.core.urlresolvers import reverse
from django.db.models import Sum
import collections
import json, re
from django.contrib.auth.decorators import login_required
from Budget.lib.csv_handler import csv_handler
from Budget.lib.assign_categories import assignCat
from Budget.forms import AccountInputForm
from Budget.models import Transaction, Category, Account
import calendar

import logging
logger = logging.getLogger(__name__)

@login_required
def dashboard(request):

    try:
        T = Transaction.objects.filter(user=request.user).order_by('-date')
        years = T.dates('date', 'year')
        years = years[::-1]
        Tdict = collections.OrderedDict()

        # Go through transactions and order them by year and month
        for y in years:
          # Create balance value for year
          y_int = int(y.strftime("%Y"))
          balY =  T.filter(date__year=y_int).aggregate(Sum('amount'))['amount__sum']
          tmp = collections.OrderedDict()

          Tdict[y] = { 'bal' : balY, 'months': tmp}

          month_list = T.dates('date', 'month').filter(date__year=y_int)
          month_list = month_list[::-1]
          for m in month_list:
            m_int = int(m.strftime("%m"))
            trans = T.filter(date__year=y_int).filter(date__month=m_int)
            tmpBal = trans.aggregate(Sum('amount'))['amount__sum']
            
            Tdict[y]['months'][m] = { 'bal': tmpBal }
        
        # Get accounts out of database
        acc = Account.objects.filter(user=request.user)
        Acc_dict = collections.OrderedDict()
        for a in acc:
            Acc_dict[a.name] = {'id' : a.id, 
                                'bal' : a.balance }

        context = {'trans_list': Tdict,
                   'accounts' : Acc_dict}
        return render(request, 'budget/dashboard.html', context)
    except: 
        return render(request, 'budget/dashboard.html')

def index(request):
    if request.user.is_authenticated():
        return dashboard(request)
    else:
        return redirect('account:login')


@login_required
def getDailyBalance(request):
    T = Transaction.objects.filter(user=request.user)
    T = T.values('date')\
         .annotate(dcount=Sum('amount'))\
         .order_by('-date')

    # Get accounts
    Acc = Account.objects.filter(user=request.user)

    data = []
    count = Acc.aggregate(Sum('balance'))['balance__sum']
    data.append([datetime.now().timestamp()*1000, float(count)])
    for trans in T:
        count -= trans['dcount']
        timestamp = calendar.timegm(trans['date'].timetuple())
        data.append([timestamp*1000, float(count)])

    data.reverse()
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def upload(request):
    if request.method == 'POST':
        # Upload files
        acc = request.POST['sel_acc']
        for _, file in request.FILES.items():
            response = csv_handler(file, request.user, acc)
            return upload_error(request, response)

    else:
        # Get accounts out of database
        acc = Account.objects.filter(user=request.user)
        Acc_dict = collections.OrderedDict()
        for a in acc:
            Acc_dict[a.name] = {'id': a.id,
                                'bal': a.balance,
                                'IBAN': a.IBAN}

        context = {'accounts': Acc_dict}
        return render(request, 'budget/upload.html', context)


@login_required
def upload_error(request, context=None):
    return render(request, 'budget/upload_error.html',
                  context)

@login_required
def getTMonth(request, datestring):
    Date = datetime.strptime(datestring, "%Y-%m")
    Trans = Transaction.objects.filter(user=request.user)
    data = Trans.filter(date__year=str(Date.year)).filter(date__month=str(Date.month)).order_by('-date')
    tmp_json = []
    for T in data:
        formDate = T.date.strftime("%Y-%m-%d")
        tmp_json.append({'Name' : T.opp_name, 'Amount' : float(T.amount), 'CUR' : T.currency, 'Reference' : T.ref, 'Date' : formDate, 'id' : T.pk, 'Category' : T.category,'Comment' : T.comment})

    return HttpResponse(json.dumps(tmp_json))

@login_required
def getTYear(request, datestring):
    Date = datetime.strptime(datestring, "%Y")
    Trans = Transaction.objects.filter(user=request.user)
    data = Trans.filter(date__year=str(Date.year)).order_by('-date')
    tmp_json = []
    for T in data:
        formDate = T.date.strftime("%Y-%m-%d")
        tmp_json.append({'Name' : T.opp_name, 'Amount' : float(T.amount), 'CUR' : T.currency, 'Reference' : T.ref, 'Date' : formDate,  'id' : T.pk , 'Category' : T.category,'Comment' : T.comment})

    return HttpResponse(json.dumps(tmp_json))

@login_required
def getTransaction(request, field, fieldvalue):
    Trans = Transaction.objects.filter(user=request.user)

    if field == 'year':
        Date = datetime.strptime(fieldvalue, "%Y")
        data = Trans.filter(date__year=str(Date.year))
    elif field == 'month':
        Date = datetime.strptime(fieldvalue, "%Y-%m")
        data = Trans.filter(date__year=str(Date.year)).filter(date__month=str(Date.month))
    elif field == 'range':
        ranges = fieldvalue.split("-")
        startDate = datetime.utcfromtimestamp(float(ranges[0]))
        endDate = datetime.utcfromtimestamp(float(ranges[1]))
        data = Trans.filter(date__range=[startDate, endDate])
    else:
        kwargs = { field : fieldvalue }
        data = Trans.filter(**kwargs)

    data = data.order_by('-date')
    tmp_json = []
    for T in data:
        tmp_json.append({'Name' : T.opp_name,#
                        'Amount' : float(T.amount),#
                        'CUR' : T.currency, #
                        'Reference' : T.ref, #
                        'Date' : T.date.strftime("%Y-%m-%d"),#
                        'id' : T.pk , #
                        'Category' : T.category,#
                        'Comment' : T.comment})

    return HttpResponse(json.dumps(tmp_json))

@login_required
def getTransaction2(request, field, fieldvalue,datevalue):
    Trans = Transaction.objects.filter(user=request.user)
    if len(datevalue) ==  4:
        Date = datetime.strptime(datevalue, "%Y")
        data = Trans.filter(date__year=str(Date.year))
    else:
        Date = datetime.strptime(datevalue, "%Y-%m")
        data = Trans.filter(date__year=str(Date.year)).filter(date__month=str(Date.month))

    kwargs = { field : fieldvalue }
    data = data.filter(**kwargs)

    data = data.order_by('-date')
    tmp_json = []
    for T in data:
        tmp_json.append({'Name' : T.opp_name,#
                        'Amount' : float(T.amount),#
                        'CUR' : T.currency, #
                        'Reference' : T.ref, #
                        'Date' : T.date.strftime("%Y-%m-%d"),#
                        'id' : T.pk , #
                        'Category' : T.category,#
                        'Comment' : T.comment})

    return HttpResponse(json.dumps(tmp_json))



@login_required
def changeT(request):
    R = request.POST
    # Check if new post
    regexp = re.compile(r'jqg\d+')
    # Change or delete existing entry
    if regexp.search(R['id']) is None:
        T = get_object_or_404(Transaction, pk=R['id'])
        if R['oper'] == 'del':
            T.delete()
            return HttpResponseRedirect(reverse('budget:index'))
    # Add new one
    else:
        T = Transaction.objects.create()

    T.date = datetime.strptime(R['Date'], '%Y-%m-%d')
    T.currency = R['CUR']
    T.opp_name = R['Name']
    T.ref = R['Reference']
    T.amount = R['Amount']
    T.category = R['Category']
    T.comment = R['Comment']
    T.save()
    return HttpResponseRedirect(reverse('budget:dashboard'))


@login_required
def getCategories(request):
    cats = Category.objects.filter(user=request.user).order_by('category')    
    
    CatDict = []
    for cat in cats:
        regs = cat.getReg()
        CatDict.append({'category': cat.category, 'regexp': regs, 'id': cat.pk })
    
    return HttpResponse(json.dumps(CatDict))

@login_required
def showCategories(request): 
    return render(request, 'budget/categories.html')

@login_required
def changeCategory(request):
    R = request.POST
    # Check if entry already exists
    regexp = re.compile(r'jqg\d+') # This is the format jqgrid returns values if
                                   # none is inserted
    if regexp.search(R['id']) is None:
        Cat = get_object_or_404(Category, pk=R['id'])
        # Check if the change is a delete
        if R['oper'] == 'del':
            Cat.delete()
            return redirect('budget:categories')

    else:
        Cat = Category.objects.create(user=request.user)

    
    Cat.category = R['category']
    Cat.setReg(R['regexp'].split(','))
    Cat.save()
    return redirect('budget:categories')

@login_required
def assignCategories(request):
    assignCat(request.user)
    return redirect('budget:dashboard')

@login_required
def chart_data_json_date(request, budget_type, datestring):
    data = []
    # Query transactions for user
    T = Transaction.objects.filter(user=request.user)

    # Check if datestring is year or year-month
    if len(datestring)==4:
        T = T.filter(date__year=datestring)
    elif len(datestring)==7:
        Date = datetime.strptime(datestring, "%Y-%m")
        T = T.filter(date__year=str(Date.year), date__month=str(Date.month))
    elif len(datestring) >= 15:
        ranges = datestring.split('-')
        startDate = datetime.utcfromtimestamp(float(ranges[0]))
        endDate = datetime.utcfromtimestamp(float(ranges[1]))
        T = T.filter(date__range=[startDate, endDate])
    # Check for Einnahmen
    if budget_type == 'Einnahmen':
        T = T.filter(amount__gte=0).values('category').annotate(dcount=Sum('amount'))
    
    elif budget_type == 'Ausgaben':
        T = T.filter(amount__lte=0).values('category').annotate(dcount=Sum('amount'))
    else:
        T = T.values('category').annotate(dcount=Sum('amount'))
    
    for trans in T:
        data.append([trans['category'], abs(float(trans['dcount']))])

    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def chart_data_json(request, budget_type):
    data = []
    # Query transactions for user
    T = Transaction.objects.filter(user=request.user)
    
    # Check for einnahmen
    if budget_type == 'Einnahmen':
        T = T.filter(amount__gte=0).values('category').annotate(dcount=Sum('amount'))
    
    elif budget_type == 'Ausgaben':
        T = T.filter(amount__lte=0).values('category').annotate(dcount=Sum('amount'))
    else:
        T = T.values('category').annotate(dcount=Sum('amount'))
    
    for trans in T:
        data.append([trans['category'], abs(float(trans['dcount']))])

    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def showCharts(request): 
    return render(request, 'budget/charts.html')

@login_required
def getAccounts(request):
    """ List all accounts and the possibility to create a new account """
    # Check for POST
    if request.method == 'POST':
        form = AccountInputForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()

            return HttpResponseRedirect(reverse('budget:accounts'))
    accs = Account.objects.filter(user=request.user)
    accs.order_by('name')

    accList = []
    for acc in accs:
        accList.append({'name':acc.name, 'IBAN':acc.IBAN, 
                        'description':acc.description, 'balance':acc.balance})
    
    form = AccountInputForm()
    context = {'account_list': accList, 'form' : form}
    return render(request, 'budget/accounts.html', context)

@login_required
def change_balance(request):
    acc_id = request.GET['account_id']
    acc_bal = request.GET['account_bal']
    
    account = get_object_or_404(Account, pk = acc_id)
    account.balance = float(acc_bal)
    account.save()
    return HttpResponse(acc_bal)


## DEBUG
@login_required
def plotDailyBalance(request):
    return render(request, 'budget/daily_plot.html')
