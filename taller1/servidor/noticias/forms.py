from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(label='Buscar', max_length=100)
    kind = forms.ChoiceField(label='Filtrar por', choices=[('all', 'Todos los campos'), ('title', 'Título'),('description', 'Descripción'), ('category', 'Categoría')])
    
