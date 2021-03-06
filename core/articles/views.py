from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.urls import reverse_lazy
from core import models
from . import forms
from _common import mixins, views


class AddArticleView(mixins.PageMixin, generic.CreateView):
    template_name = 'article/add.html'
    form_class = forms.AddArticleForm
    title = _('Add Article')

    def get_success_url(self):
        return reverse_lazy('articles:change', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by_id = self.request.user.pk
        instance.save()
        return super(AddArticleView, self).form_valid(form)


class ChangeArticleView(mixins.PageMixin, generic.UpdateView):
    template_name = 'article/edit.html'
    form_class = forms.ChangeArticleForm
    queryset = models.Article.objects.all()
    title = _('Change Article')

    def get_queryset(self):
        return self.queryset.filter(created_by_id=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy('articles:change', kwargs={'slug': self.object.slug})


class ReadArticleView(mixins.PageMixin, generic.DetailView):
    template_name = 'article/read.html'
    queryset = models.Article.objects.select_related('created_by')
    query_pk_and_slug = True
    context_object_name = 'article'
    title_template = '%s'
    title_object = True
    title_object_attribute = 'title'


class PublishArticleView(views.ActionView):
    url = reverse_lazy('profile:me')
    queryset = models.Article.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by_id=self.request.user.pk).exclude(status=models.Article.STATUSES.PUBLISHED)

    def action(self):
        instance = self.object
        instance.add_log(models.ArticleHistory.STATUSES.PUBLISHED)
        instance.status = models.Article.STATUSES.PUBLISHED
        instance.save()
