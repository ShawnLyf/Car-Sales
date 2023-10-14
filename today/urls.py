from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("",views.GridView.as_view(),name='home'),
    path("<int:id>",views.single,name='detail'),
    # path("list",views.list,name='list'),
    path('get_models/', views.get_models_for_brand, name='get_models_for_brand')
]  + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)