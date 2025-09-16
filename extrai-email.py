import requests
import re
import pandas as pd
import os

# Nome do arquivo Excel
ARQUIVO = "empresas_emails.xlsx"

# Função para extrair e-mails de um site
def extrair_emails(site):
    try:
        r = requests.get(site, timeout=10, headers={'User-Agent':'Mozilla/5.0'})
        html = r.text
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", html)
        return ", ".join(set(emails)) if emails else ""
    except Exception as e:
        print(f"Erro ao acessar {site}: {e}")
        return ""

def main():
    if not os.path.exists(ARQUIVO):
        # Primeira execução → cria o arquivo com a lista de sites (sem e-mails)
        sites = [
            "https://www.arcor.com.br",
            "https://www.painco.com.br"
            # 👉 coloque mais sites aqui na primeira execução
        ]
        df = pd.DataFrame({"site": sites, "emails": [""] * len(sites)})
        df.to_excel(ARQUIVO, index=False)
        print(f"Arquivo {ARQUIVO} criado. Preencha os sites e rode de novo para extrair e-mails.")
    else:
        # Execuções seguintes → abre o arquivo existente
        df = pd.read_excel(ARQUIVO)

        # Atualiza e-mails
        for i, row in df.iterrows():
            if pd.isna(row["emails"]) or row["emails"] == "":
                email = extrair_emails(row["site"])
                df.at[i, "emails"] = email
                print(f"{row['site']} → {email}")

        # Salva de volta
        df.to_excel(ARQUIVO, index=False)
        print(f"Arquivo {ARQUIVO} atualizado com os e-mails encontrados.")

if __name__ == "__main__":
    main()
