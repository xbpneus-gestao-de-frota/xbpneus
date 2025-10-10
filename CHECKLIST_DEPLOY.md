# ✅ Checklist de Deploy - Sistema XBPneus

Use este checklist para garantir que todos os passos sejam seguidos corretamente.

---

## 📋 Pré-Deploy

### GitHub

- [ ] Repositório criado no GitHub
- [ ] Git configurado localmente (`git config user.name` e `user.email`)
- [ ] Remote adicionado (`git remote add origin`)
- [ ] `.gitignore` verificado
- [ ] Arquivos sensíveis não commitados (db.sqlite3, .env, node_modules)
- [ ] README.md criado
- [ ] Commit inicial feito
- [ ] Push para GitHub concluído (`git push -u origin main`)

### Código

- [ ] Testes executados e aprovados (10/10)
- [ ] Páginas de autenticação preservadas (Login, Cadastro, Pós-Cadastro)
- [ ] Assets de autenticação presentes (mascotes, logos)
- [ ] Validações de negócio implementadas
- [ ] `render.yaml` configurado
- [ ] `build.sh` executável (`chmod +x build.sh`)
- [ ] `requirements-production.txt` atualizado
- [ ] `config/production.py` configurado

### Configurações

- [ ] `DEBUG = False` em production.py
- [ ] `ALLOWED_HOSTS` definido
- [ ] Security headers configurados (HSTS, XSS, CSRF)
- [ ] CORS configurado
- [ ] Email settings configurados (opcional)

---

## 🚀 Deploy no Render

### Conta e Conexão

