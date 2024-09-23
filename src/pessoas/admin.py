from django.contrib import admin
from .models import Pessoa


class PessoaAdmin(admin.ModelAdmin):
    """
        Administração para o modelo Pessoa no painel de administração do Django.

        Esta classe configura a exibição e administração do modelo Pessoa no Django Admin, especificando os campos a serem exibidos na lista de itens.

        Atributos:
            list_display (tuple): Define os campos a serem exibidos na lista de itens no painel de administração. Inclui 'nome', 'email', 'ativo' e 'valor'.
        """
    
    list_display = ('nome', 'email', 'ativo', 'valor')

admin.site.register(Pessoa, PessoaAdmin)