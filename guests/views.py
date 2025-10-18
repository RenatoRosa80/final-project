from django.shortcuts import render, redirect
from .models import Pessoa

# Create your views here.

def home(request):
    pessoas = Pessoa.objects.all()
    return render(request,"index.html",{"pessoas":pessoas})

def salvar(request):
    vnome = request.POST.get("nome")
    vemail = request.POST.get("email")
    vphone = request.POST.get("phone")
    vconvidados = request.POST.get("convidados")
    vnascimento = request.POST.get("nascimento")
    vhorario = request.POST.get("horario")
    vsolicitacao_especial = request.POST.get("solicitacao_especial")
    Pessoa.objects.create(nome=vnome, email=vemail, phone=vphone, guests=vconvidados, nascimento=vnascimento, horario=vhorario, solicitacao_especial=vsolicitacao_especial)
    pessoas = Pessoa.objects.all
    return render(request,"index.html", {"pessoas":pessoas})

def delete(request, id):
    pessoa = Pessoa.objects.get(id=id)
    pessoa.delete()
    return redirect(home)

def edite(request, id):
    pessoa = Pessoa.objects.get(id = id)
    return render(request,"update.html",{"pessoa":pessoa})

def update(request, id):
    vnome = request.POST.get("nome")
    vemail = request.POST.get("email")
    vtelefone = request.POST.get("telefone")
    vconvidados = request.POST.get("convidados")
    vnascimento = request.POST.get("nacimento")
    vhorario = request.POST.get("horario")
    vsolicitacao_especial = request.POST.get("solicitacao_especial")
    pessoa = Pessoa.objects.get(id = id)
    pessoa.nome = vnome
    pessoa.email = vemail
    pessoa.telefone = vtelefone
    pessoa.convidados = vconvidados
    pessoa.nascimento = vnascimento
    pessoa.horario = vhorario
    pessoa.solicitacao_especial = vsolicitacao_especial
    pessoa.save()
    return redirect(home)




