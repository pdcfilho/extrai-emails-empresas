import os
import re
import requests
import pandas as pd
import dns.resolver

ARQUIVO = "empresas_emails.xlsx"

PADROES_COLUNAS = [
    "contato", "rh", "dp", "vendas", "comercial",
    "financeiro", "suporte", "sac", "administrativo",
    "info", "atendimento"
]

IGNORAR_DOMINIOS = {
    "instagram.com", "facebook.com", "wa.me", "whatsapp.com",
    "youtu.be", "youtube.com", "linktr.ee", "linktree.com",
    "wixsite.com", "bit.ly", "t.me", "telegram.me",
    "forms.gle", "sites.google.com", "notion.so"
}

# ---- limpeza ----
def limpar_host(url_ou_host: str) -> str:
    if not isinstance(url_ou_host, str):
        return ""
    s = url_ou_host.strip().lower()
    if not s:
        return ""
    if s.startswith("mailto:"):
        s = s[7:]
    if "://" in s:
        s = s.split("://", 1)[1]
    s = s.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
    if "@" in s and s.count("@") == 1:
        s = s.split("@", 1)[1]
    if s.startswith("www."):
        s = s[4:]
    if ":" in s:
        s = s.split(":", 1)[0]
    return s

def normalizar_email(e: str) -> str:
    if not isinstance(e, str):
        return ""
    e = e.strip().lower()
    if not e:
        return ""
    e = e.strip(" ,;:()[]{}<>\"'")
    if e.startswith("mailto:"):
        e = e[7:]
    if "@" not in e:
        return ""
    local, dom = e.split("@", 1)
    dom = limpar_host(dom)
    if not local or not dom:
        return ""
    return f"{local}@{dom}"

def limpar_lista_emails_str(celula: str) -> str:
    if not isinstance(celula, str) or not celula.strip():
        return celula
    partes = re.split(r"[,\s]+", celula)
    limpos, vistos = [], set()
    for p in partes:
        ne = normalizar_email(p)
        if ne and ne not in vistos:
            vistos.add(ne)
            limpos.append(ne)
    return ", ".join(limpos)

# ---- MX cache ----
_mx_cache: dict[str, bool] = {}
def dominio_tem_mx(dominio: str) -> bool:
    if not dominio:
        return False
    if dominio in _mx_cache:
        return _mx_cache[dominio]
    try:
        ans = dns.resolver.resolve(dominio, "MX")
        ok = len(ans) > 0
    except Exception:
        ok = False
    _mx_cache[dominio] = ok
    return ok

# ---- scraping simples ----
def extrair_emails_site(url: str) -> list[str]:
    try:
        html = requests.get(url, timeout=12, headers={"User-Agent":"Mozilla/5.0"}).text
        brutos = re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", html, flags=re.I)
        limpos, vistos = [], set()
        for e in brutos:
            ne = normalizar_email(e)
            if ne and ne not in vistos:
                vistos.add(ne)
                limpos.append(ne)
        return limpos
    except Exception:
        return []

def main():
    if not os.path.exists(ARQUIVO):
        print(f"Arquivo {ARQUIVO} não encontrado.")
        return

    df = pd.read_excel(ARQUIVO)

    # detecta a coluna que tem os sites
    if "site" in df.columns:
        site_col = "site"
    else:
        site_col = df.columns[0]  # assume que é a primeira

    # saneia colunas existentes com e-mails
    for col in list(df.columns):
        if "email" in col.lower():
            df[col] = df[col].apply(limpar_lista_emails_str)

    # garante colunas de chutados (e força tipo string)
    for col in PADROES_COLUNAS:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].astype(str)

    # colunas auxiliares (também como string)
    if "emails_extraidos" not in df.columns:
        df["emails_extraidos"] = ""
    df["emails_extraidos"] = df["emails_extraidos"].astype(str)

    if "mx_status" not in df.columns:
        df["mx_status"] = ""
    df["mx_status"] = df["mx_status"].astype(str)

    if "mx_ok" not in df.columns:
        df["mx_ok"] = ""
    df["mx_ok"] = df["mx_ok"].astype(str)

    for i, row in df.iterrows():
        site_raw = str(row.get(site_col, "")).strip()
        if not site_raw:
            continue

        host = limpar_host(site_raw)
        if not host:
            df.at[i, "mx_ok"] = "NAO"
            df.at[i, "mx_status"] = "host_invalido"
            continue

        # ignorar redes sociais
        base = host
        base_tld2 = ".".join(base.split(".")[-2:]) if "." in base else base
        if base in IGNORAR_DOMINIOS or base_tld2 in IGNORAR_DOMINIOS:
            for col in PADROES_COLUNAS:
                df.at[i, col] = ""
            df.at[i, "mx_ok"] = "IGNORADO"
            df.at[i, "mx_status"] = "ignorado_rede_social"
            continue

        # extrai e-mails reais
        if not str(df.at[i, "emails_extraidos"]).strip():
            url_busca = site_raw if site_raw.startswith(("http://","https://")) else f"https://{host}"
            extraidos = extrair_emails_site(url_busca)
            if extraidos:
                df.at[i, "emails_extraidos"] = ", ".join(extraidos)

        # checa MX
        if not dominio_tem_mx(host):
            for col in PADROES_COLUNAS:
                df.at[i, col] = ""
            df.at[i, "mx_ok"] = "NAO"
            df.at[i, "mx_status"] = "sem_mx"
            continue
        else:
            df.at[i, "mx_ok"] = "SIM"
            df.at[i, "mx_status"] = "mx_ok"

        # gera chutados
        for col in PADROES_COLUNAS:
            if pd.isna(df.at[i, col]) or str(df.at[i, col]).strip() == "":
                df.at[i, col] = f"{col}@{host}"

    df.to_excel(ARQUIVO, index=False)
    print("Arquivo atualizado com colunas como string, sem warnings.")

if __name__ == "__main__":
    main()
