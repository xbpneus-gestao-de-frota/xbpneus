import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
try:
    user = User.objects.get(username='admin')
    user.set_password('admin')
    user.save()
    print("Senha do superusuário 'admin' definida com sucesso.")
except User.DoesNotExist:
    print("Erro: Superusuário 'admin' não encontrado.")

