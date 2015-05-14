from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

# Create your views here.
from muh_core_app.models import Guilda, Personagem, Historico, Bis, Boss, Equipamento

def home(request):
	return render(request, 'muh_core_app/home.html')

def index(request):
    lista_guildas = Guilda.objects.order_by('nome')
    context = {'lista_guildas': lista_guildas}
    return render(request, 'muh_core_app/index.html', context)


def guilda(request, guilda_id, filtros={}):

	guilda = Guilda.objects.get(pk=guilda_id)
	membros = guilda.personagem_guilda.all().order_by('-ilvl_equipado')

	#Apenas os top X membros
	paginator = Paginator(membros, 20)

	page = request.GET.get('page')

	try:
		lista_membros = paginator.page(page)
	except PageNotAnInteger:
 		# If page is not an integer, deliver first page.
		lista_membros = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		lista_membros = paginator.page(paginator.num_pages)

	return render_to_response('muh_core_app/guilda.html', {"lista_membros": lista_membros, 'guilda':guilda})

def bis_list(request):

	bis_list = Bis.objects.all()

	#Apenas os top X membros
	paginator = Paginator(bis_list, 20)

	page = request.GET.get('page')

	try:
		lista_bis = paginator.page(page)
	except PageNotAnInteger:
 		# If page is not an integer, deliver first page.
		lista_bis = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		lista_bis = paginator.page(paginator.num_pages)

	return render_to_response('muh_core_app/bis.html', {"lista_bis": lista_bis})

def bosses(request):

	bosses = Boss.objects.all()
	boss_equips = {}

	for boss in bosses:
		#Todos os equips que dropam do boss X
		boss_equips[boss.nome] = Equipamento.objects.filter(dropped_by=boss)


	#Apenas os top X membros
	paginator = Paginator(bosses, 20)

	page = request.GET.get('page')

	try:
		lista_bosses = paginator.page(page)
	except PageNotAnInteger:
 		# If page is not an integer, deliver first page.
		lista_bosses = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		lista_bosses = paginator.page(paginator.num_pages)

	return render_to_response('muh_core_app/bosses.html', {"bosses": lista_bosses, "boss_equips": boss_equips})

def personagem(request, personagem_id):
	personagem = Personagem.objects.get(pk=personagem_id)
	historico = Historico.objects.filter(personagem = personagem)

	datas = []
	ilvls = []

	for h in historico:
		datas.append(str(h.data.strftime("%d")) + "/" + str(h.data.strftime("%m")))
		ilvls.append(int(h.ilvl_equipado))

	datas = json.dumps(datas)
	ilvls = json.dumps(ilvls)

	return render(request, 'muh_core_app/personagem.html', {'personagem': personagem, 'datas':datas, 'ilvls':ilvls})

def chart_all(request, guilda_id):
	guilda = Guilda.objects.get(pk=guilda_id)
	membros = guilda.personagem_guilda.all()



