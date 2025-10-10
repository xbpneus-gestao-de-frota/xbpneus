# Guia de Instalação e Execução - Sistema XBPneus

## 📋 Visão Geral

O Sistema XBPneus é uma aplicação completa para gestão de transportadoras, com funcionalidades para gerenciamento de frota, pneus, manutenção, custos, viagens e muito mais.

**Tecnologias:**
- **Backend:** Django 4.2+ com Django REST Framework
- **Frontend:** React 18 com Vite, TailwindCSS e Zustand
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (produção)
- **Cache/Jobs:** Redis

---

## ✅ Pré-requisitos

Certifique-se de ter instalado:

- **Python 3.11+**
- **Node.js 22+** e npm
- **Redis Server**
- **Git** (opcional)

---

## 🚀 Instalação das Dependências

### 1. Backend (Python/Django)

```bash
cd /home/ubuntu/upload
pip3 install -r requirements.txt
```

**Dependências principais:**
- Django 4.2+
- Django REST Framework
- djangorestframework-simplejwt (autenticação JWT)
- django-cors-headers
- dj-database-url
- django-rq (jobs em background)
- redis
- whitenoise (arquivos estáticos)
- gunicorn (servidor WSGI)

### 2. Frontend (React/Node.js)

```bash
cd /home/ubuntu/upload/frontend
npm install
```

**Dependências principais:**
- React 18
- React Router DOM
- Vite (build tool)
- TailwindCSS
- Axios (HTTP client)
- Zustand (state management)
- Recharts (gráficos)
- Lucide React (ícones)

---

## ⚙️ Configuração do Ambiente

### 1. Arquivo `.env`

O arquivo `.env` já está configurado no diretório raiz:

```bash
# Backend
DJANGO_DEBUG=1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Database (ajuste conforme necessário)
# DATABASE_URL=postgres://user:pass@localhost:5432/xbpneus
```

### 2. Banco de Dados

O sistema já possui um banco de dados SQLite configurado (`db.sqlite3`). As migrações foram aplicadas automaticamente.

Para resetar o banco de dados:

```bash
cd /home/ubuntu/upload
rm db.sqlite3
python3.11 manage.py migrate
```

### 3. Redis

Certifique-se de que o Redis está rodando:

```bash
redis-server --daemonize yes
redis-cli ping  # Deve retornar "PONG"
```

---

## 🎯 Executando o Sistema

### Método 1: Script Automático (Recomendado)

```bash
cd /home/ubuntu/upload
./start_system.sh
```

Este script irá:
1. Verificar e iniciar o Redis
2. Iniciar o backend Django na porta 8000
3. Iniciar o frontend React na porta 3000
4. Exibir as URLs de acesso

Para parar o sistema:

```bash
./stop_system.sh
```

### Método 2: Manual

**Terminal 1 - Backend:**
```bash
cd /home/ubuntu/upload
python3.11 manage.py runserver 0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
cd /home/ubuntu/upload/frontend
npm run dev
```

**Terminal 3 - Redis (se não estiver rodando):**
```bash
redis-server
```

---

## 🌐 URLs de Acesso

Após iniciar o sistema:

- **Frontend (Interface):** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **Admin Django:** http://localhost:8000/admin
- **Documentação API (Swagger):** http://localhost:8000/api/schema/swagger-ui/
- **Documentação API (ReDoc):** http://localhost:8000/api/schema/redoc/

---

## 👤 Usuários e Autenticação

### Criar Superusuário (Admin)

```bash
cd /home/ubuntu/upload
python3.11 manage.py createsuperuser
```

Siga as instruções para criar um usuário administrador.

### Usuários de Teste

Se o sistema possui dados de teste (seed), você pode verificar os usuários disponíveis nos arquivos:
- `seed_complete.py`
- `seed_minimal.py`
- `test_100_funcional.py`

---

## 📊 Estrutura do Projeto

