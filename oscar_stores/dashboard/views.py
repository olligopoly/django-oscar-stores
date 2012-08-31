from django.views import generic
from django.db.models import get_model
from django.core.urlresolvers import reverse

from extra_views import (CreateWithInlinesView, UpdateWithInlinesView,
                         InlineFormSet)

from chocolatebox.dashboard.stores import forms

Store = get_model('stores', 'store')
StoreGroup = get_model('stores', 'storegroup')
OpeningTime = get_model('stores', 'openingtime')


class StoreListView(generic.ListView):
    model = Store
    template_name = "dashboard/stores/store_list.html"
    context_object_name = "store_list"


class OpeningTimeInline(InlineFormSet):
    extra = 7
    max_num = 7
    model = OpeningTime
    form_class = forms.OpeningTimeForm


class StoreCreateView(CreateWithInlinesView):
    model = Store
    template_name = "dashboard/stores/store_update.html"
    inlines = [OpeningTimeInline]
    form_class = forms.StoreForm

    def get_success_url(self):
        return reverse('dashboard:store-list')


class StoreUpdateView(UpdateWithInlinesView):
    model = Store
    template_name = "dashboard/stores/store_update.html"
    inlines = [OpeningTimeInline]
    form_class = forms.StoreForm

    def get_success_url(self):
        return reverse('dashboard:store-list')


class StoreDeleteView(generic.DeleteView):
    model = Store
    template_name = "dashboard/stores/store_delete.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        for time in self.object.opening_times.all():
            time.delete()
        return super(StoreDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('dashboard:store-list')


class StoreGroupListView(generic.ListView):
    model = StoreGroup
    context_object_name = 'group_list'
    template_name = "dashboard/stores/store_group_list.html"


class StoreGroupCreateView(generic.CreateView):
    model = StoreGroup
    template_name = "dashboard/stores/store_group_update.html"

    def get_success_url(self):
        return reverse('dashboard:store-group-list')


class StoreGroupUpdateView(generic.UpdateView):
    model = StoreGroup
    template_name = "dashboard/stores/store_group_update.html"

    def get_success_url(self):
        return reverse('dashboard:store-group-list')


class StoreGroupDeleteView(generic.DeleteView):
    model = StoreGroup
    template_name = "dashboard/stores/store_group_delete.html"

    def get_success_url(self):
        return reverse('dashboard:store-group-list')
