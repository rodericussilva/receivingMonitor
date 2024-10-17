import os
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv()

DOWNLOAD_FOLDER = "C:/Users/YourUser/Downloads"

def find_latest_csv():
    print("Procurando o arquivo CSV mais recente...")
    files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith('.csv')]
    if not files:
        print("Nenhum arquivo CSV encontrado na pasta de downloads.")
        return None
    files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_FOLDER, x)), reverse=True)
    latest_file = os.path.join(DOWNLOAD_FOLDER, files[0])
    print(f"Arquivo mais recente encontrado: {latest_file}")
    return latest_file

def check_orders():
    csv_path = find_latest_csv()
    if not csv_path:
        return

    print(f"Lendo o arquivo CSV: {csv_path}")
    try:
        df = pd.read_csv(csv_path, encoding='utf-8', delimiter=',')

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        print("Colunas do CSV:", df.columns.tolist())
        print("Conteúdo completo do CSV:")
        print(df)

        df.columns = df.columns.str.strip()

        required_columns = ['NF Nº', 'STATUS - COMPRA', 'DATA - EMISSÃO']
        if not all(col in df.columns for col in required_columns):
            print(f"Colunas encontradas no arquivo: {df.columns.tolist()}")
            print("Colunas necessárias não encontradas no arquivo.")
            return

        in_transit = df[df['STATUS - COMPRA'] == 'EM TRÂNSITO']
        print(f"{len(in_transit)} pedidos em trânsito encontrados.")
        print("Pedidos em trânsito:")
        print(in_transit)

        for index, row in in_transit.iterrows():
            try:
                issue_date = datetime.strptime(row['DATA - EMISSÃO'], '%d/%m/%Y')
                days_in_transit = (datetime.now() - issue_date).days

                if 15 <= days_in_transit < 18:
                    print(f"Enviando email para pedido NF {row['NF Nº']} em trânsito há {days_in_transit} dias.")
                    send_email(
                        subject=f"Alerta: Pedido NF {row['NF Nº']} em trânsito há {days_in_transit} dias",
                        body=f'''O pedido NF {row['NF Nº']} está em trânsito há {days_in_transit} dias desde {row['DATA - EMISSÃO']}.
                        Email de alerta automático, favor não responder.
                        '''
                    )
                elif days_in_transit == 18:
                    print(f"Enviando email crítico para pedido NF {row['NF Nº']} em trânsito há {days_in_transit} dias.")
                    send_email(
                        subject=f"Alerta Crítico: Pedido NF {row['NF Nº']} em trânsito por 18 dias",
                        body=f'''O pedido NF {row['NF Nº']} permanece em trânsito desde {row['DATA - EMISSÃO']}. Verificar imediatamente.
                        Email de alerta automático, favor não responder.
                        '''
                    )
            except Exception as e:
                print(f"Erro ao processar pedido NF {row['NF Nº']}: {e}")

    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")

def send_email(subject, body):
    smtp_server = os.getenv('smtp_server')
    smtp_port = os.getenv('smtp_port')
    sender_email = os.getenv('sender_email')
    sender_password = os.getenv('sender_password')

    recipients = ['user@email.com', 'user@email.com]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
        print("Email enviado com sucesso para:", ', '.join(recipients))
    except Exception as e:
        print("Erro ao enviar o e-mail:", e)

def monitor_schedule():
    check_times = ["08:00", "13:18", "17:00"]
    already_checked = set()

    while True:
        now = datetime.now().strftime("%H:%M")

        if now in check_times and now not in already_checked:
            print(f"Verificando alertas às {now}...")
            check_orders()
            already_checked.add(now)

        if now == "23:59":
            already_checked.clear()
            print("Lista de horários verificados foi resetada para o próximo dia.")

        time.sleep(60)

if __name__ == "__main__":
    monitor_schedule()
