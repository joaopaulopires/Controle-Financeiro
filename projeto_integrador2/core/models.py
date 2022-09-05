from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# TODO: Import reverse
from django.urls import reverse


# Create your models here.
#Administrador

class Administrador(models.Model):
    titulo=models.CharField(max_length=50,null=True,blank=True,verbose_name='Titulo')
    nome_social=models.CharField(max_length=50,null=True,blank=True,verbose_name='Autor')
    email=models.EmailField(max_length=50,)
    telefone=models.IntegerField(null=True,blank=True,verbose_name='Telefone')
    # TODO: Add get_absolute_url
    def get_absolute_url(self):
        return reverse('administrador_detail', kwargs={"pk": self.pk})    
    def __str__(self):
        return self.titulo

class Blog(models.Model):
    titulo=models.CharField(max_length=50,null=True,blank=True,verbose_name='Título')
    img=models.ImageField(upload_to='images/',null=True,blank=True,verbose_name='Imagem')
    texto=models.TextField(max_length=200,null=True,blank=True,verbose_name='Texto')
    link=models.URLField()
    auto_data=models.DateField(null=True,blank=True,verbose_name='Data')  
    def __str__(self):
        return self.titulo

#Usuario


class Receita(models.Model):
    titulo=models.CharField(null=True,blank=True,max_length=50,verbose_name='Título')
    recorrente=models.BooleanField(default=False,null=True,blank=True,verbose_name='Recorrente')
    produto=models.CharField(max_length=50,verbose_name='Produto')
    valor=models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Valor', default=0)
    auto_data=models.DateField(null=True,blank=True,verbose_name='Data')
    status=models.BooleanField(default=False,null=True,blank=True,verbose_name='Status')
    total_receber=models.DecimalField(max_digits=10, decimal_places=2, editable=False,verbose_name='Total', default=None)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.titulo  + ",R$" + str(self.valor) +"," + "R$" +str(self.total_receber)

        #calculo
    def save(self, *args, **kwargs):
        self.total_receber = (self.valor)
        #self.total_receber.save()
        return super (Receita, self).save(*args, **kwargs)
    

class Despesas(models.Model):
    titulo=models.CharField(null=True,blank=True,max_length=50,verbose_name='Título')
    recorrente=models.BooleanField(default=False,null=True,blank=True,verbose_name='Recorrente')
    produto=models.CharField(max_length=50,verbose_name='Produto')
    valor=models.DecimalField(max_digits=10, decimal_places=2)
    auto_data=models.DateField(null=True,blank=True,verbose_name='Data')
    status=models.BooleanField(default=False,null=True,blank=True,verbose_name='Status')
    total_pago=models.DecimalField(max_digits=10, decimal_places=2,editable=False,verbose_name='Total', default=None)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)#
    def __str__(self):
        return self.titulo  + ",R$" + str(self.valor) +"," + "R$" +str(self.total_pago)

        #calculo
    def save(self, *args, **kwargs):
        self.total_pago = self.valor
        #self.total_pago.save()
        return super (Despesas, self).save(*args, **kwargs)
       
#https://jaketrent.com/post/add-migration-nonnull-foreignkey-field-django
