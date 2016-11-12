import re

from Budget.models import Transaction, Category

def assignCat(User):
# Asign the correct category to transaction
#tmp_category = Category.objects.get(category='Unknown')
    for trans in Transaction.objects.filter(user=User,category='Unknown'):
        tmp_category = "Unknown"
        for cats in Category.objects.filter(user=User).exclude(category='Unknown'):
            regs = cats.getReg()
            regexes = [re.compile(k, re.IGNORECASE) for k in regs]
            if (any(regex.search(trans.opp_name) for regex in regexes) or any(regex.search(trans.ref) for regex in regexes)):
		    #tmp_category = Category.objects.get(category=cats.category)
                trans.category = cats.category
                trans.save()
                break

    return
