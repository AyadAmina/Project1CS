from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', views.index, name='index'),
    path('my_profile/<int:id>', views.profile, name='profile'),
    path('delete-favoris/<int:favoris_id>',views.delete_favoris, name='delete_favoris'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
