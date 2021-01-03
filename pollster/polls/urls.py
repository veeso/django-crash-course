from django.urls import path

# Import views
from . import views

# Give app a name
app_name = "polls"
urlpatterns = [
    path('', views.index, name='index'), # /polls/index.html
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
