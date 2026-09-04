def defang(text):
    text = text.replace("http://", "hxxp://")
    text = text.replace("https://", "hxxps://")
    text = text.replace(".", "[.]")
    return text

iocs_teste = [
    "http://malicious-phishing-login.com/auth",
    "185.220.101.5",
    "https://dropbox-fake-verify.org/download"
]

for item in iocs_teste:
    print(f"Original: {item} -> Defanged: {defang(item)}")