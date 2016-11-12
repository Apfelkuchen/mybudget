import csv, decimal
from datetime import datetime

from Budget.models import Transaction, Balance

def cal_bal_month(f):
			reader = csv.reader(f, delimiter=';')
			next(reader, None)
			for row in reader:
				if row[5] == '':
					row[5] = 'Sparkasse Zinsen/Gebuehren'

				# Change messy csv file to good date format
				d = row[1]
				row[1] = d[:-2] + "20" + d[-2:] # Add a 20 to the year

				obj, bol = Transaction.objects.get_or_create(
					account = row[0],
					date = str(datetime.strptime(row[1], "%d.%m.%Y").strftime("%Y-%m-%d")),
					ref = row[4],
					opp_name = row[5],
					opp_account = row[6],
					amount = decimal.Decimal(row[8].replace(',','.')),
					currency = row[9],
				)
				if bol == True:
					
					# Global balance
					#BalA = Balance.objects.get(name='Global', account=row[0])
					#BalA.bal += decimal.Decimal(row[8].replace(',','.'))
					#BalA.save()

					# Monthly balance
					obj2, bol2 = Balance.objects.get_or_create(
						name = str(datetime.strptime(row[1], "%d.%m.%Y").strftime("%Y-%m")),
						account = row[0],
						cur = row[9])
					obj2.bal = decimal.Decimal(obj2.bal)
					obj2.bal += decimal.Decimal(row[8].replace(',','.'))
					obj2.save()
