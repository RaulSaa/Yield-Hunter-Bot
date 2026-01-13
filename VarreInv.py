import time
import random
import requests
from playwright.sync_api import sync_playwright

# --- CONFIGURAÇÕES ---
NTFY_TOPIC = "op_casinhaKR_9596" 
URL_BASE = "https://yubb.com.br/investimentos/renda-fixa?investimento_type=prefixado"
TAXA_MINIMA = 13.0  
MAX_PAGINAS = 18

def enviar_ntfy(mensagem):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=mensagem.encode(encoding='utf-8'),
            headers={"Title": "Oportunidade Casinha KR", "Priority": "high", "Tags": "moneybag"}
        )
        print("🔔 Notificação enviada!")
    except Exception as e:
        print(f"❌ Erro ao notificar: {e}")

def tratar_taxa(texto):
    try:
        limpo = texto.replace("%", "").replace(" ", "").replace(",", ".")
        return float(limpo)
    except:
        return 0.0

def buscar_oportunidades():
    with sync_playwright() as p:
        print(f"🕵️  Iniciando varredura COM MEMÓRIA (Meta: >{TAXA_MINIMA}% Prefixado)")
        print("📁 Criando/Usando perfil em './sessao_yubb' para lembrar do CAPTCHA...")

        # --- MUDANÇA CRUCIAL: CONTEXTO PERSISTENTE ---
        # Isso salva cookies e cache numa pasta. O Cloudflare vai lembrar de você.
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./sessao_yubb", # Pasta onde salva os cookies
            headless=False,
            # Argumentos para parecer um Chrome normal
            args=[
                "--disable-blink-features=AutomationControlled", 
                "--start-maximized"
            ],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        
        page = browser.pages[0] # Pega a primeira aba aberta
        
        total_encontrados = 0
        pagina_atual = 1

        while pagina_atual <= MAX_PAGINAS:
            url_atual = f"{URL_BASE}&page={pagina_atual}"
            print(f"\n--- 📄 Acessando PÁGINA {pagina_atual} ---")
            
            try:
                page.goto(url_atual, timeout=60000)
                
                # Checagem de segurança (Loop de espera)
                tentativas = 0
                while tentativas < 120: # Espera até 2 minutos se precisar
                    try:
                        # Se achar o card, sai do loop de espera e segue a vida
                        if page.query_selector("article.investmentCard"):
                            break
                        
                        # Se não achou, verifica se tem um iframe de captcha ou texto de bloqueio
                        print(f"   ⏳ Esperando carregar (Tentativa {tentativas}/120)... Se tiver CAPTCHA, resolva!")
                        time.sleep(1)
                        tentativas += 1
                    except:
                        time.sleep(1)

                # Se passou do tempo e não carregou
                if not page.query_selector("article.investmentCard"):
                    print("❌ Tempo esgotado. Não consegui passar do bloqueio nesta página.")
                    break

                # --- COLETA DE DADOS (Igual ao anterior) ---
                cards = page.query_selector_all("article.investmentCard")
                qtd_cards = len(cards)
                
                if qtd_cards == 0:
                    print("Página vazia. Fim da lista.")
                    break

                print(f"🔎 Analisando {qtd_cards} cards...")

                for i, card in enumerate(cards):
                    try:
                        elemento_taxa = card.query_selector(".sugarish__number")
                        if elemento_taxa:
                            texto_taxa = elemento_taxa.inner_text().strip()
                            valor_taxa = tratar_taxa(texto_taxa)
                            
                            eh_cdi = False
                            try:
                                lbl = card.query_selector(".sugarish__cdi")
                                if lbl and "CDI" in lbl.inner_text(): eh_cdi = True
                            except: pass
                            
                            if eh_cdi: continue
                            
                            if valor_taxa < TAXA_MINIMA: continue

                            print(f"   > 💎 {texto_taxa}% -> ENCONTRADO!")
                            total_encontrados += 1
                            
                            resumo = card.inner_text().replace("\n", " ")[:150]
                            msg = f"🚀 Pág {pagina_atual}: {texto_taxa}%\n{resumo}...\nLink: {url_atual}"
                            enviar_ntfy(msg)
                            time.sleep(1)
                    except:
                        continue

                pagina_atual += 1
                
                # Pausa um pouco maior para garantir que o cookie salvou
                tempo_espera = random.uniform(5, 8)
                print(f"💤 Salvando sessão e esperando {tempo_espera:.1f}s...")
                time.sleep(tempo_espera)
                
            except Exception as e:
                print(f"Erro crítico: {e}")
                break

        browser.close()
        print(f"\n🏁 Fim da varredura. {total_encontrados} oportunidades.")

if __name__ == "__main__":
    buscar_oportunidades()
