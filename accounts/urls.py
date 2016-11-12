from django.contrib.auth.views import (
    logout,
    password_change,
    password_change_done,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
)
from django.conf.urls import url
from .views import login_view


urlpatterns = [
    url(
        regex=r'^login/$',
        view=login_view,
        name='login',
    ),
    url(
        regex=r'^logout/$',
        view=logout,
        kwargs={'next_page': 'account:login' },
        name='logout'
    )
]
