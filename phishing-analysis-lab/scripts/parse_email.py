import email
from email import policy
import sys
import re

def analyze_eml(file_path):
    with open(file_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    print("="*60)
    print("TRIAGEM AUTOMATIZADA DE E-MAIL - SOC TIER 1")
    print("="*60)
    print(f"[*] Assunto: {msg.get('Subject')}")
    print(f"[*] From (Exibido): {msg.get('From')}")
    print(f"[*] To: {msg.get('To')}")
    print(f"[*] Reply-To: {msg.get('Reply-To', 'Não definido')}")
    print(f"[*] Return-Path: {msg.get('Return-Path')}")
    print(f"[*] Message-ID: {msg.get('Message-ID')}")
    
    # Validações de Autenticação
    auth = msg.get('Authentication-Results', 'Nenhum registro encontrado')
    print("\n--- [Autenticação SPF / DKIM / DMARC] ---")
    print(auth)

    # Extração de Saltos (Received) e IPs
    print("\n--- [Rastreio de Saltos / IPs de Origem] ---")
    received_headers = msg.get_all('Received', [])
    for idx, h in enumerate(received_headers, 1):
        ips = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', h)
        print(f"Salto #{idx}: IPs encontrados -> {ips}")

    # Identificação de Anexos
    print("\n--- [Anexos Encontrados] ---")
    attachments = []
    for part in msg.walk():
        fn = part.get_filename()
        if fn:
            attachments.append(fn)
            print(f"[!] Anexo detectado: {fn} | Content-Type: {part.get_content_type()}")
    if not attachments:
        print("[+] Nenhum anexo encontrado.")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python parse_email.py <caminho_amostra.eml>")
    else:
        analyze_eml(sys.argv[1])