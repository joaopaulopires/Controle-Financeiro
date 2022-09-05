from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from .models import Despesas, Receita, Blog
from . import models
from django.views import generic
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404 
from django.db.models import Sum 

from django import template





usuario = authenticate

# Create your views here.
#def index(request):
 #   return render(request,'home.#html')

def handler404(request, exception):
    return render(request, '404.html')

class HomePageView(TemplateView):
    template_name = "home.html"
class DespesasCategoriaPageView(TemplateView):
    template_name = "despesas_categoria.html"
    
class LoginPageView(TemplateView):
    template_name = "account/login.html"    

class LegalTermsPageView(TemplateView):
    template_name = "legal_terms.html" 

class PrivacidadePageView(TemplateView):
    template_name = "privacidade.html"

class MenuPageView(TemplateView):
    template_name = "menu.html"     

class InicioPageView(TemplateView):
    template_name = "inicio.html"  
class PlanejamentoDespesasPageView(TemplateView):
    template_name = "planejamento_despesas.html"

class DetalheListView(ListView):
    model = Receita


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['receitateste'] = Receita.objects.aggregate(Sum('valor'))
        context['despesateste'] = Despesas.objects.aggregate(Sum('valor'))
        context['termopesquisa'] = request.GET.get('mes-pesquisa', None)

        return context

@login_required(login_url='/login/')
def saldo_total(request):

    termopesquisas = request.GET.get('mes-pesquisa', None)

    if termopesquisas:
        #Atributos de datetima para a variável termopesquisa
        data = datetime.strptime(termopesquisas, '%Y-%m').date()
        mes = data.month

        #Busca pelas ocorrências no mês requisitado
        #usuario = request.user
        #auto_data = datetime.now() - timedelta(hours=1)
        #evento_receita = Receita.objects.filter(usuario=usuario)
        result_rec = Receita.objects.filter(auto_data__month=data.month)
        result_des = Despesas.objects.filter(auto_data__month=data.month)


        usuario = request.user
        saldototal = {}
        saldototal['saldo_receita'] = Receita.objects.filter(auto_data__month=data.month).aggregate(Sum('valor'))
        saldototal['saldo_despesas'] = Despesas.objects.filter(auto_data__month=data.month).aggregate(Sum('valor'))
        saldorec = Receita.objects.filter(auto_data__month=data.month).aggregate(Sum('valor'))
        saldodesp = Despesas.objects.filter(auto_data__month=data.month).aggregate(Sum('valor'))


        #RETORNOS DE VARIÁVEIS PARA O TEMPLATE
        saldototal['tot_rec'] = saldorec.get("valor__sum")
        saldototal['tot_desp'] = saldodesp.get("valor__sum")
        saldototal['termodapesquisa'] = mes
        saldototal['query_rec'] = result_rec
        saldototal['query_desp'] = result_des

        #testes na linha de comando
        print(usuario, type(usuario))
        print(saldototal['tot_rec'], type(saldototal['tot_rec']))
        print(saldototal['saldo_receita'], type(saldototal['saldo_receita']))
        print("teste", saldototal['saldo_despesas'], type(saldototal['saldo_despesas']))
        print("testerece", saldototal['saldo_receita'], type(saldototal['saldo_receita']))
        print("testedesp", saldototal['saldo_despesas'], type(saldototal['saldo_despesas']))
        print("type", saldototal['saldo_receita'].get("valor__sum"), type(saldototal['saldo_receita'].get("valor__sum")))

        # CONSOLIDADO ENTRE RECEITA E DESPESA
        if saldototal['saldo_receita'] == {'valor__sum': None} and saldototal['saldo_despesas'] == {'valor__sum': None}:
            saldototal['saldo_mensal'] = 0
            print(saldototal['saldo_mensal'], type(saldototal['saldo_mensal']))
        elif saldototal['saldo_receita'].get("valor__sum") == None:
            saldototal['saldo_receita'] = 0
            saldototal['saldo_mensal'] = saldototal['saldo_receita'] - saldototal['saldo_despesas'].get("valor__sum")
        elif saldototal['saldo_despesas'].get("valor__sum") == None:
            saldototal['saldo_despesas'] = 0
            saldototal['saldo_mensal'] = saldototal['saldo_receita'].get("valor__sum") - saldototal['saldo_despesas']
        else:
            saldototal['saldo_mensal'] = saldototal['saldo_receita'].get("valor__sum") - saldototal['saldo_despesas'].get("valor__sum")

    else:
        saldototal = {}
        saldototal['saldo_receita'] = Receita.objects.aggregate(Sum('valor'))
        saldototal['saldo_despesas'] = Despesas.objects.aggregate(Sum('valor'))
        # saldototal['calculadora'] = saldototal['saldo_receita'] - saldototal['saldo_despesas']


    return render(request, 'detalhes.html', {'saldotot': saldototal})

