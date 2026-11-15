# Declaração de uso de IA

- **Ferramenta:** Claude Code (app desktop)
- **Modelo:** Claude Opus 5.5

## O que eu fiz

- Criei o repositório e fiz o commit do estado original.
- Rodei o `pytest` e o CLI na amostra, comparei a saída com a tabela do README e identifiquei os sintomas.
- Li o código e levantei as três primeiras suspeitas: o status `NO_SHOW`, o cálculo de noites por `.day` e a ordenação do `top_hotels`.
- Defini o processo: primeiro uma revisão sem alterar código; depois, para cada defeito, um teste que reproduz o erro, a correção mínima, o pytest completo e um commit.
- Decidi o escopo: moeda sem taxa sai com código 2, e a normalização de status/moeda ficou como estava.
- Aprovei a ordem das correções, revisei os resultados e rodei a suíte de forma independente.

## O que a IA fez

- Revisou o código inteiro contra as regras do README, confirmou minhas suspeitas e encontrou os defeitos de câmbio (divisão e uso de `float`) e de limite de 200 linhas.
- Propôs a ordem das correções.
- Escreveu os 8 testes adicionais, aplicou as correções mínimas, rodou o pytest e o ruff e fez um commit por defeito.
- Validou a amostra e o dataset real.
- Redigiu este documento e o `README-ENTREGA.md`, a partir das minhas instruções.
