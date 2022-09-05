from django.urls import path
from . import views
from .views import DetalheListView
app_name = "core"
urlpatterns =[
    
    path("", views.LoginPageView.as_view(), name="Login"),
    path("home", views.HomePageView.as_view(), name="home"),
    path("home/privacidade/", views.PrivacidadePageView.as_view(), name="privacidade"),
    path("home/legal/terms/", views.LegalTermsPageView.as_view(), name="legal_terms"),
    path("menu/", views.MenuPageView.as_view(), name="menu"),
    path("menu/inicio/", views.InicioPageView.as_view(), name="inicio"),
    #path("menu/detalhes/", DetalheListView.as_view(), name="detalhes"),
    #path("menu/detalhes/", views.DetalhesPageView.as_view(), name="detalhes"),
    path("menu/detalhes/", views.saldo_total, name="saldo_total"),
    path("menu/despesas_categoria/", views.DespesasCategoriaPageView.as_view(), name="despesas_categoria"),
    path("menu/planejamento_despesas/", views.PlanejamentoDespesasPageView.as_view(), name="planejamento_despesas"),
    
    path('orcamento/<int:id>/', views.saldo_receita, name='saldo_receita'),
    path("menu/contas_a_pagar/", views.Contas_a_PagarPageView.as_view(), name="contas_a_pagar"),
    #path("menu/porCategoria/", views.PorCategoriaPageView.as_view(), name="porCategoria"),
    path("menu/modalGenerico/", views.ModalGenericoPageView.as_view(), name="modalGenerico"),
    #path("menu/modalPerfil/", views.#ModalPerfilPageView.as_view(), #name="modalPerfil"),
    path("menu/modalPerfilAparencia/", views.ModalPerfilAparenciaPageView.as_view(), name="modalPerfilAparencia"),

    ####################
    # TODO: Register create view
    path('menu/administrador/register', views.AdministradorCreateView.as_view(), name='administrador_register'), 
     # TODO: Register create view
    path('menu/blog/register', views.BlogCreateView.as_view(), name='blog_register'),
    # TODO: Register create view
    


    ####Despesas    
    path('menu/despesas/',views.Despesas_html,name='despesas_register'),
    path('menu/despesas/despesas_cadastro/', views.despesas_cadastro),
    path('menu/despesas/despesas_cadastro/submit', views.Submit_despesas_cadastro,name='despesas_submit'),
    path('menu/despesas/delete/<int:id_despesas>/', views.Delete_despesas,name='despesas_delete' ),
    #Fim Despesas   


    ####Receita    
    path('menu/receita/',views.Receita_html,name='receita_register'),
    path('menu/receita/receita_cadastro/', views.receita_cadastro),
    path('menu/receita/receita_cadastro/submit', views.Submit_receita_cadastro,name='despesas_submit'),
    path('menu/receita/delete/<int:id_receita>/', views.Delete_receita,name='receita_delete' ),
    #Fim Receita  


    ####BLog    
    path('menu/blog/',views.Blog_html,name='blog_register'),
    path('menu/blog/blog_cadastro/', views.blog_cadastro),
    path('menu/blog/blog_cadastro/submit', views.Submit_blog_cadastro,name='blog_submit'),
    path('menu/blog/delete/<int:id_blog>/', views.Delete_blog,name='blog_delete' ),
    #Fim Blog      


]
