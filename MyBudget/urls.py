from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^Budget/', include('Budget.urls', namespace="budget")),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls', namespace="account")),
]
