from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    # posts
    path("posts", views.PostsListView.as_view(), name="posts"),
    path("make_post", views.PostCreateView.as_view(), name="make_post"),
    path("update_post/<int:pk>", views.PostsUpdateView.as_view(), name="update_post"),
    path("delete_post/<int:pk>", views.PostDeleteView.as_view(), name="delete_post"),

    # lessons
    path("lessons", views.LessonsListView.as_view(), name="lessons"),
    path("lessons_per_month", views.LessonsPerMonthListView.as_view(), name="lessons_per_month"),
    path("create_lesson", views.LessonsCreateView.as_view(), name="create_lesson"),
    path("delete_lesson/<int:pk>", views.LessonsDeleteView.as_view(), name="delete_lesson"),
    path("edit_lesson/<int:pk>", views.LessonsUpdateView.as_view(), name="edit_lesson"),

    # clients
    path("clients", views.ClientCreateView.as_view(), name="clients"),
    path("delete_client/<int:pk>", views.ClientDeleteView.as_view(), name="delete_client"),
    path("edit_client/<int:pk>", views.ClientUpdateView.as_view(), name="edit_client"),

    # other
    path("create_comment/<int:pk>", views.CommentCreateView.as_view(), name="create_comment"),
    path("about", views.about, name="about"),
    path("courses", views.courses, name="courses"),
]
