from django import forms


class searchForm(forms.Form):
    query = forms.CharField()

    class Meta:
        fields = ['query', ]
