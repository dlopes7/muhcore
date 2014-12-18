from django.shortcuts import render

# Create your views here.
from muh_core_app.models import Guilda


def index(request):
    lista_guildas = Guilda.objects.order_by('nome')[:5]
    context = {'lista_guildas': lista_guildas}
    return render(request, 'muh_core_app/index.html', context)


def guilda(request, guilda_id):
	guilda = Guilda.objects.get(pk=guilda_id)
	return render(request, 'muh_core_app/guilda.html', {'guilda': guilda})