- [ ] Conta criada no Render (https://render.com)
- [ ] Email confirmado
- [ ] GitHub conectado ao Render
- [ ] Repositório `xbpneus` selecionado

### Blueprint

- [ ] Blueprint aplicado (render.yaml)
- [ ] Serviços criados automaticamente:
  - [ ] Backend (xbpneus-backend)
  - [ ] Frontend (xbpneus-frontend)
  - [ ] PostgreSQL (xbpneus-db)
  - [ ] Redis (xbpneus-redis)

### Variáveis de Ambiente - Backend

- [ ] `DJANGO_SETTINGS_MODULE=config.production`
- [ ] `SECRET_KEY` (gerado automaticamente)
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` (URL do backend e frontend)
- [ ] `DATABASE_URL` (conectado automaticamente)
- [ ] `REDIS_URL` (conectado automaticamente)
- [ ] `EMAIL_HOST` (opcional)
- [ ] `EMAIL_PORT` (opcional)
- [ ] `EMAIL_HOST_USER` (opcional)
- [ ] `EMAIL_HOST_PASSWORD` (opcional)
- [ ] `CORS_ALLOWED_ORIGINS` (URL do frontend)

### Variáveis de Ambiente - Frontend

- [ ] `NODE_VERSION=22.13.0`
- [ ] `VITE_API_BASE` (URL do backend)

### Deploy

- [ ] Deploy iniciado
- [ ] Logs acompanhados
- [ ] Build concluído sem erros
- [ ] Migrações executadas
- [ ] Serviços iniciados

---

## ✅ Pós-Deploy

### Verificação de Serviços

- [ ] Backend respondendo: `https://xbpneus-backend.onrender.com/healthz/`
  - Deve retornar: `{"status": "ok"}`
- [ ] Frontend carregando: `https://xbpneus-frontend.onrender.com`
- [ ] Admin acessível: `https://xbpneus-backend.onrender.com/admin`
- [ ] API Docs acessível: `https://xbpneus-backend.onrender.com/api/schema/swagger-ui/`

### Criar Superusuário

- [ ] Acessar Shell do backend no Render
- [ ] Executar: `python manage.py createsuperuser`
- [ ] Email: admin@xbpneus.com
- [ ] Senha: (senha forte)
- [ ] Login no admin funcionando

### Testes Funcionais

- [ ] **Login**
  - [ ] Página carrega corretamente
  - [ ] Cores preservadas (fundo cinza, botão azul)
  - [ ] Mascotes visíveis e com tamanho correto
  - [ ] Login funciona com credenciais válidas
  - [ ] Erro exibido com credenciais inválidas
  - [ ] Texto dos inputs fica azul escuro após digitação

- [ ] **Cadastro**
  - [ ] Página carrega corretamente
  - [ ] Cores preservadas
  - [ ] Mascotes com mesmo tamanho do login
  - [ ] Campo "Tipo de Cliente" VISÍVEL
  - [ ] Campos de senha VISÍVEIS (não transparentes)
  - [ ] Cadastro funciona
  - [ ] Texto dos inputs fica azul escuro após digitação

- [ ] **Pós-Cadastro**
  - [ ] Página carrega após cadastro
  - [ ] Fundo ESTÁTICO (não animado)
  - [ ] Cores preservadas
  - [ ] Mensagem de sucesso exibida
  - [ ] Redirecionamento funciona

- [ ] **Dashboard**
  - [ ] Dashboard carrega após login
  - [ ] Cards de estatísticas exibidos
  - [ ] Ações rápidas funcionando
  - [ ] Alertas visíveis
  - [ ] Navegação funciona

- [ ] **Veículos**
  - [ ] Lista de veículos carrega
  - [ ] Criar veículo funciona
  - [ ] Validações funcionando (placa, ano, km)
  - [ ] Editar veículo funciona
  - [ ] Excluir veículo funciona

- [ ] **Pneus**
  - [ ] Lista de pneus carrega
  - [ ] Criar pneu funciona
  - [ ] Validações funcionando (código, medida, DOT)
  - [ ] Editar pneu funciona
  - [ ] Excluir pneu funciona

### Testes de API

- [ ] Endpoint de login: `POST /api/transportador/login/`
- [ ] Endpoint de dashboard: `GET /api/transportador/dashboard/`
- [ ] Endpoint de veículos: `GET /api/transportador/frota/veiculos/`
- [ ] Criar veículo: `POST /api/transportador/frota/veiculos/`
- [ ] Endpoint de pneus: `GET /api/transportador/pneus/pneus/`
- [ ] Criar pneu: `POST /api/transportador/pneus/pneus/`

### Verificação Visual

- [ ] **Login**
  - [ ] Fundo: `bg-gray-100` (cinza claro)
  - [ ] Mascotes: Tamanho correto
  - [ ] Logo: Dimensões corretas
  - [ ] Botão: Gradiente azul
  - [ ] Inputs: Texto azul escuro após digitação

- [ ] **Cadastro**
  - [ ] Fundo: `bg-gray-100`
  - [ ] Mascotes: Mesmo tamanho do login
  - [ ] Campo "Tipo de Cliente": VISÍVEL
  - [ ] Campos de senha: VISÍVEIS
  - [ ] Inputs: Texto azul escuro após digitação

- [ ] **Pós-Cadastro**
  - [ ] Fundo: ESTÁTICO (não animado)
  - [ ] Imagem de sucesso: Visível
  - [ ] Card: Branco com sombra
  - [ ] Botão: Gradiente azul

### Performance

- [ ] Tempo de resposta da API < 500ms
- [ ] Tempo de carregamento do frontend < 3s
- [ ] Imagens carregando corretamente
- [ ] Sem erros no console do navegador

### Segurança

- [ ] HTTPS habilitado
- [ ] HSTS headers ativos
- [ ] CSRF protection funcionando
- [ ] CORS configurado corretamente
- [ ] Tokens JWT funcionando
- [ ] Refresh tokens funcionando

---

## 📊 Monitoramento

### Logs

- [ ] Logs do backend acessíveis no Render
- [ ] Logs do frontend acessíveis no Render
- [ ] Sem erros críticos nos logs
- [ ] Avisos revisados

### Métricas

- [ ] Uptime > 99%
- [ ] Tempo de resposta médio < 500ms
- [ ] Uso de memória normal
- [ ] Uso de CPU normal

---

## 🐛 Troubleshooting

Se algo não funcionar:

- [ ] Verificar logs no Render
- [ ] Verificar variáveis de ambiente
- [ ] Verificar conexão com banco de dados
- [ ] Verificar conexão com Redis
- [ ] Consultar [RELATORIO_DEPLOY_GITHUB_RENDER.md](RELATORIO_DEPLOY_GITHUB_RENDER.md)
- [ ] Consultar seção Troubleshooting do relatório

---

## 📝 Documentação

- [ ] README.md atualizado
- [ ] RELATORIO_DEPLOY_GITHUB_RENDER.md revisado
- [ ] PRESERVACAO_PAGINAS_AUTH.md consultado
- [ ] DEPLOY_GUIDE.md disponível

---

## 🎉 Deploy Concluído

Quando todos os itens estiverem marcados:

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              ✅ DEPLOY CONCLUÍDO COM SUCESSO!               ║
║                                                              ║
║              Sistema 100% Funcional em Produção             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

- [ ] **DEPLOY FINALIZADO E VERIFICADO** ✅

---

**Data do Deploy:** ___/___/______  
**Responsável:** _________________  
**URLs:**
- Frontend: _________________
- Backend: _________________
- Admin: _________________