"""class DetalhesPageView(TemplateView):
    template_name = "detalhes.html" """

class Contas_a_PagarPageView(TemplateView):
    template_name = "contas_a_pagar.html" 

#class PorCategoriaPageView(TemplateView):
 #   template_name = "porCategoria.html"

class ModalGenericoPageView(TemplateView):
    template_name = "modalGenerico.html" 

#class ModalPerfilPageView(TemplateView):
   # template_name = "modalPerfil.html"     

class ModalPerfilAparenciaPageView(TemplateView):
    template_name = "modalPerfilAparencia.html" 

###########################################    



###############Final views.py#######
class AdministradorCreateView(generic.CreateView):
    model = models.Administrador
    template_name = 'modalPerfil.html'
    fields = ['nome_social', 'titulo', 'email','telefone']

class BlogCreateView(generic.CreateView):
    model = models.Blog
    template_name = 'inicio.html'
    fields = ['titulo', 'img', 'texto','link']    

class ReceitaCreateView(generic.CreateView):
    model = models.Receita
    template_name = 'porCategoria.html'
    fields = ['titulo', 'recorrente', 'produto','valor','status','total_receber']

##########DEspesas################

@login_required(login_url='/login/')
def Despesas_html(request):
    usuario = request.user
    auto_data = datetime.now() - timedelta(hours=1)
    evento_despesas = Despesas.objects.filter(usuario=usuario)
    dados = {'eventos':evento_despesas}
    return render(request, 'despesas.html', dados) 
    
@login_required(login_url='/login/')
def despesas_cadastro(request):
    id_evento_despesas=request.GET.get('id')
    dados={}
    if id_evento_despesas:
        dados['evento_despesas']=Despesas.objects.get(id=id_evento_despesas)
    return render(request,'despesas_cadastro.html',dados)    

@login_required(login_url='/login/')
def Submit_despesas_cadastro(request):
    if request.POST:
        titulo=request.POST.get('titulo')
        recorrente=request.POST.get('recorrente')
        produto=request.POST.get('produto')
        valor=request.POST.get('valor')
        auto_data=request.POST.get('auto_data')
        status=request.POST.get('status')
        total_pago=request.POST.get('total_pago')
        id_despesas = request.POST.get('id')
        usuario = request.user

        if id_despesas:
            evento_despesas = Despesas.objects.get(id=id_despesas)
            if usuario == evento_despesas.usuario:            
                Despesas.objects.filter(id=id_despesas).update(titulo=titulo,
                            recorrente=recorrente,
                            produto=produto,
                            valor=valor,
                            auto_data=auto_data,
                            status=status,
                            total_pago=total_pago)

        else :
            Despesas.objects.create(titulo=titulo,
                                    recorrente=recorrente,
                                    produto=produto,
                                    valor=valor,
                                    auto_data=auto_data,
                                    status=status,
                                    total_pago=total_pago,
                                    usuario=usuario)
    return redirect('/menu/despesas/despesas_cadastro/')
'''    
@login_required(login_url='/login/')
def Delete_despesas(request, id_despesas):
    despesas_delete=Despesas.objects.get(id=id_despesas).delete()
    return redirect('/menu/despesas/') 
'''

@login_required(login_url='/login/')
def Delete_despesas(request, id_despesas):
    usuario = request.user
    try:
        evento_despesas = Despesas.objects.get(id=id_despesas)
    except Despesas.DoesNotExist:
        raise Http404
    if usuario == evento_despesas.usuario:
        evento_despesas.delete()
    else:
        raise Http404
    return redirect('/menu/despesas/')     

##########Receita################

'''
    #@login_required
def Receita_html(request):
    evento_receita = Receita.objects.all()
    dados = {'eventos': evento_receita}
    return render(request,'receita.html',dados)
    '''
@login_required(login_url='/login/')
def Receita_html(request):
    usuario = request.user
    auto_data = datetime.now() - timedelta(hours=1)
    evento_receita = Receita.objects.filter(usuario=usuario)
    dados = {'eventos':evento_receita}
    return render(request, 'receita.html', dados)    