```
xbpneus_project_final/
├── backend/                    # Aplicações Django
│   ├── transportador/          # Módulo principal
│   │   ├── frota/             # Gestão de veículos
│   │   ├── pneus/             # Gestão de pneus
│   │   ├── manutencao/        # Manutenções
│   │   ├── custos/            # Controle de custos
│   │   ├── viagens/           # Gestão de viagens
│   │   ├── combustivel/       # Abastecimento
│   │   ├── multas/            # Multas
│   │   ├── estoque/           # Estoque
│   │   └── ...                # Outros módulos
│   ├── borracharia/           # Módulo borracharia
│   ├── motorista/             # Módulo motorista
│   ├── revenda/               # Módulo revenda
│   └── recapagem/             # Módulo recapagem
├── frontend/                   # Aplicação React
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── pages/             # Páginas
│   │   ├── api/               # Chamadas API
│   │   └── layouts/           # Layouts
│   └── public/                # Arquivos estáticos
├── config/                     # Configurações Django
├── data/                       # Dados CSV
├── manage.py                   # CLI Django
├── requirements.txt            # Dependências Python
├── start_system.sh            # Script de inicialização
├── stop_system.sh             # Script para parar
└── .env                       # Variáveis de ambiente
```

---

## 🧪 Testes

### Testes Funcionais

O projeto inclui vários scripts de teste:

```bash
# Teste completo (100% funcional)
python3.11 test_100_funcional.py

# Teste de fluxo de usuário
python3.11 test_user_flow.py

# Teste de transportador
python3.11 test_transportador.py

# Teste pós-login
python3.11 test_pos_login.py
```

### Testes Django

```bash
cd /home/ubuntu/upload
python3.11 manage.py test
```

---

## 🔧 Comandos Úteis

### Backend (Django)

```bash
# Criar migrações
python3.11 manage.py makemigrations

# Aplicar migrações
python3.11 manage.py migrate

# Coletar arquivos estáticos
python3.11 manage.py collectstatic

# Shell interativo
python3.11 manage.py shell

# Criar superusuário
python3.11 manage.py createsuperuser
```

### Frontend (React)

```bash
# Modo desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview do build
npm run preview

# Lint
npm run lint
```

### Redis

```bash
# Iniciar Redis
redis-server --daemonize yes

# Verificar status
redis-cli ping

# Parar Redis
redis-cli shutdown

# Monitor em tempo real
redis-cli monitor
```

---

## 📝 Logs

Os logs do sistema são salvos em:

- **Backend:** `backend.log`
- **Frontend:** `frontend.log`

Para visualizar em tempo real:

```bash
# Backend
tail -f backend.log

# Frontend
tail -f frontend.log
```

---

## 🐛 Solução de Problemas

### Redis não está rodando

```bash
redis-server --daemonize yes
```

### Porta 8000 ou 3000 já em uso

```bash
# Verificar processos
lsof -i :8000
lsof -i :3000

# Matar processo
kill -9 <PID>
```

### Erro de dependências Python

```bash
pip3 install -r requirements.txt --force-reinstall
```

### Erro de dependências Node.js

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Erro de migrações

```bash
python3.11 manage.py migrate --fake
python3.11 manage.py migrate
```

---

## 📚 Documentação Adicional

- **Relatório Final:** `Relatório_Final_-_Sistema_XBPneus_90%_Funcional.pdf`
- **Resultados de Teste:** `resultado_teste_100.txt`
- **Scripts de Seed:** `seed_complete.py`, `seed_minimal.py`

---

## 🔐 Segurança

Para produção, certifique-se de:

1. Alterar `SECRET_KEY` no `.env`
2. Definir `DJANGO_DEBUG=0`
3. Configurar `ALLOWED_HOSTS` adequadamente
4. Usar PostgreSQL ao invés de SQLite
5. Configurar HTTPS
6. Revisar configurações de CORS

---

## 📞 Suporte

Para problemas ou dúvidas, consulte:
- Documentação da API: http://localhost:8000/api/schema/swagger-ui/
- Logs do sistema: `backend.log` e `frontend.log`
- Relatório Final do projeto

---

**Sistema XBPneus - Gestão Completa para Transportadoras**

*Desenvolvido com Django, React e tecnologias modernas*

