# Prova de Conceito: Resiliência Offline e Sincronização Assíncrona

## O que este spike prova

Este código valida o **ADR 0005: sincronização assíncrona nas UBSs**.

O cenário simula uma UBS que:

1. registra um atendimento localmente;
2. continua registrando atendimentos quando a internet está indisponível;
3. mantém os eventos pendentes em uma fila local;
4. tenta sincronizar os eventos quando a conexão volta;
5. enfrenta um **timeout**, em que o servidor recebe o evento, mas a UBS não recebe a confirmação;
6. reenvia o mesmo evento sem criar um segundo registro no servidor.

O ponto principal do spike é demonstrar a combinação de **persistência local + worker de sincronização + reentrega + processamento idempotente**.

## ADR validado

**ADR 0005 — Sincronização assíncrona nas UBSs**

A decisão atende ao caso porque as UBSs podem ter internet instável e precisam continuar o atendimento durante a indisponibilidade da conexão.

## Relação com a arquitetura

O spike representa, de forma simplificada:

- **Aplicação local/PWA:** registra o atendimento sem depender da conexão;
- **Fila local:** mantém eventos ainda não sincronizados;
- **Worker:** tenta enviar eventos pendentes;
- **Rede:** simula estados online, offline e timeout;
- **Servidor central:** simula o armazenamento central e a regra de idempotência.

Para manter o spike pequeno e executável sem infraestrutura externa, banco e rede são simulados localmente. O armazenamento utiliza `sqlite3` em memória, disponível na biblioteca padrão do Python 3.12.

## Como executar

Requisito: **Python 3.12**.

Na pasta `3-spike`, execute:

```bash
python3 exemplo.py
```

Não é necessário instalar bibliotecas externas.

## Resultado esperado

A execução determinística está registrada em:

```text
saida-esperada.txt
```

Os IDs dos eventos são fixos (`evt-001`, `evt-002` e `evt-003`) para que a saída seja reproduzível e possa ser conferida.

Ao final, o servidor possui **3 registros** e a fila local possui **0 eventos pendentes**.

## Referência

O mecanismo de reentrega e consumidor idempotente foi adaptado ao caso da Rede Municipal de Saúde a partir do conceito apresentado no livro:

**Abreu, Douglas Henrique Siqueira. _Estilos Arquiteturais de Software: guia de consulta_. 2026.**

O spike foi adaptado ao **Caso Saúde + Envelope A**, em vez de reproduzir um exemplo genérico do livro.
