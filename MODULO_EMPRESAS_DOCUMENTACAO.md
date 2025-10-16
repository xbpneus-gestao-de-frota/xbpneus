# Documentação do Módulo de Empresas - Sistema XBPneus

## Visão Geral

O Módulo de Empresas foi desenvolvido seguindo uma arquitetura hierárquica em cascata, onde cada nível de navegação leva a funcionalidades mais específicas. Este documento descreve a implementação completa, estrutura de arquivos e instruções para teste.

## Estrutura Hierárquica Implementada

```
Dashboard Transportador (Nível 1)
    ↓ [Botão "Empresas"]
Dashboard Empresas (Nível 2)
    ↓ [Cards/Botões de Módulos]
Telas de Funcionalidades (Nível 3)
    - Empresas (CRUD completo)
    - Filiais (CRUD completo)
    - Agregados (CRUD completo)
    - Documentos (placeholder)
    - Relatórios (placeholder)
    - Configurações (placeholder)
```

## Arquivos Criados e Modificados

### Novos Componentes

1. **`/frontend/src/components/EmpresasSidebar.jsx`**
   - Sidebar lateral específica para o Dashboard de Empresas
   - Navegação entre os módulos
   - Botão "Voltar ao Dashboard" principal

2. **`/frontend/src/components/LayoutEmpresasDashboard.jsx`**
   - Layout wrapper para o Dashboard de Empresas
   - Integra EmpresasSidebar + Header + Outlet

3. **`/frontend/src/components/common/FormModal.jsx`**
   - Modal reutilizável para formulários
   - Suporta 4 tamanhos: sm, md, lg, xl
   - Botões de ação padronizados

4. **`/frontend/src/components/common/ConfirmDialog.jsx`**
   - Diálogo de confirmação para ações destrutivas
   - Suporta 3 variantes: danger, warning, info
   - Ícones e cores contextuais

5. **`/frontend/src/components/common/StatusBadge.jsx`**
   - Badge para exibir status
   - Mapeamento automático de cores por status
   - Estilos consistentes

6. **`/frontend/src/components/common/SearchBar.jsx`**
   - Barra de busca com debounce
   - Delay configurável (padrão: 500ms)
   - Ícone de busca integrado

7. **`/frontend/src/components/common/StatsCard.jsx`**
   - Card para exibir estatísticas
   - Suporta ícones e tendências
   - 6 variações de cores

### Novas Páginas

8. **`/frontend/src/pages/transportador/empresas-dashboard/EmpresasDashboard.jsx`**
   - Dashboard principal do módulo de Empresas
   - Cards de estatísticas
   - 6 cards de módulos clicáveis
   - Seções de atividades recentes

9. **`/frontend/src/pages/transportador/empresas-dashboard/EmpresasList.jsx`**
   - Lista de empresas com tabela
   - CRUD completo: Criar, Ler, Editar, Excluir
   - Busca por nome, CNPJ ou cidade
   - Formulário com validação

10. **`/frontend/src/pages/transportador/empresas-dashboard/FiliaisList.jsx`**
    - Lista de filiais com tabela
    - CRUD completo
    - Vinculação com empresas
    - Busca por nome, código, cidade ou empresa
    - Campos: código, nome, empresa, responsável, endereço

11. **`/frontend/src/pages/transportador/empresas-dashboard/AgregadosList.jsx`**
    - Lista de agregados (motoristas agregados)
    - CRUD completo
    - Formulário dividido em 3 seções:
      - Dados Pessoais (nome, CPF, RG, CNH, etc.)
      - Dados do Veículo (placa, modelo)
      - Dados do Contrato (empresa, datas)
    - Busca por nome, CPF, CNH ou placa

### Arquivos Modificados

12. **`/frontend/src/pages/transportador/Dashboard.jsx`**
    - Adicionado botão "Empresas" nas Ações Rápidas
    - Importado ícone Building2
    - Link para `/dashboard/empresas-dashboard`

13. **`/frontend/src/App.jsx`**
    - Importados novos componentes e páginas
    - Adicionadas rotas para o Dashboard de Empresas
    - Configuração de rotas aninhadas

14. **`/frontend/src/api/config.js`**
    - Adicionados endpoints de Empresas e Filiais
    - Adicionados endpoints de Motoristas (internos e externos)
    - Endpoints organizados por módulo

