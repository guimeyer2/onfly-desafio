# Entrega — Consolidador de reservas de hotel

## Defeitos corrigidos

| # | Defeito | Arquivo | Causa raiz | Commit |
|-|-|-|-|-|
| 1 | `NO_SHOW` entrava como faturável | `src/onfly_report/services/status_policy.py` | `is_billable` excluía só `CANCELLED` (`status != "CANCELLED"`) em vez de aceitar só `CONFIRMED`. | `ee3c977` |
| 2 | Noites negativas na virada de mês/ano | `src/onfly_report/services/stay_calculator.py` | Subtraía o dia do mês (`checkout.day - checkin.day`) em vez da diferença entre as datas (`(checkout - checkin).days`). | `80b6c92` |
| 3 | Câmbio invertido e em `float` | `src/onfly_report/services/currency_converter.py` | Dividia o valor pela taxa e convertia para `float`, quando a regra é `amount * rate_to_brl` em `Decimal`. | `68d1454` |
| 4 | `top_hotels` em ordem crescente | `src/onfly_report/services/report_builder.py` | A chave de ordenação `(amount, hotel_id)` era crescente, e o certo é `(-amount, hotel_id)`: total decrescente com desempate por `hotel_id` crescente. | `644d91d` |
| 5 | Só as 200 primeiras reservas eram lidas | `src/onfly_report/repositories/csv_reservation_repository.py` | Um `break` ao chegar em 200 linhas truncava o arquivo sem aviso, e o dataset real tem 300. | `30aa1a4` |
| 6 | Moeda sem taxa saía com código 1 | `src/onfly_report/services/currency_converter.py` | A busca `rates[currency]` gerava `KeyError` (erro inesperado) em vez de `InputFileError`, que corresponde ao código 2 do contrato (entrada inválida). | `65e55f0` |

Com os defeitos 1 a 4 corrigidos, os 5 testes fornecidos passam e a amostra de validação bate com o README. O defeito 5 só aparece no dataset real. O defeito 6 é uma questão de aderência ao contrato de códigos de saída.

## Como investiguei

### Feito manualmente, antes de usar IA

1. Criei o repositório e fiz o commit do estado original (`2e052c1`).
2. Rodei `pytest -q`, e os 5 testes falharam.
3. Rodei o CLI na amostra (`data/exemplo-validacao.csv`) e comparei a saída com a tabela esperada do README. Os sintomas principais foram:
   - `total_room_nights = -33`, quando o esperado era 28;
   - `average_nightly_rate_brl = 0.00`, quando o esperado era 270.21;
   - `by_month` de 2025-01 com 9 reservas, quando o esperado era 8;
   - `top_hotels` em ordem crescente.
4. Li o código e levantei três suspeitas: o `status_policy` só exclui `CANCELLED`, o `stay_calculator` usa `.day` e a ordenação do `report_builder` está invertida.

### Feito junto com a IA (Claude Code)

1. **Revisão completa sem alterar código.** Pedi uma varredura de todo o código, regra por regra do README. A IA confirmou as três suspeitas e encontrou dois defeitos novos: o câmbio, que dividia em vez de multiplicar e usava `float`, e o limite de 200 linhas. Também explicou que o `0.00` da média era consequência das noites negativas, porque o código cai no ramo "sem noites". Levantou ainda o caso da moeda sem taxa; decidi tratá-lo como código 2 e manter a normalização de status/moeda como estava, já que os dados são consistentes.
2. **Ordem de correção.** Aprovei a ordem: dos defeitos de maior impacto para os mais isolados. O câmbio veio depois das noites, para que a média deixasse de ser mascarada.
3. **Ciclo por defeito:** escrever um teste novo que reproduz o erro, mostrar o teste falhando, aplicar a correção mínima, rodar o `pytest -q` completo e fazer um commit. Os testes fornecidos e os CSVs não foram alterados.

| Defeito | Teste novo | Falha antes da correção | Suíte depois |
|-|-|-|-|
| 1 | `tests/test_no_show_excluded.py` | 2 noites em vez de 1 | 2 passando, 4 falhando |
| 2 | `tests/test_nights_extra.py` | −29 e −52 noites | 5 passando, 3 falhando |
| 3 | `tests/test_currency_extra.py` | `25.51` em vez de `882.00`; `0.06` em vez de `1.63` | 9 passando, 1 falhando |
| 4 | `tests/test_top_hotels_tiebreak.py` | `H04,H01,H03` em vez de `H02,H01,H03` | 11 passando |
| 5 | `tests/test_large_input.py` | 200 reservas em vez de 250 | 12 passando |
| 6 | `tests/test_missing_rate.py` | código 1 com traceback | 13 passando |

## Como validar

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

pytest -q

PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json

PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json
```

Saídas esperadas no stdout:

```
Reservas: 12 | Confirmadas: 9 | Noites: 28 | Total BRL: 7566.00
Reservas: 300 | Confirmadas: 235 | Noites: 1347 | Total BRL: 396170.00
```

O `output/exemplo.json` bate com as três tabelas da amostra do README: o resumo, o `by_month` (2025-01 com 8 reservas, 25 noites e 6684.00; 2025-02 com 1 reserva, 3 noites e 882.00) e o `top_hotels` (H01, H02, H12, H10, H09).

## Resultado do pytest

```
$ pytest -q
.............                                                            [100%]
13 passed
```

São 5 testes fornecidos, sem alteração, e 8 testes adicionais. O `ruff check src tests` não aponta nenhum problema.
