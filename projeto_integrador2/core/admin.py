from django.contrib import admin


# Register your models here.

from core.models import Administrador, Blog, Receita, Despesas

class ReceitaAdmin(admin.ModelAdmin):
    list_display = ("titulo",'recorrente')


admin.site.register(Administrador)
admin.site.register(Blog)
admin.site.register(Receita, ReceitaAdmin)
admin.site.register(Despesas)