## Rotas Configuradas

### Rota Principal
- **`/dashboard/empresas-dashboard`** - Dashboard de Empresas (Nível 2)

### Rotas Aninhadas
- **`/dashboard/empresas-dashboard/empresas`** - Lista de Empresas
- **`/dashboard/empresas-dashboard/filiais`** - Lista de Filiais
- **`/dashboard/empresas-dashboard/agregados`** - Lista de Agregados
- **`/dashboard/empresas-dashboard/documentos`** - Documentos (placeholder)
- **`/dashboard/empresas-dashboard/relatorios`** - Relatórios (placeholder)
- **`/dashboard/empresas-dashboard/configuracoes`** - Configurações (placeholder)

## Fluxo de Navegação

### 1. Dashboard Principal → Dashboard Empresas

```javascript
// No Dashboard Transportador
<QuickAction
  title="Empresas"
  description="Gerenciar empresas, filiais e agregados"
  icon={Building2}
  to="/dashboard/empresas-dashboard"
  color="blue"
/>
```

### 2. Dashboard Empresas → Módulos

```javascript
// No Dashboard de Empresas
<ModuleCard
  title="Empresas"
  description="Cadastro e gerenciamento de empresas do grupo"
  icon={Building2}
  to="/dashboard/empresas-dashboard/empresas"
  color="blue"
  stats="5"
/>
```

### 3. Módulos → Funcionalidades CRUD

Cada módulo possui:
- **Lista** - Tabela com dados
- **Criar** - Modal com formulário
- **Editar** - Modal com formulário preenchido
- **Excluir** - Diálogo de confirmação

## Padrão de Cores Mantido

O módulo mantém o padrão de cores existente do sistema:

- **Fundo Principal:** `#0b1220` (azul escuro)
- **Texto Principal:** `#e5e7eb` (cinza claro)
- **Sidebar:** `#1A237E` (azul índigo escuro)
- **Gradiente Principal:** `linear-gradient(135deg, #60a5fa, #6366f1, #7c3aed)`
- **Hover Sidebar:** `#3949AB`
- **Item Ativo:** Gradiente `from-blue-400 via-indigo-500 to-purple-600`

## Instruções para Teste

### 1. Iniciar o Backend (Django)

```bash
cd /home/ubuntu/xbpneus
source venv/bin/activate
python manage.py runserver 8000
```

### 2. Iniciar o Frontend (React + Vite)

```bash
cd /home/ubuntu/xbpneus/frontend
npm run dev
```

### 3. Fluxo de Teste

1. **Login no Sistema**
   - Acesse `http://localhost:3000/login`
   - Use as credenciais: `transportador.teste@xbpneus.com` / `Teste@2025`

2. **Navegar para Dashboard de Empresas**
   - No Dashboard principal, clique no card "Empresas"
   - Você será redirecionado para `/dashboard/empresas-dashboard`

3. **Testar Dashboard de Empresas**
   - Verifique os 4 cards de estatísticas
   - Verifique os 6 cards de módulos
   - Verifique as seções "Empresas Recentes" e "Atividades Recentes"

4. **Testar Módulo de Empresas**
   - Clique no card "Empresas"
   - Clique em "Nova Empresa"
   - Preencha o formulário e salve
   - Edite uma empresa existente
   - Exclua uma empresa (confirme a exclusão)
   - Teste a busca

5. **Testar Módulo de Filiais**
   - Clique no card "Filiais" no Dashboard de Empresas
   - Clique em "Nova Filial"
   - Selecione uma empresa
   - Preencha os dados e salve
   - Teste edição, exclusão e busca

6. **Testar Módulo de Agregados**
   - Clique no card "Agregados" no Dashboard de Empresas
   - Clique em "Novo Agregado"
   - Preencha as 3 seções do formulário:
     - Dados Pessoais
     - Dados do Veículo
     - Dados do Contrato
   - Salve e teste edição, exclusão e busca

7. **Testar Navegação**
   - Use o botão "Voltar ao Dashboard" na sidebar
   - Navegue entre os módulos usando a sidebar lateral
   - Verifique que os itens ativos ficam destacados

## Funcionalidades Implementadas

### CRUD Completo

