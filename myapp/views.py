from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sqlite3

import json
import requests
from myapp.models import Jar,Transaction
from datetime import datetime

@csrf_exempt
def post_jar(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        name = body["name"]
        cash = body["cash"]
        availableCurrencies = ['EUR', 'PLN', 'USD']
        currency = body["currency"]
        if currency in availableCurrencies:
            newJar = Jar(name=name,
                        cash=cash,
                        currency=currency)
            newJar.save()
            newTransaction = Transaction(jar=newJar,
                                         cash=cash,
                                         date=datetime.now(),
                                         name='Jar created')
            newTransaction.save()
            return HttpResponse([{'Jar was added to the database'}], content_type='text / json')
        else:
            return HttpResponse([{'Use on of those currencies: PLN USD EUR'}], content_type='text / json')

@csrf_exempt
def get_jars(request):
    if request.method == "GET":
        queryset = Jar.objects.all()
        result = []
        for obj in queryset:
            result.append({"id":obj.id, "name" : obj.name,  "cash" : obj.cash, "currency" : obj.currency})
        json_stuff = json.dumps({"jar_list": result})
        if result:
            return HttpResponse(json_stuff, content_type='text/json')
        else:
            return HttpResponse([{'There are no jars in the database'}], content_type='text / json')

@csrf_exempt
def withdraw(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body["id"]
        cash = body["cash"]
        queryset = Jar.objects.filter(id=id)
        if queryset:
            currentCash = Jar.objects.filter(id=id)[0].cash
            if currentCash > cash:
                Jar.objects.filter(id=id).update(cash=currentCash - cash)
                newTransaction= Transaction(jar=Jar.objects.filter(id=id)[0],
                             cash=cash,
                             date=datetime.now(),
                            name='Withdraw')
                newTransaction.save()
                return HttpResponse({'Withdraw succeeded'}, content_type='text/json')
            else:
                return HttpResponse({'Not enough cash in the Jar'}, content_type='text/json')
        else:
            return HttpResponse({'There is no jar with that id'}, content_type='text/json')

@csrf_exempt
def cashin(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body["id"]
        cash = body["cash"]
        currency = body["currency"]
        queryset = Jar.objects.filter(id=id)
        if queryset:
            if currency == Jar.objects.filter(id=id)[0].currency:
                currentCash = Jar.objects.filter(id=id)[0].cash
                Jar.objects.filter(id=id).update(cash=currentCash + cash)
                newTransaction= Transaction(jar=Jar.objects.filter(id=id)[0],
                             cash=cash,
                             date=datetime.now(),
                            name='Cash in')
                newTransaction.save()
                return HttpResponse({'Cash in succeeded'}, content_type='text/json')
            else:
                return HttpResponse({'Select same currency jar'}, content_type='text/json')
        else:
            return HttpResponse({'There is no jar with that id'}, content_type='text/json')

@csrf_exempt
def get_transactions(request, jar_id=None, order_by=None, order=''):
    if request.method == "GET":
        if jar_id:
            if order_by:
                if order=='desc':
                    queryset = Transaction.objects.all().order_by('-' + str(order_by))
                else:
                    queryset = Transaction.objects.all().order_by('' + str(order_by))
            else:
                queryset = Transaction.objects.all()
            result = []
            for obj in queryset:
                if obj.jar.id == jar_id:
                    result.append(
                        {"id": obj.id, "jar": str(obj.jar), "name": obj.name, "cash": obj.cash, "date": str(obj.date)})
            json_stuff = json.dumps({"history": result})
            if result:
                return HttpResponse(json_stuff, content_type='text/json')
            else:
                return HttpResponse([{'There are no transactions in the database'}], content_type='text / json')
        else:
            if order_by:
                if order == 'desc':
                    queryset = Transaction.objects.all().order_by('-' + str(order_by))
                else:
                    queryset = Transaction.objects.all().order_by('' + str(order_by))
            else:
                queryset = Transaction.objects.all()
            result = []
            for obj in queryset:
                result.append({"id":obj.id, "jar" : str(obj.jar), "name": obj.name, "cash": obj.cash, "date": str(obj.date)})
            json_stuff = json.dumps({"history": result})
            if result:
                return HttpResponse(json_stuff, content_type='text/json')
            else:
                return HttpResponse([{'There are no transactions in the database'}], content_type='text / json')

@csrf_exempt
def transfer(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        fromid = body["from_id"]
        toid = body["to_id"]
        cash = body["cash"]
        fromset = Jar.objects.filter(id=fromid)
        toset = Jar.objects.filter(id=toid)
        if toid == fromid:
            return HttpResponse({'Transfer failed, select unique id\'s'}, content_type='text/json')
        else:
            if fromset and toset:
                fromCurrentCash = fromset[0].cash
                toCurrentCash = toset[0].cash
                if fromset[0].currency == toset[0].currency:
                    if fromCurrentCash >= cash:

                            Jar.objects.filter(id=fromid).update(cash=fromCurrentCash - cash)
                            Jar.objects.filter(id=toid).update(cash=toCurrentCash + cash)
                            newTransaction = Transaction(jar=Jar.objects.filter(id=fromid)[0],
                                                         cash=cash,
                                                         date=datetime.now(),
                                                         name=f'Transfer from {fromset[0].name} to {toset[0].name}')
                            newTransaction.save()
                            return HttpResponse({'Transfer succeeded'}, content_type='text/json')

                    else:
                        return HttpResponse({'Not enough cash in the Jar'}, content_type='text/json')
                else:
                    return HttpResponse({'Choose same currency jars'}, content_type='text/json')
            else:
                return HttpResponse({'There is no jar with that id'}, content_type='text/json')