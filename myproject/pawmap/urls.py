from django.urls import path
from . import views

app_name = "pawmap"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("category/<int:category_id>/", views.CategoryView.as_view(), name="category_list"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("create/", views.CreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.UpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.DeleteView.as_view(), name="delete"),
    path("how_to_use/", views.HowToUseView.as_view(), name="how_to_use"),  # ご利用方法のURLを追加
    path("about/", views.AboutView.as_view(), name="about"),  # このサイトについてのURLを追加
    path("map/", views.MapView.as_view(), name="map"),  # 全体マップのURLを追加
]