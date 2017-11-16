from django import forms


class CodigoFuente(forms.Form):
    codigo = forms.CharField(widget=forms.Textarea, label="")
    codigo.widget.attrs["class"] = "form-control"
    # fields = ('codigo',)
