from django.views import generic
from .models import Category, Site
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
import re
from django.conf import settings

class IndexView(generic.ListView):
    model = Site
    template_name = "pawmap/site_list.html"
    context_object_name = "object_list"

    def extract_prefecture(self, address):
        match = re.match(r"^(.*?都|.*?道|.*?府|.*?県)", address)
        return match.group(0) if match else None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = None  # すべてのページではカテゴリーが未選択

        # 都道府県リストを生成
        all_sites = Site.objects.all()
        prefectures = sorted({self.extract_prefecture(site.address) for site in all_sites if self.extract_prefecture(site.address)})
        context['prefectures'] = prefectures
        context['current_prefecture'] = self.request.GET.get("prefecture")
        return context

    def get_queryset(self):
        queryset = Site.objects.all()
        prefecture = self.request.GET.get("prefecture")

        if prefecture:  # 都道府県のフィルタリング
            queryset = [site for site in queryset if self.extract_prefecture(site.address) == prefecture]

        return queryset


class CategoryView(generic.ListView):
    model = Site
    template_name = "pawmap/site_list.html"
    context_object_name = "object_list"

    # 都道府県を抽出するヘルパー関数
    def extract_prefecture(self, address):
        match = re.match(r"^(.*?都|.*?道|.*?府|.*?県)", address)
        return match.group(0) if match else None

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        prefecture = self.request.GET.get("prefecture")

        queryset = Site.objects.filter(category__id=category_id)

        if prefecture:  # 都道府県のフィルタリング
            queryset = [site for site in queryset if self.extract_prefecture(site.address) == prefecture]

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.kwargs["category_id"]
        
        # 都道府県リストを生成
        all_sites = Site.objects.all()
        prefectures = sorted({self.extract_prefecture(site.address) for site in all_sites if self.extract_prefecture(site.address)})
        context['prefectures'] = prefectures
        context['current_prefecture'] = self.request.GET.get("prefecture")
        return context
      
class HowToUseView(TemplateView):
    template_name = "pawmap/how_to_use.html"  # how_to_use.html を指定
    
class AboutView(TemplateView):
    template_name = "pawmap/about.html"  # about.html をテンプレートとして指定
    
class MapView(generic.TemplateView):
    template_name = "pawmap/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 全てのスポットの住所をリスト形式で取得
        context["sites_addresses"] = [site.address for site in Site.objects.all()]
        # GoogleマップAPIキーを追加
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        return context

class DetailView(generic.DetailView):
    model = Site

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # GoogleマップAPIキーを追加
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        return context

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Site
    fields = ["name", "address", "category"] 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Site
    fields = ["name", "address", "category"] # '__all__'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Site
    success_url = reverse_lazy("pawmap:index")