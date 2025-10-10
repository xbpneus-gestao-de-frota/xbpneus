# 🎨 Preservação das Páginas de Autenticação - Sistema XBPneus

## ⚠️ IMPORTANTE - NÃO MODIFICAR

As páginas de **Login**, **Cadastro** e **Pós-Cadastro** devem manter **EXATAMENTE** suas cores, dimensões e formatos originais.

---

## 📋 Páginas Protegidas

### 1. Login (`/frontend/src/pages/Login.jsx`)

**Elementos que NÃO devem ser alterados:**

#### Cores
- ✅ Fundo: `bg-gray-100`
- ✅ Card de login: Branco com sombra
- ✅ Botão de login: Gradiente azul (mantido)
- ✅ Texto dos inputs: **Azul escuro após digitação**
- ✅ Links: Azul padrão

#### Dimensões
- ✅ Mascotes laterais: Tamanho atual preservado
- ✅ Logo XBPneus: Dimensões atuais
- ✅ Card central: Largura e altura atuais
- ✅ Inputs: Altura e padding atuais

#### Posições
- ✅ Mascote esquerda: `left-2 xl:left-4 top-1/4`
- ✅ Mascote direita: `right-2 xl:right-4 top-1/4`
- ✅ Logo: Centralizado no topo
- ✅ Card: Centralizado vertical e horizontalmente

#### Assets
- ✅ `/static/manutenção.png` - Mascote esquerda
- ✅ `/static/frota.png` - Mascote direita
- ✅ Logo XBPneus (atual)

---

### 2. Cadastro (`/frontend/src/pages/Cadastro.jsx`)

**Elementos que NÃO devem ser alterados:**

#### Cores
- ✅ Fundo: `bg-gray-100`
- ✅ Card de cadastro: Branco com sombra
- ✅ Botão de cadastro: Gradiente azul
- ✅ **Campo 'tipo de cliente': VISÍVEL (não transparente)**
- ✅ **Campos de senha: VISÍVEIS (não transparentes)**
- ✅ Texto dos inputs: **Azul escuro após digitação**

#### Dimensões
- ✅ Mascotes: **Mesmo padrão de tamanho da página de login**
- ✅ Logo: Mesma aparência da página de login
- ✅ Card: Largura e altura atuais
- ✅ Inputs: Altura e padding atuais

#### Visibilidade
- ⚠️ **CRÍTICO:** Campo "Tipo de Cliente" deve estar VISÍVEL
- ⚠️ **CRÍTICO:** Campos de senha devem estar VISÍVEIS (não transparentes)

#### Assets
- ✅ Mascotes (tamanho igual ao login)
- ✅ Logo XBPneus (igual ao login)

---

### 3. Pós-Cadastro (`/frontend/src/pages/PosCadastro.jsx`)

**Elementos que NÃO devem ser alterados:**

#### Cores
- ✅ **Fundo: ESTÁTICO** (não animado)
- ✅ Card: Branco com sombra
- ✅ Texto: Cores atuais
- ✅ Botão: Gradiente azul

#### Dimensões
- ✅ Imagem de sucesso: Tamanho atual
- ✅ Card: Largura e altura atuais
- ✅ Textos: Tamanhos atuais

#### Comportamento
- ✅ Fundo estático (sem animações)
- ✅ Redirecionamento após cadastro funcional

#### Assets
- ✅ `/static/pos_cadastro.png` - Imagem de sucesso
- ✅ `/static/images/pos-cadastro.png` - Backup
- ✅ `/static/images/pos-cadastro-bg.png` - Fundo estático

---

## 🎨 Tema Visual do Sistema

### Paleta de Cores Principal

```css
/* Cores primárias */
--primary-blue: #1e40af;        /* Azul principal */
--primary-blue-light: #3b82f6;  /* Azul claro */
--primary-blue-dark: #1e3a8a;   /* Azul escuro */

/* Gradientes */
--gradient-blue: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--gradient-button: linear-gradient(to right, #3b82f6, #1e40af);

/* Backgrounds */
--bg-light: #f3f4f6;            /* Cinza claro */
--bg-white: #ffffff;            /* Branco */
--bg-card: rgba(255, 255, 255, 0.95);  /* Card com transparência */

/* Textos */
--text-primary: #1f2937;        /* Texto principal */
--text-secondary: #6b7280;      /* Texto secundário */
--text-input: #1e3a8a;          /* Texto em inputs (azul escuro) */
```

### Estilo dos Inputs

