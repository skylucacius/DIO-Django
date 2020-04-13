from django.contrib import admin
from core.models import Evento
# Register your models here.
class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario','titulo', 'data_evento', 'data_criacao', 'local')
    list_filter = ('usuario','data_evento')
    
admin.site.register(Evento, EventoAdmin)