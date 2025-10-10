from django.contrib import admin
from .models import Empresa, Transportador


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'cnpj')
    list_filter = ('tipo',)
    search_fields = ('nome', 'cnpj')
    readonly_fields = ()

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'tipo', 'cnpj')
        }),
    )


    actions = ['aprovar_cadastros', 'recusar_cadastros']

    def aprovar_cadastros(self, request, queryset):
        from backend.users.models import User
        count = 0
        for empresa in queryset.filter(status='PENDENTE'):
            # Criar usuário
            user = User.objects.create_user(
                username=empresa.email,
                email=empresa.email,
                password="senha_temporaria_123",  # Enviar email para redefinir
                is_active=True
            )
            user.role = empresa.tipo_empresa
            user.save()
            empresa.status = 'APROVADO'
            empresa.save()
            count += 1
        self.message_user(request, f'{count} cadastro(s) aprovado(s) com sucesso!')
    aprovar_cadastros.short_description = 'Aprovar cadastros selecionados'

    def recusar_cadastros(self, request, queryset):
        count = queryset.filter(status='PENDENTE').update(status='RECUSADO')
        self.message_user(request, f'{count} cadastro(s) recusado(s)!')
    recusar_cadastros.short_description = 'Recusar cadastros selecionados'


@admin.register(Transportador)
class TransportadorAdmin(admin.ModelAdmin):
    list_display = (
        'razao', 'cnpj', 'email', 'telefone', 'status', 'criado_em'
    )
    list_filter = ('status', 'criado_em')
    search_fields = ('razao', 'cnpj', 'email')
    readonly_fields = ('criado_em',)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('razao', 'cnpj', 'telefone', 'email')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Datas', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )

    actions = ['aprovar_cadastros', 'recusar_cadastros']

    def aprovar_cadastros(self, request, queryset):
        from backend.users.models import User
        count = 0
        for transportador in queryset.filter(status='PENDENTE'):
            # Criar usuário
            user = User.objects.create_user(
                username=transportador.email,
                email=transportador.email,
                password="senha_temporaria_123",  # Enviar email para redefinir
                is_active=True
            )
            user.role = 'transportador'
            user.save()
            transportador.status = 'APROVADO'
            transportador.save()
            count += 1
        self.message_user(request, f'{count} cadastro(s) aprovado(s) com sucesso!')
    aprovar_cadastros.short_description = 'Aprovar cadastros selecionados'

    def recusar_cadastros(self, request, queryset):
        count = queryset.filter(status='PENDENTE').update(status='RECUSADO')
        self.message_user(request, f'{count} cadastro(s) recusado(s)!')
    recusar_cadastros.short_description = 'Recusar cadastros selecionados'