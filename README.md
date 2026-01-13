# Yield-Hunter-Bot
Bot em Python para varredura automática de investimentos em Renda Fixa (LCI/LCA/CDB) com alertas em tempo real via celular. 💰🚀

# 💰 Yubb Investment Scraper & Notifier

> **Automação em Python para monitoramento de renda fixa em tempo real.**

Este projeto é um bot desenvolvido em **Python** que realiza a varredura automática (Web Scraping) na plataforma de investimentos **Yubb**, filtra as melhores oportunidades com base em taxas pré-definidas (ex: acima de 110% do CDI) e envia notificações instantâneas para o celular via **ntfy.sh**.

Ideal para investidores que não querem perder janelas curtas de oportunidade no mercado secundário ou ofertas promocionais.

---

## 🚀 Funcionalidades

* **Web Scraping Automatizado:** Varre as ofertas de LCI, LCA, CDB e RDB.
* **Filtros Inteligentes:** Só alerta se o investimento atender aos critérios (Ex: Taxa > 110% CDI, Liquidez Diária, etc).
* **Notificações Mobile:** Integração com o app **Ntfy** para alertas push no Android/iOS assim que uma oportunidade é detectada.
* **Log de Execução:** Feedback visual no terminal sobre o status da varredura.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Coleta de Dados:** `Requests` / `BeautifulSoup` (ou `Selenium` - *ajuste conforme seu código*)
* **Notificações:** API do `ntfy.sh`
* **Manipulação de Dados:** `Pandas` (para estruturação das ofertas)

## 📱 Exemplo de Funcionamento

O script roda em background e monitora o mercado. Quando encontra uma oferta alvo:

```bash
🕵️  Iniciando varredura no Yubb...
🔎 Analisando 12 investimentos encontrados...
   > Item 1: 115,00% CDI
🔔 Notificação enviada para o celular!
   > Item 2: 95,00% CDI (Ignorado - Abaixo do alvo)
...
🏁 Sucesso! Alertas enviados.
