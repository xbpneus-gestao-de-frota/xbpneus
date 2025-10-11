# Padrão de Cores - Sistema XBPneus

## Análise das Telas de Login e Cadastro

### Paleta de Cores Principal

**Logo e Título:**
- Azul principal: `#5B7FE8` (azul médio vibrante)
- Roxo degradê: `#7B5FE8` até `#9B5FE8`
- Sombra: azul escuro com opacidade

**Campos de Entrada (Inputs):**
- Borda verde: `#4CAF50` ou similar (campo Nome/Razão Social)
- Borda azul: `#5B7FE8` (campo CNPJ)
- Borda laranja/amarela: `#FFA726` ou `#FFB74D` (campo Telefone)
- Borda roxa/lilás: `#9C27B0` ou `#AB47BC` (campo E-mail)
- Borda ciano/turquesa: `#00BCD4` ou `#26C6DA` (campo Senha)
- Borda rosa: `#E91E63` ou `#EC407A` (campo Confirmar Senha)
- Borda roxa escura: `#673AB7` (campo Tipo de Usuário)

**Botões:**
- Botão principal (Entrar/Registrar): Degradê azul-roxo
  - Início: `#5B7FE8`
  - Fim: `#9B5FE8`
- Hover: Degradê mais intenso
- Texto: Branco `#FFFFFF`

**Links:**
- Cor: Ciano/turquesa `#00BCD4`
- Hover: Ciano mais escuro

**Fundo:**
- Cor principal: `#F5F5F5` ou `#FAFAFA` (cinza muito claro)
- Card de login/cadastro: Branco `#FFFFFF` com sombra suave

**Mascotes:**
- Uniforme: Azul marinho escuro `#1A237E` ou similar
- Detalhes: Branco

### Cores para Aplicar no Restante do Sistema

#### Sidebar/Menu Lateral
- Fundo: `#1A237E` (azul marinho escuro)
- Texto: `#FFFFFF`
- Item ativo: Degradê `#5B7FE8` → `#9B5FE8`
- Hover: `#3949AB` (azul médio)

#### Header/Cabeçalho
- Fundo: Branco `#FFFFFF` com sombra
- Texto: `#1A237E`
- Ícones: `#5B7FE8`

#### Botões Primários
- Fundo: Degradê `#5B7FE8` → `#9B5FE8`
- Texto: `#FFFFFF`
- Hover: Degradê mais intenso
- Sombra: `rgba(91, 127, 232, 0.3)`

#### Botões Secundários
- Fundo: Transparente
- Borda: `#5B7FE8` 2px
- Texto: `#5B7FE8`
- Hover: Fundo `rgba(91, 127, 232, 0.1)`

#### Cards/Painéis
- Fundo: Branco `#FFFFFF`
- Borda: `#E0E0E0` ou sem borda
- Sombra: `0 2px 8px rgba(0, 0, 0, 0.1)`
- Título: `#1A237E`

#### Tabelas
- Header: Degradê `#5B7FE8` → `#9B5FE8`
- Texto header: `#FFFFFF`
- Linhas alternadas: `#F5F5F5`
- Hover linha: `rgba(91, 127, 232, 0.1)`
- Borda: `#E0E0E0`

#### Status/Badges
- Sucesso: `#4CAF50` (verde)
- Aviso: `#FFA726` (laranja)
- Erro: `#E91E63` (rosa/vermelho)
- Info: `#00BCD4` (ciano)
- Neutro: `#9E9E9E` (cinza)

#### Inputs/Forms
- Borda normal: `#E0E0E0`
- Borda focus: `#5B7FE8`
- Label: `#666666`
- Texto: `#1A237E` (azul escuro após digitação)
- Placeholder: `#BDBDBD`
- Background: `#FFFFFF`

#### Gráficos/Dashboard
- Cor 1: `#5B7FE8` (azul principal)
- Cor 2: `#9B5FE8` (roxo)
- Cor 3: `#00BCD4` (ciano)
- Cor 4: `#4CAF50` (verde)
- Cor 5: `#FFA726` (laranja)
- Cor 6: `#E91E63` (rosa)

### Tipografia

**Fontes:**
- Principal: Sans-serif moderna (provavelmente Roboto, Inter ou similar)
- Peso: 400 (normal), 500 (medium), 700 (bold)

**Tamanhos:**
- Logo: 48-64px
- Título página: 24-32px
- Subtítulo: 18-20px
- Texto normal: 14-16px
- Texto pequeno: 12-14px

### Espaçamento e Layout

**Padding/Margin:**
- Pequeno: 8px
- Médio: 16px
- Grande: 24px
- Extra grande: 32px

**Border Radius:**
- Inputs: 8px
- Botões: 8px
- Cards: 12px
- Modais: 16px

**Sombras:**
- Leve: `0 2px 4px rgba(0, 0, 0, 0.1)`
- Média: `0 4px 8px rgba(0, 0, 0, 0.15)`
- Forte: `0 8px 16px rgba(0, 0, 0, 0.2)`

### Responsividade

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Acessibilidade

- Contraste mínimo: 4.5:1 para texto normal
- Contraste mínimo: 3:1 para texto grande
- Focus visível em todos os elementos interativos
- Estados hover/active claramente diferenciados

---

## Implementação

Para aplicar este padrão em todo o sistema:

1. Criar arquivo CSS/SCSS com variáveis de cores
2. Atualizar componentes React para usar as variáveis
3. Garantir consistência em todas as páginas
4. Testar responsividade
5. Validar acessibilidade

