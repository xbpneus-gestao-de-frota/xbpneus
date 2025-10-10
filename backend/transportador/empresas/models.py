from django.db import models

class Empresa(models.Model):
    TIPOS = [
        ('transportador', 'Transportador'),
        ('revenda', 'Revenda'),
        ('borracharia', 'Borracharia'),
        ('recapagem', 'Recapagem'),
    ]
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    cnpj = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nome} ({self.tipo})"



class Transportador(models.Model):
    """Cadastro de transportador aguardando aprovação"""
    cnpj = models.CharField(max_length=20, unique=True)
    razao = models.CharField(max_length=200)
    estado = models.CharField(max_length=2, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    status = models.CharField(
        max_length=20,
        choices=[("PENDENTE", "Pendente"), ("APROVADO", "Aprovado"), ("RECUSADO", "Recusado")],
        default="PENDENTE",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.razao