```css
/* Input padrão */
.input-auth {
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: all 0.3s;
}

/* Input com foco */
.input-auth:focus {
  border-color: #3b82f6;
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Texto digitado (AZUL ESCURO) */
.input-auth {
  color: #1e3a8a !important;
}
```

### Botões de Ação

```css
.btn-primary {
  background: linear-gradient(to right, #3b82f6, #1e40af);
  color: white;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
}
```

---

## 📐 Dimensões e Espaçamentos

### Mascotes

```css
.mascote-lateral {
  max-width: 28rem;        /* 448px */
  height: auto;
  object-fit: contain;
  position: absolute;
  z-index: 1;
}

/* Posicionamento */
.mascote-esquerda {
  left: 0.5rem;           /* 8px */
  top: 25%;
}

.mascote-direita {
  right: 0.5rem;          /* 8px */
  top: 25%;
}

/* Responsivo */
@media (min-width: 1280px) {
  .mascote-esquerda {
    left: 1rem;           /* 16px */
  }
  .mascote-direita {
    right: 1rem;          /* 16px */
  }
}
```

### Logo XBPneus

```css
.logo-xbpneus {
  width: 200px;
  height: auto;
  margin-bottom: 2rem;
}
```

### Cards de Autenticação

```css
.auth-card {
  width: 100%;
  max-width: 28rem;       /* 448px */
  background: white;
  border-radius: 1rem;    /* 16px */
  padding: 2rem;          /* 32px */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  z-index: 10;
}
```

---

## 🔒 Regras de Preservação

### ✅ PERMITIDO

1. Corrigir bugs funcionais
2. Melhorar acessibilidade (sem alterar visual)
3. Adicionar validações de formulário
4. Otimizar performance
5. Corrigir responsividade (mantendo proporções)

### ❌ NÃO PERMITIDO

1. Alterar cores dos elementos
2. Modificar dimensões dos mascotes
3. Mudar posicionamento de elementos
4. Alterar gradientes e sombras
5. Modificar tamanho de fontes
6. Mudar espaçamentos principais
7. Alterar animações existentes
8. Modificar assets (imagens, logos)

---

## 📁 Arquivos Protegidos

### Páginas
```
✅ /frontend/src/pages/Login.jsx
✅ /frontend/src/pages/Cadastro.jsx
✅ /frontend/src/pages/CadastroTipoCliente.jsx
✅ /frontend/src/pages/PosCadastro.jsx
```

### Assets
```
✅ /frontend/public/static/manutenção.png
✅ /frontend/public/static/frota.png
✅ /frontend/public/static/configurações.png
✅ /frontend/public/static/pos_cadastro.png
✅ /frontend/public/static/images/pos-cadastro.png
✅ /frontend/public/static/images/pos-cadastro-bg.png
✅ /frontend/public/static/images/pos_login.png
```

### Estilos
```
✅ Classes CSS relacionadas a autenticação
✅ Variáveis de cores em index.css
✅ Gradientes definidos
```

---

## 🧪 Checklist de Verificação

Antes de fazer deploy, verificar:

- [ ] Página de Login mantém cores originais
- [ ] Página de Cadastro mantém cores originais
- [ ] Página Pós-Cadastro mantém cores originais
- [ ] Mascotes têm o mesmo tamanho em Login e Cadastro
- [ ] Logo XBPneus igual em Login e Cadastro
- [ ] Campo "Tipo de Cliente" está VISÍVEL
- [ ] Campos de senha estão VISÍVEIS (não transparentes)
- [ ] Texto dos inputs fica azul escuro após digitação
- [ ] Fundo do Pós-Cadastro é ESTÁTICO
- [ ] Todos os assets estão presentes
- [ ] Responsividade funciona sem quebrar layout
- [ ] Gradientes dos botões preservados
- [ ] Sombras dos cards preservadas

---

## 🚨 Em Caso de Problemas

Se alguma alteração acidental for feita:

1. **Reverter commit:**
   ```bash
   git revert <commit-hash>
   ```

2. **Restaurar arquivo específico:**
   ```bash
   git checkout <commit-hash> -- <arquivo>
   ```

3. **Verificar diferenças:**
   ```bash
   git diff <commit-hash> -- frontend/src/pages/Login.jsx
   ```

---

## 📞 Contato

Para dúvidas sobre preservação das páginas de autenticação:
- Consultar este documento
- Verificar screenshots originais
- Não alterar sem aprovação explícita

---

**IMPORTANTE:** Este documento é parte essencial do processo de deploy. Qualquer modificação nas páginas de autenticação deve ser documentada e aprovada antes de ser implementada.

---

**Última atualização:** 10 de Outubro de 2025  
**Versão:** 1.0

