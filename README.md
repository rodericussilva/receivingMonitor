# Projeto de Automação de Download e Verificação de Pedidos

Este projeto automatiza o download de pedidos de uma Lista de compras no SharePoint, aplica filtros e verifica o status dos pedidos em trânsito. Caso pedidos estejam há muito tempo em trânsito (conforme regra de negócio), o sistema envia alertas por e-mail para as partes interessadas.

## Índice

- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Como Executar](#como-executar)
- [Funcionalidades](#funcionalidades)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Tecnologias Utilizadas

- Python 3.8+
- Selenium
- Pandas
- WebDriver Manager para Chrome
- dotenv para carregar variáveis de ambiente
- smtplib para envio de e-mails

## Estrutura do Projeto

```bash
projeto/
├── download.py             # Script principal que faz o download dos pedidos.
├── verification.py         # Script que verifica os pedidos e envia alertas por e-mail.
├── .env                    # Arquivo contendo as variáveis de ambiente.
├── requirements.txt        # Dependências do projeto.
```

## Configuração do Ambiente

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/rodericussilva/receivingMonitor.git
    cd receivingMonitor
    ```

2. **Crie um ambiente virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # No Linux/MacOS
    venv\Scripts\activate      # No Windows
    ```

3. **Instale as dependências:**

    ```bash
    pip install selenium pandas python-dotenv webdriver-manager
    ```
   - `selenium`: Para automação do navegador.
   - `pandas`: Para manipulação dos dados do CSV.
   - `python-dotenv`: Para carregar variáveis de ambiente do arquivo `.env`.
   - `webdriver-manager`: Para gerenciar o WebDriver do Chrome automaticamente.

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```bash
smtp_server=seu_servidor_smtp
smtp_port=sua_porta_smtp
sender_email=seu_email
sender_password=sua_senha
```

Essas variáveis são usadas para enviar os e-mails de alerta.

## Como Executar

1. **Configurar URL e Credenciais:**
   - No arquivo `download.py`, substitua `'YourURL'` pela URL do SharePoint e `user@email.com.br` pelas credenciais de login.

2. **Executar o script principal:**

    ```bash
    python download.py
    ```

   O script realizará o login, aplicará os filtros e fará o download dos arquivos CSV.

3. **Verificar pedidos automaticamente em horários específicos:**

    O script `verification.py` inclui a função `monitor_schedule` que verifica os pedidos em horários pré-determinados (08:00, 14:00, 17:00). A verificação é iniciada logo após o download do arquivo.

   Este processo ficará em execução contínua, verificando e enviando alertas conforme a necessidade.

## Funcionalidades

- **Login Automático**: Realiza login no SharePoint e acessa a página de pedidos.
- **Filtro de Status**: Filtra os pedidos pelo status "EM TRÂNSITO".
- **Exportação de Dados**: Exporta os dados filtrados para um arquivo CSV.
- **Verificação de Pedidos**: Analisa o CSV exportado para identificar pedidos em trânsito há mais de 15 dias.
- **Envio de E-mails de Alerta**: Envia e-mails automáticos para informar sobre pedidos que excederam o tempo de trânsito.
- **Agendamento de Verificações**: Realiza a verificação em horários específicos ao longo do dia.

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/sua-feature`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona uma nova feature'`).
4. Envie para o branch principal (`git push origin feature/sua-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
