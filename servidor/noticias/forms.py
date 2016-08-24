from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(label='Buscar', max_length=100)
    kind = forms.ChoiceField(label='Filtrar por', choices=[('title', 'Título'),
                                                           ('description', 'Descripción'),
                                                           ('category', 'Categoría'),
                                                           ('all', 'Todos los campos')])
    