@login_required(login_url='/login/')
def receita_cadastro(request):
    id_evento_receita=request.GET.get('id')
    dados={}
    if id_evento_receita:
        dados['evento_receita']=Receita.objects.get(id=id_evento_receita)
    return render(request,'receita_cadastro.html',dados)

@login_required(login_url='/login/')
def Submit_receita_cadastro(request):
    if request.POST:
        titulo=request.POST.get('titulo')
        recorrente=request.POST.get('recorrente')
        produto=request.POST.get('produto')
        valor=request.POST.get('valor')
        auto_data=request.POST.get('auto_data')
        status=request.POST.get('status')
        total_receber=request.POST.get('total_receber')
        id_receita = request.POST.get('id')
        usuario = request.user 

        if id_receita:
            evento_receita = Receita.objects.get(id=id_receita)
            if usuario == evento_receita.usuario:
                Receita.objects.filter(id=id_receita).update(titulo=titulo,
                            recorrente=recorrente,
                            produto=produto,
                            valor=valor,
                            auto_data=auto_data,
                            status=status,)          


        else :
            Receita.objects.create(titulo=titulo,
                                    recorrente=recorrente,
                                    produto=produto,
                                    valor=valor,
                                    auto_data=auto_data,
                                    status=status,
                                   
                                    usuario=usuario)                         
    return redirect('/menu/receita/receita_cadastro/')

@login_required(login_url='/login/')
def Delete_receita(request, id_receita):
    usuario = request.user
    try:
        evento_receita = Receita.objects.get(id=id_receita)
    except Receita.DoesNotExist:
        raise Http404
    if usuario == evento_receita.usuario:
        evento_receita.delete()
    else:
        raise Http404
    return redirect('/menu/receita/') 

@login_required(login_url='/login/')
def saldo_receita(request, id=None, *args, **kwargs):
	contexto = {}
	contexto['saldo_receita'] = Receita.objects.get(id=id)

	return render(request, "receita.html", contexto)    

"""@login_required(login_url='/login/')
def saldo_total(request):
    #usuario = request.user
    saldo_receita=Receita.objects.aggregate(Sum('valor'))
    print(saldo_receita)
    saldo_despesas=Despesas.objects.aggregate(Sum('valor'))
    print(saldo_despesas)
    saldo_total=(saldo_receita+saldo_despesas)
    return render('/menu/detalhes')"""

##########Blog################


    #@login_required
def Blog_html(request):
    evento_blog = Blog.objects.all()
    dados = {'eventos': evento_blog}
    return render(request,'blog.html',dados)

#@login_required(login_url='login/')
def blog_cadastro(request):
    id_evento_blog=request.GET.get('id')
    dados={}
    if id_evento_blog:
        dados['evento_blog']=Blog.objects.get(id=id_evento_blog)
    return render(request,'blog_cadastro.html',dados)

#@login_required
def Submit_blog_cadastro(request):
    if request.POST:
        titulo=request.POST.get('titulo')
        img=request.POST.get('img')
        texto=request.POST.get('texto')
        link=request.POST.get('link')
        auto_data=request.POST.get('auto_data')
        id_blog = request.POST.get('id')

        if id_blog:
            Blog.objects.filter(id=id_blog).update(titulo=titulo,
                        
                        img=img,
                        texto=texto,
                        auto_data=auto_data,
                        link=link,)

        else :
            Blog.objects.create(titulo=titulo,
                        
                        img=img,
                        texto=texto,
                        auto_data=auto_data,
                        link=link,)
    return redirect('/menu/blog/blog_cadastro/')
#@login_required
def Delete_blog(request, id_blog):
    blog_delete=Blog.objects.get(id=id_blog).delete()
    return redirect('/menu/blog/')              

"""        if saldototal['saldo_receita'].get("valor__sum") == None:
            saldototal['saldo_receita'] = 0
            if saldototal['saldo_despesas'].get("valor__sum") == None:
                saldototal['saldo_mensal'] = 0
            #saldototal['saldo_mensal'] = (saldototal['saldo_receita']) - ((saldototal['saldo_despesas'].get("valor__sum")))
        if saldototal['saldo_despesas'].get("valor__sum") == None:
            saldototal['saldo_despesas'] = 0
            if saldototal['saldo_receita'].get("valor__sum") == None:
                saldototal['saldo_mensal'] = 0
            saldototal['saldo_mensal'] = saldototal['saldo_receita'].get("valor__sum") - saldototal['saldo_despesas']"""
            
         