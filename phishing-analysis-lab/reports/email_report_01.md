# Relatório de Triagem de Phishing — Amostra #01

## 1. Informações do Chamado
* **Ticket ID:** INC-2026-089
* **Data da Notificação:** 04/09/2026
* **Destinatário Original:** j***@target.corp (Mascarado)
* **Assunto (Subject):** URGENTE: Pagamento de fatura pendente

## 2. Análise do Cabeçalho
* **Endereço From (Exibido):** "Suporte Financeiro" <financeiro@empresa-legitima.com>
* **Reply-To:** cobranças@server-xyz-malicious.com (Divergente)
* **IP de Origem:** 185.220.101.5
* **Resultados de Autenticação:**
  * **SPF:** FAIL (IP não autorizado pelo domínio)
  * **DKIM:** FAIL / NONE
  * **DMARC:** FAIL (p=none ou falha de alinhamento)

## 3. Indicadores de Comprometimento (IOCs)
* **URLs Ofuscadas/Redirecionamentos:** `hxxps[://]auth-update-login[.]com/login` *(defang)*
* **Nome do Anexo:** `comprovante_fatura.pdf.exe`
* **Hash SHA-256 do Anexo:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## 4. Análise Dinâmica / Reputação
* **VirusTotal:** 42/72 detecções para o hash do anexo (Trojan/Dropper).
* **urlscan.io:** Identificada página clone da Microsoft solicitando credenciais corporativas.
* **ANY.RUN Sandbox:** Tentativa de conexão para C2 via IP `194.36.177.2` após execução.

## 5. Veredito e Ações Recomendadas (N1)
* **Veredito:** Verdadeiro Positivo — Phishing Malicioso / Credential Harvester.
* **Ações Tomadas/Recomendadas:**
  1. Purgar o e-mail das caixas de entrada de toda a organização via Exchange/Google Admin.
  2. Adicionar o domínio `auth-update-login[.]com` e o IP `185.220.101.5` à lista de bloqueio de borda/firewall e gateway de e-mail.
  3. Confirmar com o usuário se houve abertura do anexo ou preenchimento de senhas. Em caso afirmativo, revogar sessões e isolar o host preventivamente.