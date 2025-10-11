import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email="admin@xbpneus.com").exists():
    admin_user = User.objects.create_superuser(
        email="admin@xbpneus.com", 
        password="Admin@123", 
        nome_razao_social="Admin", 
        cnpj="00.000.000/0001-00"
    )
    # Aprovar o admin por padrão
    admin_user.aprovado = True
    admin_user.save()
    print("Superusuário 'admin' criado com sucesso.")
    print("Email: admin@xbpneus.com")
    print("Senha: Admin@123")
else:
    # Atualizar senha e aprovar se já existir
    admin_user = User.objects.get(email="admin@xbpneus.com")
    admin_user.set_password("Admin@123")
    admin_user.aprovado = True
    admin_user.save()
    print("Superusuário 'admin' já existe. Senha atualizada para Admin@123 e aprovado.")

