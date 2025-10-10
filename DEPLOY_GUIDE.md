# Guia de Deploy - Sistema XBPneus

## 📋 Pré-requisitos

- Servidor Linux (Ubuntu 22.04 LTS recomendado)
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Nginx (opcional)
- Docker e Docker Compose (opcional)

---

## 🚀 Opção 1: Deploy com Docker (Recomendado)

### 1. Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt install docker-compose -y

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
```

### 2. Clonar o Projeto

```bash
git clone https://github.com/seu-usuario/xbpneus.git
cd xbpneus
```

### 3. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.production.example .env

# Editar com valores reais
nano .env
```

**Importante:** Gere uma SECRET_KEY segura:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Iniciar os Containers

```bash
# Build e start
docker-compose up -d --build

# Verificar logs
docker-compose logs -f web

# Executar migrações
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Coletar arquivos estáticos
docker-compose exec web python manage.py collectstatic --noinput
```

### 5. Verificar Status

```bash
# Ver containers rodando
docker-compose ps

# Testar aplicação
curl http://localhost:8000/healthz/
```

---

## 🔧 Opção 2: Deploy Manual

### 1. Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib redis-server nginx git
```

### 2. Configurar PostgreSQL

```bash
# Acessar PostgreSQL
sudo -u postgres psql

# Criar banco e usuário
CREATE DATABASE xbpneus;
CREATE USER xbpneus WITH PASSWORD 'senha-forte-aqui';
ALTER ROLE xbpneus SET client_encoding TO 'utf8';
ALTER ROLE xbpneus SET default_transaction_isolation TO 'read committed';
ALTER ROLE xbpneus SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE xbpneus TO xbpneus;
\q
```

### 3. Configurar Aplicação

```bash
# Criar diretório
sudo mkdir -p /var/www/xbpneus
cd /var/www/xbpneus

# Clonar projeto
git clone https://github.com/seu-usuario/xbpneus.git .

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements-production.txt

# Configurar variáveis de ambiente
cp .env.production.example .env
nano .env

# Executar migrações
python manage.py migrate --settings=config.production

# Coletar arquivos estáticos
python manage.py collectstatic --noinput --settings=config.production

# Criar superusuário
python manage.py createsuperuser --settings=config.production
```

### 4. Configurar Gunicorn

```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/xbpneus.service
```

Conteúdo:
```ini
[Unit]
Description=XBPneus Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/xbpneus
Environment="PATH=/var/www/xbpneus/venv/bin"
EnvironmentFile=/var/www/xbpneus/.env
ExecStart=/var/www/xbpneus/venv/bin/gunicorn \
          --workers 4 \
          --threads 2 \
          --bind unix:/var/www/xbpneus/xbpneus.sock \
          --access-logfile /var/log/xbpneus/access.log \
          --error-logfile /var/log/xbpneus/error.log \
          --log-level info \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Criar diretório de logs
sudo mkdir -p /var/log/xbpneus
sudo chown www-data:www-data /var/log/xbpneus

# Iniciar serviço
sudo systemctl start xbpneus
sudo systemctl enable xbpneus
sudo systemctl status xbpneus
```

### 5. Configurar Nginx

```bash
# Criar configuração
sudo nano /etc/nginx/sites-available/xbpneus
```

Conteúdo:
```nginx
server {
    listen 80;
    server_name xbpneus.com www.xbpneus.com;

    client_max_body_size 100M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/xbpneus/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/xbpneus/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/xbpneus/xbpneus.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/xbpneus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Configurar SSL com Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado
sudo certbot --nginx -d xbpneus.com -d www.xbpneus.com

# Renovação automática já está configurada
```

### 7. Configurar Worker RQ

```bash
# Criar serviço
sudo nano /etc/systemd/system/xbpneus-worker.service
```

Conteúdo:
```ini
[Unit]
Description=XBPneus RQ Worker
After=network.target redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/xbpneus
Environment="PATH=/var/www/xbpneus/venv/bin"
EnvironmentFile=/var/www/xbpneus/.env
ExecStart=/var/www/xbpneus/venv/bin/python manage.py rqworker default

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar worker
sudo systemctl start xbpneus-worker
sudo systemctl enable xbpneus-worker
```

---

## 🔒 Segurança

### Firewall

```bash
# Configurar UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Backup Automático

```bash
# Criar script de backup
sudo nano /usr/local/bin/backup-xbpneus.sh
```

Conteúdo:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/xbpneus"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup do banco de dados
pg_dump -U xbpneus xbpneus | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup dos arquivos de media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/xbpneus/media/

# Manter apenas últimos 7 dias
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup concluído: $DATE"
```

```bash
# Tornar executável
sudo chmod +x /usr/local/bin/backup-xbpneus.sh

# Adicionar ao cron (diariamente às 2h)
sudo crontab -e
# Adicionar linha:
0 2 * * * /usr/local/bin/backup-xbpneus.sh >> /var/log/xbpneus/backup.log 2>&1
```

---

## 📊 Monitoramento

### Logs

```bash
# Logs do Django
tail -f /var/log/xbpneus/error.log
tail -f /var/log/xbpneus/access.log

# Logs do sistema
sudo journalctl -u xbpneus -f
sudo journalctl -u xbpneus-worker -f

# Logs do Nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### Health Check

```bash
# Verificar status dos serviços
sudo systemctl status xbpneus
sudo systemctl status xbpneus-worker
sudo systemctl status postgresql
sudo systemctl status redis
sudo systemctl status nginx

# Testar endpoint
curl https://xbpneus.com/healthz/
```

---

## 🔄 Atualização

```bash
# Parar serviços
sudo systemctl stop xbpneus xbpneus-worker

# Atualizar código
cd /var/www/xbpneus
git pull origin main

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar dependências
pip install -r requirements-production.txt

# Executar migrações
python manage.py migrate --settings=config.production

# Coletar arquivos estáticos
python manage.py collectstatic --noinput --settings=config.production

# Reiniciar serviços
sudo systemctl start xbpneus xbpneus-worker
sudo systemctl restart nginx
```

---

## 🐛 Troubleshooting

### Erro 502 Bad Gateway

```bash
# Verificar se Gunicorn está rodando
sudo systemctl status xbpneus

# Verificar logs
tail -f /var/log/xbpneus/error.log

# Reiniciar serviço
sudo systemctl restart xbpneus
```

### Erro de Conexão com Banco de Dados

```bash
# Verificar PostgreSQL
sudo systemctl status postgresql

# Testar conexão
psql -U xbpneus -d xbpneus -h localhost
```

### Problemas com Arquivos Estáticos

```bash
# Recoletar arquivos estáticos
python manage.py collectstatic --clear --noinput --settings=config.production

# Verificar permissões
sudo chown -R www-data:www-data /var/www/xbpneus/staticfiles
```

---

## 📞 Suporte

Para suporte adicional, entre em contato:
- Email: suporte@xbpneus.com
- Documentação: https://docs.xbpneus.com

---

**Última atualização:** 10 de Outubro de 2025