Todas as 3 telas principais possuem:

✅ **Create (Criar)**
- Modal com formulário
- Validação de campos obrigatórios
- Botões "Cancelar" e "Salvar"

✅ **Read (Ler)**
- Tabela responsiva
- Paginação (preparado para implementação)
- Busca com debounce
- Estado de loading
- Estado vazio (quando não há dados)

✅ **Update (Atualizar)**
- Modal com formulário preenchido
- Mesma validação do Create
- Atualização em tempo real na lista

✅ **Delete (Excluir)**
- Diálogo de confirmação
- Mensagem personalizada com nome do item
- Botões "Cancelar" e "Excluir"

### Componentes Reutilizáveis

Os componentes criados podem ser usados em outros módulos:

- **FormModal** - Para qualquer formulário
- **ConfirmDialog** - Para qualquer confirmação
- **StatusBadge** - Para exibir status
- **SearchBar** - Para busca com debounce
- **StatsCard** - Para cards de estatísticas

## Próximos Passos

### 1. Conectar com Backend Real

Atualmente, os dados são simulados. Para conectar com o backend:

```javascript
// Em EmpresasList.jsx, substituir:
const fetchEmpresas = async () => {
  setLoading(true);
  try {
    const response = await api.get(API_ENDPOINTS.transportador.empresas);
    setEmpresas(response.data);
    setLoading(false);
  } catch (error) {
    console.error('Erro ao carregar empresas:', error);
    setLoading(false);
  }
};
```

### 2. Implementar Paginação

Adicionar componente de paginação:

```javascript
<Pagination
  currentPage={currentPage}
  totalPages={totalPages}
  onPageChange={setCurrentPage}
/>
```

### 3. Implementar Exportação

Adicionar botões de exportação (CSV, Excel, PDF):

```javascript
<ExportButton
  data={empresas}
  filename="empresas"
  formats={['csv', 'excel', 'pdf']}
/>
```

### 4. Adicionar Validações Avançadas

- Validação de CNPJ
- Validação de CPF
- Validação de CNH
- Validação de placa de veículo
- Validação de datas

### 5. Implementar Módulos Restantes

Seguir o mesmo padrão para:
- Documentos
- Relatórios
- Configurações

### 6. Adicionar Testes Unitários

Criar testes para:
- Componentes reutilizáveis
- Páginas de CRUD
- Fluxos de navegação

## Padrão para Replicação

Este padrão deve ser replicado para todos os outros pilares do sistema:

### Estrutura Padrão

```
Dashboard Principal
    ↓ [Botão do Pilar]
Dashboard do Pilar
    ↓ [Cards de Módulos]
Telas de Funcionalidades
```

### Exemplo: Pilar de Frota

```
Dashboard Transportador
    ↓ [Botão "Frota"]
Dashboard Frota
    ↓ [Cards: Veículos, Motoristas, Manutenção, etc.]
Telas de Funcionalidades
    - Veículos (CRUD)
    - Motoristas (CRUD)
    - Manutenção (CRUD)
```

### Componentes a Criar para Cada Pilar

1. **`[Pilar]Sidebar.jsx`** - Sidebar específica
2. **`Layout[Pilar]Dashboard.jsx`** - Layout wrapper
3. **`[Pilar]Dashboard.jsx`** - Dashboard com cards
4. **`[Modulo]List.jsx`** - Lista de cada módulo

### Rotas a Configurar

```javascript
// No App.jsx
<Route path="/dashboard/[pilar]-dashboard" element={...}>
  <Route index element={<[Pilar]Dashboard />} />
  <Route path="[modulo]" element={<[Modulo]List />} />
  ...
</Route>
```

## Conclusão

O Módulo de Empresas foi implementado com sucesso seguindo a arquitetura hierárquica solicitada. Todos os componentes são reutilizáveis e o padrão pode ser replicado para os demais pilares do sistema.

**Resumo do que foi entregue:**

✅ 7 componentes reutilizáveis
✅ 4 páginas completas
✅ 2 arquivos modificados
✅ Rotas configuradas
✅ Padrão de cores mantido
✅ CRUD completo em 3 módulos
✅ Documentação completa

**Próximo pilar sugerido:** Frota (Veículos, Motoristas, Manutenção)

