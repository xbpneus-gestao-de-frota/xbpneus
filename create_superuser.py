import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email="admin@xbpneus.com").exists():
    User.objects.create_superuser(email="admin@xbpneus.com", password="Admin@123", nome_razao_social="Admin", cnpj="00.000.000/0001-00")
    print("Superusuário \'admin\' criado com sucesso.")
else:
    print("Superusuário \'admin\' já existe.")

