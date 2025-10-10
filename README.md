# 🚚 Sistema XBPneus

Sistema completo de gestão de frotas e pneus para transportadoras.

![Status](https://img.shields.io/badge/status-production%20ready-success)
![Version](https://img.shields.io/badge/version-2.0-blue)
![Tests](https://img.shields.io/badge/tests-100%25%20passing-success)

---

## 📋 Sobre o Projeto

O **XBPneus** é um sistema completo para gestão de frotas de veículos e controle de pneus, desenvolvido para atender transportadoras de todos os portes (de 1 a 3000+ caminhões).

### Principais Funcionalidades

- 🚛 **Gestão de Frota** - CRUD completo de veículos com validações robustas
- 🛞 **Gestão de Pneus** - Controle de estoque, aplicações e recapagens
- 🔧 **Manutenção** - Ordens de serviço e histórico de manutenções
- 📦 **Estoque** - Movimentações e controle de entrada/saída
- 📊 **Dashboard** - Métricas em tempo real e alertas inteligentes
- 🔐 **Autenticação** - JWT com refresh tokens
- 📱 **Responsivo** - Interface adaptável a todos os dispositivos

---

## 🏗️ Arquitetura

### Backend
- **Framework:** Django 4.2 + Django REST Framework
- **Banco de Dados:** PostgreSQL 15
- **Cache:** Redis 7
- **Autenticação:** JWT (Simple JWT)
- **Servidor:** Gunicorn
- **Documentação:** drf-spectacular (Swagger/OpenAPI)

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite 5
- **Estilização:** TailwindCSS 3
- **Ícones:** Lucide React
- **HTTP Client:** Axios
- **Estado:** Zustand

---

## 🚀 Deploy

### Opção 1: Render (Recomendado)

O sistema está configurado para deploy automático no Render via Blueprint.

```bash
# 1. Push para GitHub
git push origin main

# 2. No Render, conecte o repositório
# 3. Aplique o Blueprint (render.yaml)
# 4. Configure as variáveis de ambiente
# 5. Deploy automático!
```

**Documentação Completa:** [RELATORIO_DEPLOY_GITHUB_RENDER.md](RELATORIO_DEPLOY_GITHUB_RENDER.md)

### Opção 2: Docker

```bash
# Build e start
docker-compose up -d --build

# Migrações
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser
```

### Opção 3: Manual

Consulte [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) para instruções detalhadas.

---

## 💻 Desenvolvimento Local

### Pré-requisitos

- Python 3.11+
- Node.js 22+
- PostgreSQL 15+ (ou SQLite para dev)
- Redis 7+

### Instalação

```bash
# 1. Clonar repositório
git clone https://github.com/SEU_USUARIO/xbpneus.git
cd xbpneus

# 2. Backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# 3. Frontend
cd frontend
npm install

# 4. Iniciar (em terminais separados)
# Terminal 1 - Backend
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### URLs de Desenvolvimento

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **Admin Django:** http://localhost:8000/admin
- **API Docs:** http://localhost:8000/api/schema/swagger-ui/

---

## 🧪 Testes

### Executar Testes

```bash
# Testes funcionais
python test_100_funcional.py

# Testes de validação
python test_validations.py

# Testes Django
python manage.py test
```

### Cobertura Atual

- ✅ **10/10** testes funcionais aprovados (100%)
- ✅ **10/10** testes de validação aprovados (100%)

---

## 📚 Documentação

- [RELATORIO_DEPLOY_GITHUB_RENDER.md](RELATORIO_DEPLOY_GITHUB_RENDER.md) - Guia completo de deploy
- [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) - Deploy manual detalhado
- [PRESERVACAO_PAGINAS_AUTH.md](PRESERVACAO_PAGINAS_AUTH.md) - Diretrizes de UI/UX
- [RELATORIO_100_FUNCIONAL.md](RELATORIO_100_FUNCIONAL.md) - Sistema 100% funcional
- [RELATORIO_DESENVOLVIMENTO_COMPLETO.md](RELATORIO_DESENVOLVIMENTO_COMPLETO.md) - Desenvolvimento completo

---

## 🎨 Design e UI/UX

### ⚠️ Páginas Protegidas

As seguintes páginas **NÃO devem ser modificadas** em cores, dimensões e formatos:

- ✅ Login (`/frontend/src/pages/Login.jsx`)
- ✅ Cadastro (`/frontend/src/pages/Cadastro.jsx`)
- ✅ Pós-Cadastro (`/frontend/src/pages/PosCadastro.jsx`)

**Consulte:** [PRESERVACAO_PAGINAS_AUTH.md](PRESERVACAO_PAGINAS_AUTH.md)

### Paleta de Cores

```css
--primary-blue: #1e40af;
--primary-blue-light: #3b82f6;
--primary-blue-dark: #1e3a8a;
--gradient-button: linear-gradient(to right, #3b82f6, #1e40af);
```

---

## 🔒 Segurança

- ✅ HTTPS obrigatório em produção
- ✅ HSTS headers configurados
- ✅ CSRF protection habilitado
- ✅ XSS protection habilitado
- ✅ SQL injection protection (ORM)
- ✅ Rate limiting (django-axes)
- ✅ JWT com refresh tokens
- ✅ Validações robustas de entrada

---

## 📦 Estrutura do Projeto

```
xbpneus/
├── backend/                    # Backend Django
│   ├── common/                # Módulos comuns
│   ├── transportador/         # Módulo transportador
│   │   ├── frota/            # Gestão de frota
│   │   ├── pneus/            # Gestão de pneus
│   │   ├── estoque/          # Gestão de estoque
│   │   └── ... (44 módulos)
│   └── ...
├── config/                     # Configurações Django
│   ├── settings.py           # Configurações base
│   ├── production.py         # Configurações de produção
│   └── ...
├── frontend/                   # Frontend React
│   ├── src/
│   │   ├── pages/            # Páginas
│   │   ├── components/       # Componentes
│   │   └── api/              # API client
│   └── public/
│       └── static/           # Assets estáticos
├── .gitignore
├── build.sh                    # Script de build
├── render.yaml                 # Configuração Render
├── requirements.txt            # Dependências Python
├── requirements-production.txt # Dependências de produção
├── Dockerfile                  # Container Docker
├── docker-compose.yml          # Orquestração Docker
└── README.md                   # Este arquivo
```

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

**Importante:** Não modifique as páginas de autenticação sem aprovação.

---

## 📝 Licença

Este projeto é proprietário e confidencial.

---

## 👥 Equipe

- **Desenvolvimento:** Equipe XBPneus
- **Design:** Equipe XBPneus
- **Testes:** Equipe XBPneus

---

## 📞 Suporte

Para suporte, entre em contato:
- **Email:** suporte@xbpneus.com
- **Documentação:** [docs/](docs/)

---

## 🎯 Status do Projeto

- ✅ Backend 100% funcional
- ✅ Frontend completo
- ✅ Validações de negócio implementadas
- ✅ Testes 100% aprovados
- ✅ Pronto para produção
- ✅ Documentação completa

---

## 🏆 Conquistas

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         ✅ SISTEMA 100% FUNCIONAL                           ║
║         ✅ PRONTO PARA PRODUÇÃO                             ║
║         ✅ 10/10 TESTES APROVADOS                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

**Desenvolvido com ❤️ pela Equipe XBPneus**

