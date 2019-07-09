from django.conf.urls import url, include


from . import views


urlpatterns = [
    url(r'^me/applications/(?P<position>\d+)/(?P<applicant>\d+)/(?P<status>\w+)/$',
        views.UserApplicationStatus.as_view(), name='status_update'),
    url(r'^me/applications/$', views.UserApplications.as_view(), name='my_applications'),
    url(r'^me/edit/$', views.EditProfile.as_view(), name='edit_profile'),
    url(r'^me/notifications/$', views.UserNotifications.as_view(), name='my_notifications'),
    url(r'^me/$', views.ShowProfile.as_view(), name='my_profile'),
    url(r'^(?P<slug>[-\w]+)/$', views.ShowProfile.as_view(), name='show_profile'),

]
