# adote/templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    """
    Adiciona a classe CSS ao campo do formulário.
    Garante que o campo é realmente um campo de formulário.
    """
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'class': css_class})
    return field
