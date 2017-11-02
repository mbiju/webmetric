from django.conf.urls import url
from .views import HomeView, ProductDetailView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^product/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),
]