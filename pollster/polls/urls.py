from django.urls import path

# Import views
from . import views

# Give app a name
app_name = "polls"
urlpatterns = [
    path('', views.index, name='index'), # /polls/index.html
]
