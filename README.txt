# Extrair e-mails de empresas a partir do Google Maps

Este projeto tem como objetivo ajudar pessoas a coletar sites de empresas listadas no Google Maps e, a partir disso, gerar endereços de e-mail de forma automatizada para facilitar o envio de currículos.

## Etapa 1 – Capturar empresas no Google Maps

1. Instale a extensão do Chrome chamada [Instant Data Scraper](https://chrome.google.com/webstore/detail/instant-data-scraper/).
2. Acesse o [Google Maps](https://www.google.com/maps).
3. Pesquise por algo como: empresas Cidade UF
4. Quando aparecer a lista de empresas na lateral, abra a extensão Instant Data Scraper.
5. Clique em “Locate Next button” para que ele continue passando pelas páginas de empresas.
6. Se quiser, ative a opção “Infinite scroll” para garantir que todos os resultados sejam coletados.
7. Quando terminar, clique em “XLSX” para exportar os dados para uma planilha.

## Etapa 2 – Preparar a planilha

- Renomeie o arquivo exportado para: empresas_emails.xlsx
- Coloque esse arquivo dentro da pasta do projeto, no mesmo local onde está o script `testa-email.py`.

## Etapa 3 – Instalar dependências do Python

Certifique-se de ter o Python instalado (versão 3 ou superior). Depois, instale as bibliotecas necessárias com o seguinte comando:

No terminal para instalar as dependências:
	pip install pandas requests dnspython openpyxl
Por último rode o script:
	python testa-email.py


##O que o script faz

Limpa e normaliza os domínios coletados (remove prefixos como www. e outros).
Ignora links de redes sociais ou atalhos (Instagram, Facebook, WhatsApp, etc.).
Testa se o domínio tem registros MX válidos (ou seja, se aceita e-mails).
Extrai e-mails que já estejam publicados no site.
Gera e-mails baseados em padrões comuns, como:
contato@dominio.com.br
rh@dominio.com.br
dp@dominio.com.br
vendas@dominio.com.br
comercial@dominio.com.br
financeiro@dominio.com.br
suporte@dominio.com.br
sac@dominio.com.br
administrativo@dominio.com.br
info@dominio.com.br
atendimento@dominio.com.br
Salva tudo no próprio arquivo empresas_emails.xlsx, criando novas colunas.


####Aviso importante

Este projeto deve ser utilizado apenas para fins profissionais legítimos, como envio de currículos e contatos comerciais. Não utilize para práticas de spam.

####Licença

Este projeto está sob a licença MIT. Isso significa que você pode usar, modificar e compartilhar, ajude quantas pessoas conseguir.


