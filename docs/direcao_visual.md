# Reformulação do dashboard — 02/11/2026

Superfície: `app/main.py`, `app/ui/`. Modo **Operate**: interpretar leituras e executar controles com clareza.

## Direction contract

**THESIS:** aproximar o dashboard da composição aprovada, preservando os dados e o comportamento do MVP.

**OWN-WORLD:** lateral azul-marinho, fundo cinza azulado, cartões brancos com borda discreta e sombra suave; turquesa para destaque. Fonte simples local de 17 px, sem decoração animada.

**STORY:** identificar modo simulado e última leitura, consultar vazão/volume/válvula/alertas, atuar na válvula e entender os eventos. Pausa, falta de comunicação e estados pendentes permanecem distintos.

**FIRST VIEWPORT:** navegação à esquerda; título e modo demonstração no topo; quatro indicadores; gráfico com janela real de cinco minutos e painel da válvula lado a lado; eventos recentes e configurações abaixo. Em janela estreita, sidebar recolhível e blocos empilhados.

**FORM:** referência escolhida explicitamente pelo usuário; adaptação aos componentes nativos do Streamlit, sem votação de estilos ou períodos fictícios. SVGs geométricos para ícones, sem novas imagens decorativas. Ações importantes permanecem botões nativos.

**FINISH:** revisão funcional, capturas desktop/estreita, contraste e foco verificados; documentação do sistema efetivamente implementado. Sem push, merge ou deploy nesta entrega.
