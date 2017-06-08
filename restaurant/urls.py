from django.conf.urls import patterns, include, url
import restaurant.views


urlpatterns = patterns('restaurant.views',
    url(r'^/?$','index'),
    url(r'^metamask/?$','metamask'),
    url(r'^balance/?$','balance'),
    url(r'^comment/(?P<id_transaction>\d*)/?$','comment'),
    url(r'^comment_list/?$','comment_list'),
    url(r'^payment/?$','payment'),
    url(r'^payment_accepted/?$','payment_accepted'),
    url(r'^restaurant_list/?$','restaurant_list'),
    url(r'^review_list/(?P<id_restaurant>\d*)/?$','review_list'),
    url(r'^new_bill/?$','new_bill'),
    url(r'^create_contract/?$','create_contract'),
)
