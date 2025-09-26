# Política de Segurança

## Versões Suportadas

Atualmente, as seguintes versões do aplicativo de contatos pessoais estão sendo mantidas com atualizações de segurança:

| Versão | Suportada          |
| ------ | ------------------ |
| 1.x.x  | :white_check_mark: |
| < 1.0  | :x:                |

## Reportando uma Vulnerabilidade

Agradecemos seu interesse em ajudar a manter este projeto seguro. Se você descobrir uma vulnerabilidade de segurança, por favor, siga estas diretrizes:

### Como Reportar

1. **NÃO** crie uma issue pública no GitHub para vulnerabilidades de segurança.
2. Envie um e-mail para [seu-email@exemplo.com] com detalhes sobre a vulnerabilidade.
3. Inclua os seguintes detalhes em seu relatório:
   - Descrição clara da vulnerabilidade
   - Passos para reproduzir o problema
   - Versão do aplicativo afetada
   - Possível impacto da vulnerabilidade
   - Sugestões para mitigação ou correção (se possível)

### O que esperar

Após o envio de um relatório de vulnerabilidade:

1. Confirmaremos o recebimento do seu relatório dentro de 48 horas.
2. Nossa equipe avaliará a vulnerabilidade e determinará sua gravidade.
3. Manteremos você informado sobre o progresso da correção.
4. Quando a vulnerabilidade for corrigida, você será creditado pela descoberta (a menos que prefira permanecer anônimo).

## Práticas de Segurança

Este aplicativo implementa as seguintes práticas de segurança:

- Armazenamento seguro de senhas com hashing e salting
- Proteção contra injeção SQL usando ORM e consultas parametrizadas
- Validação de entrada para prevenir XSS e outros ataques
- Uso de HTTPS para todas as comunicações
- Implementação de autenticação JWT com expiração de tokens
- Sanitização de dados de entrada e saída

## Atualizações de Segurança

As atualizações de segurança são publicadas nos releases do projeto e documentadas no CHANGELOG. Recomendamos que você mantenha sua instalação sempre atualizada com a versão mais recente.

---

Agradeço sua contribuição para manter este projeto seguro!
