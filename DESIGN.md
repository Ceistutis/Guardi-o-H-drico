---
name: Guardião Hídrico
description: Monitoramento demonstrativo de água com leitura clara.
colors:
  accent: "#007F83"
  ink: "#10283F"
  ground: "#F1F6FA"
  surface: "#FFFFFF"
  border: "#CFDDE7"
  muted: "#4B6074"
  tint: "#E0F5F3"
  focus: "#006970"
  success: "#076B50"
  success-bg: "#E2F4EB"
  warning: "#854A08"
  warning-bg: "#FFF3DB"
  danger: "#AC2430"
  danger-bg: "#FDECEF"
  sidebar-accent: "#32D4D0"
  sidebar-hover: "#1C3A53"
typography:
  body:
    fontFamily: "sans-serif"
    fontSize: "17px"
    lineHeight: 1.5
  headline:
    fontSize: "2.5rem"
    letterSpacing: "-.035em"
  title:
    fontSize: "1.35rem"
    letterSpacing: "-.02em"
  metric:
    fontSize: "clamp(1.65rem, 2.6vw, 2.4rem)"
    fontWeight: 700
    lineHeight: 1.15
  chart:
    fontFamily: "Arial"
    fontSize: "16px"
rounded:
  card: "14px"
  mode: "12px"
  navigation: "10px"
  status: "8px"
spacing:
  base: "1rem"
  card: "1.1rem"
components:
  valve-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.card}"
    padding: "{spacing.card}"
  mode:
    backgroundColor: "{colors.tint}"
    textColor: "{colors.ink}"
    rounded: "{rounded.mode}"
    padding: ".8rem 1rem"
  status-good:
    backgroundColor: "{colors.success-bg}"
    textColor: "{colors.success}"
    rounded: "{rounded.status}"
    padding: ".25rem .7rem"
  navigation-selected:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.surface}"
    rounded: "{rounded.navigation}"
    padding: ".65rem .75rem"
---

# Design System: Guardião Hídrico

## Overview

**Creative North Star: "Monitoramento de água com clareza"**

A direção aprovada combina lateral azul-marinho, fundo cinza azulado, cartões brancos e destaque turquesa. A leitura ampla e os controles explícitos atendem um público que inclui pessoas de meia-idade e idosas. A metáfora resume a direção existente, sem propor outra identidade.

Registro extraído de `.streamlit/config.toml`, `app/ui/theme.py`, `styles.css`, `components.py`, `charts.py`, `screens.py` e `app/main.py`, para Streamlit 1.50.0. O tema de execução é a origem dos valores; atualizar esta referência quando ele mudar. Este documento não constitui certificação de acessibilidade ou registro de testes realizados pelo documentador.

**Key Characteristics:**
- Leitura ampla, superfícies claras e lateral escura.
- Estados em texto, com cores de apoio.
- Simulação identificada e comandos separados da leitura.

## Colors

### Primary

O turquesa de monitoramento (`accent`) aparece nos gráficos, ícones e seleção da navegação. O turquesa luminoso (`sidebar-accent`) identifica marca e foco na lateral. O turquesa profundo (`focus`) identifica o foco externo e o texto de estado do modo demonstração.

### Neutral

Azul-marinho (`ink`) para texto, lateral e ação da válvula; névoa azulada (`ground`) para fundo; branco (`surface`) para cartões; borda fria (`border`) para divisores. Texto secundário usa `muted` sem redução de opacidade. `tint` oferece apoio tonal a ícones e modo; `sidebar-hover` responde ao ponteiro na navegação.

Verde, âmbar e vermelho semânticos acompanham mensagens de sucesso, atenção e erro. Etiquetas usam os pares sucesso/atenção. Alertas nativos mantêm seus fundos Streamlit e têm texto reforçado pelos tokens; informação usa `ink`. Não confundir a disponibilidade de `danger-bg` no tema com uma sobrescrita do fundo de alertas nativos.

## Typography

