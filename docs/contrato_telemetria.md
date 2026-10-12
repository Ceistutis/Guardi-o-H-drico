# Contrato de telemetria v1 — proposta

**Proposta a revisar com a frente de firmware.** Implementada somente por um mock. Não define transporte, calibração ou garantias de atuação física.

## Exemplo de leitura

```json
{
  "schema_version": "1.0",
  "device_id": "bancada-principal",
  "session_id": "d5908728-bebe-4ba4-ad93-1fb9a6245045",
  "sequence": 1,
  "measured_at_utc": "2026-10-12T20:00:00+00:00",
  "received_at_utc": "2026-10-12T20:00:00+00:00",
  "flow_l_min": 4.0,
  "session_volume_l": 0.0,
  "water_detected": false,
  "valve_reported_state": "aberta",
  "quality": "good",
  "simulated": true
}
```

| Campo | Significado |
| --- | --- |
| schema_version | Versão do formato, 1.0 no mock |
| device_id | Identidade lógica do ponto de medição |
| session_id | Identidade da sessão; reinício gera outra |
| sequence | Contador crescente de leituras da sessão |
| measured_at_utc | Instante UTC da amostra |
| received_at_utc | Instante UTC de recepção, separado para futura latência |
| flow_l_min | Vazão não negativa em L/min, ou null |
| session_volume_l | Integral não negativa da vazão da sessão em litros, ou null |
| water_detected | Presença de água no sensor localizado; bool ou null, não umidade relativa |
| valve_reported_state | aberta, fechada ou desconhecido, informado pela leitura |
| quality | good, invalid ou unknown; só good confirma estado na UI |
| simulated | true no mock; identifica origem simulada |

Volume da sessão exclui pausa e intervalos sem comunicação, sem extrapolar lacunas. Não é consumo diário; o histórico diário ilustrativo é separado. O adaptador real deverá definir contador, reinícios e reconciliação com firmware.

Sem leitura retornar `None`; desconhecido é null, nunca zero fictício. UTC no contrato; interface converte para America/Sao_Paulo. Após 10 s desde a recepção, os valores são históricos/desatualizados e a válvula é desconhecida. Indisponibilidade explícita bloqueia comandos imediatamente. Qualidade não good impede confirmação.

Identidade: `(device_id, session_id, sequence)`. O mock publica na amostragem ou mudança efetiva de cenário, sem duplicar no rerender. Um adaptador real deverá rejeitar duplicatas, leituras fora de ordem, unidades inválidas e timestamps incoerentes antes de expor dados. A ingestão de pacotes reais não foi implementada.

## Comandos

`ValveCommand`: command_id único, device_id, desired_state (aberta/fechada), requested_at_utc e confirm_alerts (bool, default false, confirmação demonstrativa do operador).

`CommandResult`: command_id, status, message, completed_at_utc (null enquanto pendente).

- pending: aceito para envio, aguardando resposta.
- acknowledged: resposta recebida; não comprova estado físico. A UI aguarda leitura posterior.
- failed: pedido inválido, abertura bloqueada ou cancelada pela proteção. Rejeição imediata retorna ao chamador sem substituir comando em andamento.
- timeout: sem resposta em 8 s simulados; sem repetição automática.

Resposta em 3 s de simulação; leitura seguinte informa posição. Pausa congela ambos. Repetir o identificador do último comando retorna o resultado existente. Não há fila: pedido concorrente é rejeitado. Idempotência durável e reconciliação ficam para o adaptador real.

## Eventos e fonte

`Event`: event_id, timestamp_utc, severity (informação/atenção/crítico), category (consumo/vazamento/comunicacao/protecao/comando), message, state (ativo/reconhecido/resolvido).

Reconhecer não altera água detectada ou cenário. Sair do cenário resolve o alerta e mantém seu registro. Ações/resultados pontuais usam resolvido. Limites: 200 eventos e 151 leituras recentes por sessão, sem armazenamento externo.

`TelemetrySource`: get_latest, get_recent_history, send_valve_command, get_events, get_last_command, get_command_result, acknowledge_event e is_available. Getters não avançam tempo. O `DemoController` controla relógio, cenário, proteção e pausa exclusivamente na demonstração.

MQTT, persistência e coordenação de usuários podem exigir serviço intermediário. A atuação autônoma final pertence ao controlador/serviço apropriado, sem depender do ciclo de uma página aberta.
