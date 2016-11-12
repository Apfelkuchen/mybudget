# -*- coding: utf-8 -*-
import decimal, re
from datetime import datetime
import csv
from Budget.models import Transaction, Category, Account
from Budget.lib.assign_categories import assignCat
import pandas as pd

## Debugging --> REMOVE ##
import logging
import sys

logger = logging.Logger(__name__)
##########################

def csv_handler(f, user, account):
    """
        Function to process the uploaded csv files.
        Extracts all information and stores the information as transaction
        model.

        Parameters:
        f:          ['File'] The uploaded csv file
        user:       ['response.user'] The owner of the transactions
        account:    ['account.id'] Account id used for the transactions
    """
    User = user

    # iso-8859-1 because of Sparkasse. Should change this!
    reader = pd.read_csv(f, delimiter=';', encoding='iso-8859-1', )
    acc = Account.objects.get(id=account)

    run_bal = 0
    for i, row in reader.iterrows():
        # Complete if there exists no name --> Bank stuff
        if row[5] == '':
            row[5] = 'Konto Gebühren/Zinsen'

        # Change messy csv file to good date format
        d = row[1]
        row[1] = d[:-2] + "20" + d[-2:]

        # Create new transaction if not already present
        formatted_date = str(datetime.strptime(row[1], "%d.%m.%Y")
                             .strftime("%Y-%m-%d"))
        objT, boolT = Transaction.objects.get_or_create(
            user=User,
            account=acc,
            date=formatted_date,
            ref=row[4],
            opp_name=row[5],
            opp_account=row[6],
            amount=decimal.Decimal(row[8].replace(',', '.')),
            currency=row[9],
        )
        if boolT:
            run_bal += float(row[8].replace(',', '.'))
        objT.save()

    print(run_bal)
    # Update Balance
    curr_bal = float(acc.balance)
    acc.balance = decimal.Decimal(curr_bal + run_bal)
    acc.save()

    assignCat(User)
    return {}
