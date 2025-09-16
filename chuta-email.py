import pandas as pd
import os

# Nome do arquivo Excel com os sites
ARQUIVO = "empresas_emails.xlsx"

# Padrões de e-mail que vamos gerar
PADROES = [
    "contato@{dominio}",
    "rh@{dominio}",
    "dp@{dominio}",
    "vendas@{dominio}",
    "comercial@{dominio}",
    "financeiro@{dominio}",
    "suporte@{dominio}",
    "sac@{dominio}",
    "administrativo@{dominio}",
    "info@{dominio}",
    "atendimento@{dominio}"
]

def gerar_emails(dominio):
    emails = [padrao.format(dominio=dominio) for padrao in PADROES]
    return ", ".join(emails)

def main():
    if not os.path.exists(ARQUIVO):
        print(f"Arquivo {ARQUIVO} não encontrado. Rode o script anterior primeiro.")
        return
    
    df = pd.read_excel(ARQUIVO)

    # Gera os e-mails chutados com base no domínio
    for i, row in df.iterrows():
        site = row["site"]

        # extrair domínio do site
        dominio = site.replace("http://", "").replace("https://", "").split("/")[0]

        # gera lista de e-mails
        df.at[i, "emails_chutados"] = gerar_emails(dominio)

    # salva de volta
    df.to_excel(ARQUIVO, index=False)
    print(f"Arquivo {ARQUIVO} atualizado com os e-mails chutados.")

if __name__ == "__main__":
    main()