from django.urls import path
from task_manager.tasks import views


urlpatterns = [
    path('', views.SearchResultsListView.as_view(), name='tasks'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
]
