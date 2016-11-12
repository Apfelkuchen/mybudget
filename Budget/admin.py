from django.contrib import admin
from Budget.models import Transaction, Category, Account

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'opp_name','amount','currency', 'ref', 'date')
    #ist_filter = ['pub_date']
    search_fields = ['opp_name']
    ordering = ['-date']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'regexp')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Account)