Fonte sem serifa nativa, sem download; Arial nos gráficos. A base do frontmatter governa corpo, legendas e tabela. Métricas e horários usam algarismos tabulares. Subtítulos usam a regra CSS `title`, que prevalece sobre h3 do TOML. O indicador de válvula é uma exceção de 1.7rem; rótulos de cartões têm peso 650 e botões, 600. Usar números pt-BR, unidades explícitas e horário de Brasília.

## Layout

Contêiner principal até 1530px, padding de 2rem 1.75rem 1.25rem; sidebar nativa entre 260 e 300px. Quatro métricas em colunas iguais, permitindo duas colunas entre 641 e 1100px. Até 640px, padding de 3.5rem 1rem 1.25rem, h1 de 2rem e métricas de 2.1rem. O empilhamento dos demais blocos depende do Streamlit; a lateral é recolhível.

Visão geral: gráfico/válvula em 2.15:1. Alertas: eventos/válvula em 1.8:1. Métricas têm altura mínima de 155px. Eventos quebram textos longos e posicionam o horário em outra linha na janela estreita.

## Elevation & Depth

Superfícies brancas, borda de 1px e sombra ambiente única (`--gh-shadow`, no sidecar). Fundo e lateral fornecem a separação principal. Sem animação decorativa ou transições customizadas.

## Shapes

Cartões suavemente arredondados, avisos e etiquetas progressivamente compactos: usar raios do frontmatter. Ícones geométricos locais acompanham rótulos. No app, SVGs são imagens autocontidas para compatibilidade com a sanitização de `st.html`.

## Components

- **Botões:** widgets nativos, altura mínima de 46px, peso 600. A válvula usa marinho, hover `#24475F` e estado desabilitado próprio (fundo `#E0E7ED`, borda `#C4D0D9`, texto `#526577`). Foco de 3px com afastamento de 3px. Explicar indisponibilidade quando relevante.
- **Campos:** data, seleção, checkbox e toggle nativos; preservar rótulos e teclado. Checkbox/toggle têm rótulos com altura mínima de 44px; expander, 52px. Não existe campo customizado com medidas próprias.
- **Navegação:** rádio nativo com rótulos, seleção turquesa, hover marinho elevado e foco luminoso. Itens com altura mínima de 52px.
- **Cartões:** superfície, borda, raio e sombra compartilhados; métricas com padding .85rem 1rem e demais cartões com `spacing.card`.
- **Modo demonstração:** fundo tonal, simulação e ausência de hardware explícitas. O texto de estado usa `focus` para contraste sobre `tint`.
- **Etiquetas e alertas:** verde para estado conhecido, âmbar para desconhecido; resposta de comando e leitura continuam distintos. Reconhecer alerta não resolve sua condição.
- **Gráficos:** Plotly transparente, altura 295px, grade horizontal discreta, linha turquesa de 2.5px, marcadores de 4px e preenchimento a 10%. Lacunas de comunicação quebram a linha. Histórico com barras e tabela semântica.
- **Eventos:** mensagem, categoria, severidade, estado e horário; divisores frios e quebra de texto. Vazio recebe explicação.

Estilos nativos são específicos ao Streamlit 1.50.0. Preferir chaves `st-key-*` e classes próprias; limitar `data-testid` às adaptações necessárias em `app/ui/styles.css`, evitando classes geradas. Revalidar seletores após atualizar Streamlit. Amostras do sidecar são representações autônomas, não substitutos dos widgets ou do calendário nativo.

## Do's and Don'ts

### Do:
- **Do** manter texto amplo, unidades e rótulos explícitos.
- **Do** preservar foco visível e alvos amplos.
- **Do** indicar simulação, ausência de leitura e desatualização em texto.
- **Do** atualizar esta referência quando o tema mudar.

### Don't:
- **Don't** usar somente cor para diferenciar estados.
- **Don't** tratar resposta de comando como leitura confirmada.
- **Don't** acrescentar decoração animada ou ocultar a simulação.
- **Don't** ampliar seletores internos do Streamlit sem necessidade.
