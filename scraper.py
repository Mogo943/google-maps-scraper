import csv
import time
from playwright.sync_api import sync_playwright

def scraping_localizado(busqueda, lat, lng, zoom=15):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Forzar el mapa a posicionarse en las coordenadas exactas de la zona
        url_busqueda = f"https://www.google.com/maps/search/{busqueda}/@{lat},{lng},{zoom}z"
        page.goto(url_busqueda)
        
        try:
            page.wait_for_selector('div[role="feed"]', timeout=10000)
        except Exception:
            print("[FAIL] No se encontraron resultados en esta zona.")
            browser.close()
            return

        # Scroll para cargar todos los comercios del cuadrante
        contenedor = page.locator('div[role="feed"]')
        for _ in range(20):
            contenedor.evaluate("el => el.scrollBy(0, 1000)")
            time.sleep(1.5)
            
        enlaces = [a.get_attribute("href") for a in page.locator('a[href*="/maps/place/"]').all()]
        enlaces_unicos = list(set([e for e in enlaces if e]))
        
        leads = []
        for url in enlaces_unicos:
            try:
                page.goto(url)
                page.wait_for_selector('h1', timeout=5000)
                
                # Evaluar presencia y tipo de sitio web
                nodo_web = page.locator('a[data-item-id="authority"]')
                tiene_web_propia = False
                link_instagram = "No tiene"
                
                if nodo_web.count() > 0:
                    href_web = nodo_web.get_attribute("href") or ""
                    if "instagram.com" in href_web.lower():
                        link_instagram = href_web
                    else:
                        tiene_web_propia = True # Tiene web corporativa real
                
                # Filtrar: Califica si no tiene web o si su única web es Instagram
                if not tiene_web_propia:
                    nombre = page.locator('h1').inner_text()
                    
                    btn_direccion = page.locator('button[data-item-id="address"]')
                    direccion = btn_direccion.inner_text() if btn_direccion.count() > 0 else "No disponible"
                    
                    btn_telefono = page.locator('button[data-item-id^="phone:tel:"]')
                    telefono = btn_telefono.get_attribute("data-item-id").replace("phone:tel:", "") if btn_telefono.count() > 0 else "No disponible"
                    
                    leads.append({
                        "Nombre": nombre,
                        "Direccion": direccion,
                        "Telefono": telefono,
                        "Instagram": link_instagram,
                        "URL_Maps": url
                    })
            except Exception:
                continue
                
        # Guardar base de datos refinada
        with open("leads_filtrados.csv", "w", newline="", encoding="utf-8") as f:
            campos = ["Nombre", "Direccion", "Telefono", "Instagram", "URL_Maps"]
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(leads)
            
        browser.close()

# Coordenadas aproximadas del centro de Palermo, CABA
scraping_localizado(busqueda="padel", lat="-34.5783", lng="-58.4266", zoom=15)