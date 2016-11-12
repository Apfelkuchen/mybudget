from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^upload', views.upload, name='upload'),
	url(r'^dashboard', views.dashboard, name='dashboard'),
	url(r'^Trans/(?P<datestring>\d+\-\d+)$', views.getTMonth, name='getTMonth'),
	url(r'^Trans/(?P<datestring>\d+)$', views.getTYear, name='getTYear'),
	url(r'^Trans/(?P<field>[^\/]+)/(?P<fieldvalue>[^\/]+)[\/]+$', 
        views.getTransaction, name='getTransaction'),
	url(r'^changeT$', views.changeT, name='changeT'),
	url(r'^categories', views.showCategories, name='categories'),
	url(r'^CAT', views.getCategories, name='getCat'),
	url(r'^changeCAT$', views.changeCategory, name='changeCategory'),
	url(r'^assignCategories', views.assignCategories, name='assignCategories'),
	url(r'^ChartData/(?P<budget_type>\w+)/$', 
        views.chart_data_json, name='getChartData'),
	url(r'^ChartData/(?P<budget_type>\w+)/(?P<datestring>[0-9-]+)', 
        views.chart_data_json_date, name='chart_data_json_date'),
	url(r'^showCharts', views.showCharts, name='showCharts'),
	url(r'^Accounts/$', views.getAccounts, name='accounts'),
	url(r'^changeBalance/$', views.change_balance, name='changeBalance'),
	url(r'^dailyBalance/', views.getDailyBalance, name='dailyBalance'),
	url(r'^plotDailyBalance/', views.plotDailyBalance, name='plotBalance'),
	url(r'^upload_error', views.upload_error, name='uploadError'),
]