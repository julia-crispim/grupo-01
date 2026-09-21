# ADR 0003: integrar sistema legado via portas e adaptadores

**Status:** aceito

**Contexto:** Existe um sistema legado de regulação de leitos que não pode ser desligado nos primeiros 2 anos, além de integrações com APIs federais propensas a janelas de indisponibilidade.

**Decisão:** Utilizar o Padrão Hexagonal (Portas e Adaptadores) combinado com o padrão Anti-Corruption Layer (ACL) no módulo de regulação. As regras do nosso sistema conversam com uma "porta" limpa, enquanto o "adaptador" traduz as chamadas para o protocolo específico do legado, isolando falhas e instabilidades.

**Alternativas consideradas:**
- Integração direta no código de negócio: descartada, pois qualquer mudança ou queda do legado corromperia o domínio da aplicação.
- Barramento ESB (Cap. 10): descartado por ser pesado, caro e incompatível com a agilidade exigida da startup.

**Consequências:**
- **Positivas:** o domínio da aplicação permanece limpo e testável sem depender do legado; se o legado cair, a camada de adaptação gerencia o erro sem travar a UPA.
- **Negativas:** aumento inicial de código boilerplate (interfaces e mappers de tradução).
