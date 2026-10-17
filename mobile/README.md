# Guardião Hídrico Inteligente — Mobile

Aplicativo mobile do projeto **Guardião Hídrico Inteligente**, desenvolvido para monitorar o consumo de água, apresentar informações sobre o dispositivo e facilitar a visualização de possíveis vazamentos.

O aplicativo está sendo desenvolvido com React Native e Expo, utilizando TypeScript e navegação com Expo Router.

> **Status do projeto:** versão inicial da interface, com dados simulados. A integração com a API e o hardware ESP32 ainda será implementada.

## 📱 Funcionalidades implementadas

### Monitoramento — Início
- Exibição do estado de conexão do dispositivo.
- Indicador de status geral do sistema.
- Visualização da vazão atual em litros por minuto (L/min).
- Exibição do volume de água da sessão em litros (L).
- Apresentação do estado reportado da válvula.

### Alertas
- Tela para apresentação de eventos e alertas.
- Exibição de mensagens sobre o estado do sistema.
- Estrutura inicial para futura integração com os eventos da API.

### Histórico
- Exibição de leituras anteriores de vazão e volume.
- Apresentação dos registros em uma lista organizada por horário.
- Estrutura preparada para receber dados históricos do backend.

### Dispositivo
- Exibição do identificador do dispositivo.
- Apresentação do microcontrolador ESP32 e do sensor de vazão planejado.
- Visualização do estado reportado da válvula e informações de comunicação.

## 🛠️ Tecnologias e ferramentas

| Tecnologia ou ferramenta | Utilização |
|---|---|
| React Native | Desenvolvimento da interface mobile. |
| Expo SDK 58 | Ambiente e ferramentas para desenvolvimento do aplicativo. |
| TypeScript | Tipagem estática e organização do código. |
| Expo Router | Navegação entre as telas baseada em arquivos. |
| NativeTabs | Navegação por abas nativas. |
| React Native StyleSheet | Estilização dos componentes. |
| Node.js e npm | Ambiente de execução das ferramentas e gerenciamento de dependências. |
| Git e GitHub | Versionamento e colaboração no projeto. |
| Visual Studio Code | Editor de código recomendado. |

## 📋 Pré-requisitos

Antes de executar o projeto, instale:

- **Node.js:** versão compatível com o Expo SDK utilizado.
- **npm:** instalado junto com o Node.js.
- **Git:** para clonar o repositório.
- **Expo Go:** opcional, para testar em um celular compatível.
- **Android Studio:** opcional, para executar em um emulador Android.

Para conferir as versões instaladas:

```bash
node -v
npm -v
git --version
```

Consulte a documentação do Expo para verificar a compatibilidade das versões de Node.js e dos ambientes de desenvolvimento:

