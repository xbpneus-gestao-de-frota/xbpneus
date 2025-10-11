# Análise do Erro 400 - Login
**Data:** 11 de outubro de 2025
**Hora:** 11:42:26 AM

## Problema Identificado

Ao tentar fazer login com o usuário `transportador.teste2@xbpneus.com`, o sistema retornou **erro 400** (Bad Request).

### Log do Erro

```
Oct 11 11:42:26 AM [POST] 400 xbpneus-backend.onrender.com/api/token/?t=1760182946104
clientIP="34.201.241.51" 
requestID="afe40438-00af-4cd3" 
responseTimeMS=595 
responseBytes=652 
userAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
```

## Hipóteses

### 1. Problema na Nova Validação de Aprovação
A correção que implementamos adiciona validação do campo `aprovado` no serializer. Possíveis causas:

- **Campo `aprovado` não existe no modelo base:** O modelo `UsuarioTransportador` herda de `AbstractUser`, mas a validação está verificando `self.user.aprovado` que pode não existir no usuário base.

- **Erro de atributo:** O campo `aprovado` pode estar definido apenas no modelo `UsuarioTransportador`, mas o serializer está acessando através de `self.user` (que é o modelo base do Django).

### 2. Estrutura do Código Implementado

```python
def validate(self, attrs):
    # Primeiro, valida as credenciais normalmente
    data = super().validate(attrs)
    
    # Verifica se o usuário está aprovado (exceto superusuários)
    if not self.user.is_superuser and not self.user.aprovado:
        raise serializers.ValidationError(
            "Usuário aguardando aprovação do administrador. "
            "Por favor, aguarde a aprovação para acessar o sistema."
        )
    
    return data
```

**Problema:** `self.user` é uma instância de `User` (modelo base do Django), não de `UsuarioTransportador`. O campo `aprovado` está em `UsuarioTransportador`, não em `User`.

## Solução Necessária

Precisamos acessar o campo `aprovado` corretamente através do relacionamento OneToOne entre `User` e `UsuarioTransportador`.

### Opção 1: Usar hasattr para verificar se o campo existe

```python
def validate(self, attrs):
    data = super().validate(attrs)
    
    # Verifica se o usuário tem o campo aprovado (usuários específicos)
    if not self.user.is_superuser:
        if hasattr(self.user, 'aprovado') and not self.user.aprovado:
            raise serializers.ValidationError(
                "Usuário aguardando aprovação do administrador."
            )
    
    return data
```

### Opção 2: Acessar através do relacionamento reverso

```python
def validate(self, attrs):
    data = super().validate(attrs)
    
    if not self.user.is_superuser:
        # Tenta acessar o perfil de transportador
        try:
            if hasattr(self.user, 'usuariotransportador'):
                if not self.user.usuariotransportador.aprovado:
                    raise serializers.ValidationError(
                        "Usuário aguardando aprovação do administrador."
                    )
        except AttributeError:
            pass  # Usuário não é transportador
    
    return data
```

### Opção 3: Verificar tipo de usuário primeiro

```python
def validate(self, attrs):
    data = super().validate(attrs)
    
    if not self.user.is_superuser:
        # Verifica cada tipo de usuário
        user_types = [
            'usuariotransportador',
            'usuariomotorista', 
            'usuarioborracharia',
            'usuariorevenda',
            'usuariorecapagem'
        ]
        
        for user_type in user_types:
            if hasattr(self.user, user_type):
                user_profile = getattr(self.user, user_type)
                if hasattr(user_profile, 'aprovado') and not user_profile.aprovado:
                    raise serializers.ValidationError(
                        "Usuário aguardando aprovação do administrador."
                    )
                break
    
    return data
```

## Próxima Ação

Implementar a **Opção 3** (mais robusta) para corrigir o erro 400 e permitir o login correto.

