# 🎣 Phishing Analysis Lab & Playbook Operacional (SOC N1)

## 📖 Visão Geral
Este repositório contém um laboratório prático de **Triagem e Resposta a Incidentes de Phishing**, simulando o fluxo de trabalho real de um Analista de SOC Nível 1. Foram analisadas 10 amostras reais de e-mails suspeitos (amostras com cabeçalhos RFC 822 brutos), focando em dissecação de autenticação de e-mail, reputação de indicadores e detonação controlada em sandbox externa.

O projeto comprova capacidade técnica em:
- **Atendimento de chamados N1:** Análise de e-mails suspeitos reportados por colaboradores.
- **Engenharia de Detecção & Investigação:** Extração de saltos (`Received`), alinhamento SPF/DKIM/DMARC e evasão por `Reply-To`.
- **Análise Dinâmica e Estática Segura:** Mapeamento de IOCs sem execução de artefatos no host local.
- **Automação com Python:** Script nativo para parsing de arquivos `.eml` e sanitização (*defanging*) de IOCs.
- **Padronização:** Construção de Playbook de Triagem e Relatórios Técnicos de Incidente.

---

## 🏗️ Arquitetura do Repositório

```text
phishing-analysis/
├── README.md                          # Documentação executiva do projeto
├── playbook/
│   └── playbook_triagem_phishing.md   # Procedimento Operacional Padrão (SOP/Runbook)
├── reports/
│   ├── email_report_01.md             # Credential Harvester (Fake Login Microsoft)
│   ├── email_report_02.md             # Malicious Attachment (Trojan Dropper)
│   └── email_report_03.md             # Business Email Compromise / Spoofing
├── iocs/
│   └── ioc_table.csv                  # Tabela consolidada de indicadores (Defanged)
├── scripts/
│   ├── parse_email.py                 # Parser automatizado de cabeçalhos RFC 822
│   └── defang_iocs.py                 # Script de sanitização de URLs e IPs
└── samples_metadata/
    └── summary_10_samples.md          # Matriz de resumo dos 10 casos analisados

🛠️ Ferramental Utilizado
Etapa,Ferramenta / Recurso,Finalidade
Parsing & Automação,"Python 3 (email, re)",Extração automatizada de cabeçalhos brutos e saltos de rede
Análise de Cabeçalho,MXToolbox / Google Admin Toolbox,"Validação de alinhamento SPF, DKIM e DMARC"
Desofuscação,CyberChef,"Decodificação de parâmetros em Base64, Hex e URL-encode"
Reputação de Redes/Domínios,VirusTotal & Whois DomainTools,"Idade de domínios, ASN e listas de bloqueio globais"
Inspeção de Links,urlscan.io,Renderização passiva de DOM e captura de screenshots de páginas falsas
Detonação Dinâmica,ANY.RUN Sandbox (Community),Execução em máquina virtual descartável para captura de C2 e processos

⚙️ Automação Desenvolvida
Para acelerar a triagem de chamados, foram desenvolvidos utilitários em Python:

1. Parser Automatizado de E-mails (scripts/parse_email.py)
Lê diretamente arquivos brutos .eml sem renderização de HTML, isolando:

Endereço anunciado no campo From vs. campo Return-Path / Reply-To.

Registros de Authentication-Results (SPF, DKIM e DMARC).

Cadeia completa de servidores de salto (Received: from).

Lista de anexos e seus respectivos tipos MIME.
# Execução no terminal:
python scripts/parse_email.py samples_metadata/amostra1.eml

2. Sanitizador de IOCs (scripts/defang_iocs.py)
Sanitiza URLs e endereços de rede para prevenir cliques acidentais em relatórios e tickets, convertendo http:// para hxxp:// e pontuações de domínio para [.].

🛡️ Playbook Operacional de Triagem (Resumo)O fluxo segue o ciclo de tratamento do NIST SP 800-61:Ingestão: Recebimento do ticket e download seguro do .eml sem carregar imagens ou links no cliente de e-mail.Análise de Cabeçalho:Se SPF=fail, DKIM=fail ou DMARC=fail com alinhamento inconsistente $\rightarrow$ Forte indicativo de Spoofing.Discrepância entre From e Reply-To $\rightarrow$ Tentativa de redirecionamento de resposta.Inspeção de URLs: Verificação de domínio recém-registrado (< 30 dias) e varredura via urlscan.io.Inspeção de Anexos: Cálculo de Hash SHA-256 via terminal (Get-FileHash / sha256sum) e checagem no VirusTotal. Detonação no ANY.RUN caso a amostra seja inédita.Ações de Contenção & Erradicação:Bloqueio imediato de IP/Domínio no Firewall / Secure Email Gateway (SEG).Purga do e-mail em caixas de entrada de outros colaboradores via console do Exchange/Google Workspace.Notificação educativa ao usuário reportante.

📊 Matriz Consolidada de Indicadores de Comprometimento (IOCs)
Amostra,Tipo,Indicador (Defanged),Veredito,Impacto / Alvo
#01,IP,185.220.101[.]5,Malicioso,Servidor de origem (Tor Exit Node)
#01,URL,hxxps[://]auth-update-login[.]com/login,Phishing,Credential Harvester (Clone Microsoft 365)
#02,SHA-256,e3b0c44298fc1c149afbf4c8996fb92427ae...,Trojan,Dropper disfarçado de fatura (.pdf.exe)
#02,IP,194.36.177[.]2,C2 Server,Servidor de Comando & Controle mapeado no ANY.RUN

#03,Domínio,suporte-ti-financeiro[.]org,Spoofing,Typosquatting visando engenharia social
Procedimentos Operacionais
Quarentena e Coleta: Não clicar nos hiperlinks. Obter o e-mail em formato bruto (.eml ou .msg).

Execução de Script: Rodar python scripts/parse_email.py <amostra.eml> para mapear a infraestrutura de envio.

Enriquecimento:

Consultar reputação do IP de salto no AbuseIPDB / VirusTotal.

Checar se a data de criação do domínio do remetente é inferior a 30 dias.

Contenção Imediata:

Adicionar URLs/Domínios à Blocklist do SEG (Secure Email Gateway).

Executar busca e exclusão por Message-ID em todos os mailboxes corporativos.

Se o usuário inseriu credenciais: forçar redefinição de senha e revogação de sessões ativas (MFA reset).