- [Documentação do Expo](https://docs.expo.dev/)
- [Expo Router](https://docs.expo.dev/router/introduction/)

## 🚀 Como executar em outra máquina

### 1. Instale os pré-requisitos

Instale o Git e o Node.js. Se for utilizar um celular físico, instale também o Expo Go.

### 2. Clone o repositório

No terminal, execute:

```bash
git clone https://github.com/Ceistutis/Guardi-o-H-drico.git
```

Entre na pasta do projeto:

```bash
cd Guardi-o-H-drico
```

### 3. Acesse o aplicativo mobile

```bash
cd mobile
```

### 4. Instale as dependências

```bash
npm install
```

Esse comando instala as dependências declaradas no `package.json`, utilizando o arquivo `package-lock.json` quando disponível para reproduzir as versões registradas.

Não é necessário instalar manualmente cada biblioteca utilizada no projeto.

### 5. Inicie o Expo

```bash
npx expo start
```

Após a inicialização, o terminal exibirá as opções para abrir o aplicativo.

- **Celular físico:** escaneie o QR code com o Expo Go, conforme as instruções exibidas.
- **Emulador Android:** abra o Android Studio, inicie um emulador e utilize a opção indicada pelo Expo.
- **Navegador:** pressione `w`, se o suporte web estiver disponível e configurado.

Caso o dispositivo não consiga se conectar, verifique se o computador e o celular estão na mesma rede Wi-Fi. Se necessário, tente iniciar o servidor com:

```bash
npx expo start --tunnel
```

### 6. Executar diretamente no Android

Com o ambiente Android configurado e um emulador ou dispositivo disponível, também é possível executar:

```bash
npm run android
```

Confira os scripts disponíveis no `package.json` antes de utilizar comandos específicos.

## 📂 Estrutura do projeto

A estrutura principal do aplicativo está organizada da seguinte maneira:

```text
mobile/
├── assets/              # Imagens, ícones e outros recursos
├── scripts/             # Scripts auxiliares
├── src/
│   ├── app/
│   │   ├── _layout.tsx  # Configuração do layout e navegação
│   │   ├── index.tsx    # Tela inicial de monitoramento
│   │   ├── alerts.tsx   # Tela de alertas
│   │   ├── history.tsx  # Tela de histórico
│   │   ├── device.tsx   # Tela do dispositivo
│   │   └── explore.tsx  # Tela de exemplo do template Expo
│   ├── components/
│   │   └── app-tabs.tsx # Navegação inferior por abas
│   ├── constants/       # Constantes e tema da aplicação
│   ├── hooks/           # Hooks reutilizáveis
│   └── global.css       # Estilos globais
├── app.json             # Configuração do Expo
├── package.json         # Dependências e scripts
├── package-lock.json    # Registro das versões das dependências
└── tsconfig.json        # Configuração do TypeScript
```

A estrutura acima representa a organização prevista para as telas implementadas. Alguns arquivos ou diretórios poderão ser adicionados conforme a evolução do projeto.

## 🔌 Integração com o sistema

O aplicativo faz parte do projeto Guardião Hídrico Inteligente, que prevê a comunicação entre o ESP32, uma API central, o dashboard e o aplicativo mobile.

Arquitetura planejada:

```text
ESP32 + sensores
       |
       v
    API REST
       |
       +------ Dashboard Python
       |
       +------ Aplicativo React Native
```

O contrato de telemetria do projeto estabelece os principais dados que poderão ser compartilhados, incluindo:

- Identificador do dispositivo.
- Data e hora das leituras em UTC.
- Vazão em L/min.
- Volume em litros.
- Detecção de água.
- Estado reportado da válvula.
- Eventos e resultados de comandos.

Nesta etapa, as telas utilizam valores definidos localmente para demonstrar a interface. A conexão com a API e o recebimento de dados reais ainda precisam ser desenvolvidos.

## ⚠️ Observações importantes

- Os valores exibidos atualmente são simulados e não representam medições reais.
- O status de conexão apresentado na interface é ilustrativo.
- Os controles físicos da válvula ainda não estão conectados ao ESP32.
- O aplicativo não deve ser considerado um mecanismo de proteção autônomo enquanto a integração e os testes de hardware não forem concluídos.
- Não é necessário criar um novo repositório Git para desenvolver o aplicativo, pois ele faz parte do repositório principal do projeto.

## 🌱 Fluxo de desenvolvimento com Git

O desenvolvimento mobile deve ocorrer em uma branch própria para manter as alterações organizadas.

Criar uma branch:

```bash
git switch -c feat/mobile-app
```

Verificar as alterações:

```bash
git status
```

Registrar as mudanças:

```bash
git add mobile/
git commit -m "feat: desenvolve interface inicial mobile"
```

Enviar a branch para o GitHub:

```bash
git push -u origin feat/mobile-app
```

Depois, abra um Pull Request para revisão e integração com a branch principal, seguindo o fluxo combinado pela equipe.

## 📚 Referências

- [Repositório do Guardião Hídrico Inteligente](https://github.com/Ceistutis/Guardi-o-H-drico)
- [Documentação do React Native](https://reactnative.dev/docs/getting-started)
- [Documentação do Expo](https://docs.expo.dev/)
- [Documentação do Expo Router](https://docs.expo.dev/router/introduction/)

---

Desenvolvido como parte do projeto acadêmico **Guardião Hídrico Inteligente**, com foco no monitoramento do consumo de água e na identificação de possíveis vazamentos.
