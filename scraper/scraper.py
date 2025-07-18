from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import re
from datetime import datetime


def clean_location_value(value: str) -> str:
    return re.sub(r",\s*$", "", value.strip())

# === CONFIGURACIÓN ===
fecha_checkin = "25/08/2025"
fecha_checkout = "31/08/2025"
checkin = datetime.strptime(fecha_checkin, "%d/%m/%Y")
checkout = datetime.strptime(fecha_checkout, "%d/%m/%Y")
num_noches = (checkout - checkin).days

PATH = "C:\\Tools\\chromedriver\\chromedriver.exe"
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(service=Service(PATH), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# === ENTRADA INICIAL ===
driver.get("https://es.rentalia.com/alquiler-apartamentos-malaga/")
time.sleep(3)

try:
    driver.find_element(By.ID, "didomi-notice-agree-button").click()
    time.sleep(1)
except:
    pass

driver.execute_script(f"""
    let entrada = document.querySelector('#checkinSearcher');
    entrada.value = '{fecha_checkin}';
    entrada.dispatchEvent(new Event('input', {{bubbles: true}}));
    entrada.dispatchEvent(new Event('change', {{bubbles: true}}));

    let salida = document.querySelector('#checkoutSearcher');
    salida.value = '{fecha_checkout}';
    salida.dispatchEvent(new Event('input', {{bubbles: true}}));
    salida.dispatchEvent(new Event('change', {{bubbles: true}}));
""")
time.sleep(1)

# === 1 persona ===
try:
    for _ in range(0):
        driver.find_element(By.CSS_SELECTOR, "button.btn-floating.waves-effect.waves").click()
        time.sleep(0.3)
except:
    pass

try:
    btn_buscar = driver.find_element(By.CSS_SELECTOR, "button.searchButton")
    driver.execute_script("arguments[0].click();", btn_buscar)
    time.sleep(5)
except:
    pass

def extraer_anuncios():
    lista = []
    cards = driver.find_elements(By.CSS_SELECTOR, "div.itemRow")
    print(f"Anuncios encontrados en esta p\u00e1gina: {len(cards)}")

    for card in cards:
        try:
            titulo = card.find_element(By.CSS_SELECTOR, "div.title h3").text.strip()
            enlace = card.find_element(By.CSS_SELECTOR, "div.title a").get_attribute("href")

            # === VARIABLES ===
            registro_turistico = "N/A"
            registro_alquiler = "N/A"
            referencia_rentalia = "N/A"
            propietario = "N/A"
            propietario_verificado = "N/A"
            direccion_verificada = "N/A"
            antiguedad_verificada = "N/A"
            telefono = "N/A"

            # === ENTRAR AL ANUNCIO ===
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(enlace)
            time.sleep(3)

            try:
                contact_block = driver.find_element(By.CSS_SELECTOR, "p.contactTitle")
                propietario_raw = contact_block.text.strip()
                propietario = propietario_raw.split("verificado")[0].strip()
                try:
                    contact_block.find_element(By.CSS_SELECTOR, "span.verified")
                    propietario_verificado = "yes"
                except:
                    propietario_verificado = "no"
            except:
                pass

            try:
                bloques_verificacion = driver.find_elements(By.CSS_SELECTOR, "div.verifiedInfo.col.s12 p.title")
                for p in bloques_verificacion:
                    texto = p.text.strip().lower()
                    if "dirección verificada" in texto:
                        direccion_verificada = "yes"
                    elif "verificado por antigüedad" in texto:
                        antiguedad_verificada = "yes"
                if direccion_verificada == "N/A": direccion_verificada = "no"
                if antiguedad_verificada == "N/A": antiguedad_verificada = "no"
            except:
                pass

            try:
                tel_divs = driver.find_elements(By.CSS_SELECTOR, "div.editButtons.col.s12 a")
                for a in tel_divs:
                    try:
                        i_tag = a.find_element(By.TAG_NAME, "i")
                        if "phone" in i_tag.text.strip().lower():
                            telefono = a.text.replace("phone", "").strip()
                            break
                    except:
                        continue
            except:
                pass

            try:
                house_div = driver.find_element(By.CSS_SELECTOR, "div.houseId")
                parrafos = house_div.find_elements(By.TAG_NAME, "p")
                for p in parrafos:
                    label = p.text.strip().lower()
                    if "registro turístico" in label:
                        span = p.find_element(By.TAG_NAME, "span")
                        registro_turistico = span.text.strip()
                    elif "registro de alquiler" in label:
                        span = p.find_element(By.TAG_NAME, "span")
                        registro_alquiler = span.text.strip()
                    elif "referencia rentalia" in label:
                        span = p.find_element(By.TAG_NAME, "span")
                        referencia_rentalia = span.text.strip()
            except:
                pass

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            
            # === Localidad, municipio, provincia ===
            localidad = "N/A"
            municipio = "N/A"
            provincia = "N/A"
            try:
                spans = card.find_elements(By.CSS_SELECTOR, "div.title.col.s12 h4.truncate span")
                if len(spans) == 3:
                    localidad = clean_location_value(spans[0].text)
                    municipio = clean_location_value(spans[1].text)
                    provincia = clean_location_value(spans[2].text)
                elif len(spans) == 2:
                    localidad = municipio = clean_location_value(spans[0].text)
                    provincia = clean_location_value(spans[1].text)
            except:
                pass

# === DATOS DEL CARD PRINCIPAL ===
            precio_texto = card.find_element(By.CSS_SELECTOR, "div.price").text.strip()
            m = re.search(r'(\d[\d.,]*)', precio_texto)
            total = float(m.group(1).replace('.', '').replace(',', '.')) if m else None
            precio_noche = round(total / num_noches, 2) if total else None

            try:
                style = card.find_element(By.CSS_SELECTOR, "div.stars div.percentage").get_attribute("style")
                pct = int(re.search(r"width\s*:\s*(\d+)", style).group(1))
                estrellas = round(pct / 100 * 5, 1)
            except:
                estrellas = 0

            try:
                val_html = card.find_element(By.CSS_SELECTOR, "div.valuations").get_attribute("innerHTML")
                m = re.search(r'<span[^>]*class="[^"]*truncate[^"]*"[^>]*>\s*(\d+)', val_html)
                opiniones = int(m.group(1)) if m else 0
            except:
                opiniones = 0

            txt = card.find_element(By.CSS_SELECTOR, "div.characteristics").text.lower().replace('\n', ' ')
            pm = re.search(r"(\d+)(?:\s*-\s*(\d+))?\s+personas?", txt)
            personas = pm.group(2) or pm.group(1) if pm else ""
            hm = re.search(r"(\d+)\s+habitaci[oó]n(?:es)?", txt)
            habitaciones = hm.group(1) if hm else ""
            cm = re.search(r"(\d+)\s+camas?", txt)
            camas = cm.group(1) if cm else ""
            try:
                html = card.find_element(By.CSS_SELECTOR, "p.capacityInfo").get_attribute("innerHTML").lower()
                match = re.search(r"item\.bathrooms[^>]*>\s*·?\s*(\d+)", html)
                banos = match.group(1) if match else ""
            except:
                banos = ""

            lista.append({
                "titulo": titulo,
                "localidad": localidad,
                "municipio": municipio,
                "provincia": provincia,
                "enlace": enlace,
                "precio_texto": precio_texto,
                "precio_total": total,
                "precio_noche": precio_noche,
                "estrellas": estrellas,
                "opiniones": opiniones,
                "personas": personas,
                "habitaciones": habitaciones,
                "camas": camas,
                "baños": banos,
                "propietario": propietario,
                "propietario_verificado": propietario_verificado,
                "direccion_verificada": direccion_verificada,
                "antiguedad_verificada": antiguedad_verificada,
                "telefono": telefono,
                "registro_turistico": registro_turistico,
                "registro_alquiler": registro_alquiler,
                "referencia_rentalia": referencia_rentalia,
                "fecha_desde": fecha_checkin,
                "fecha_hasta": fecha_checkout,
                "noches": num_noches,
            })
        except:
            continue
    return lista

# === RECORRER PAGINAS ===
todos = []
pagina = 1
while True:
    print(f"Procesando página {pagina}...")
    time.sleep(2)
    last, same = 0, 0
    while same < 2:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        curr = len(driver.find_elements(By.CSS_SELECTOR, "div.itemContent"))
        same = same + 1 if curr == last else 0
        last = curr

    todos += extraer_anuncios()
    try:
        nxt = driver.find_element(By.XPATH, "//a[contains(text(),'Siguiente')]")
        driver.execute_script("arguments[0].click();", nxt)
        pagina += 1
        time.sleep(4)
    except:
        print("No hay más páginas.")
        break

driver.quit()

# === GUARDAR CSV ===


def dividir_seguro(a, b):
    try:
        return round(float(a) / int(b), 2) if a and b and int(b) > 0 else None
    except:
        return None

df = pd.DataFrame(todos)
now = datetime.now()
df["fecha_extraccion"] = now.strftime("%d/%m/%Y")
df["hora_extraccion"] = now.strftime("%H:%M:%S")
df["precio_noche_persona"] = df.apply(lambda x: dividir_seguro(x["precio_noche"], x["personas"]), axis=1)
df["precio_noche_habitacion"] = df.apply(lambda x: dividir_seguro(x["precio_noche"], x["habitaciones"]), axis=1)
df["precio_noche_cama"] = df.apply(lambda x: dividir_seguro(x["precio_noche"], x["camas"]), axis=1)

for col in ["precio_total", "precio_noche", "precio_noche_persona", "precio_noche_habitacion", "precio_noche_cama"]:
    df[col] = df[col].apply(lambda x: f"{x:.2f}".replace(".", ",") if pd.notnull(x) else "")

columnas_ordenadas = [
    "id", "titulo", "localidad", "municipio", "provincia",
    "fecha_desde", "fecha_hasta", "noches",
    "precio_texto", "precio_total", "precio_noche",
    "precio_noche_persona", "precio_noche_habitacion", "precio_noche_cama",
    "opiniones", "estrellas", "personas", "habitaciones", "camas", "baños",
    "propietario", "propietario_verificado", "direccion_verificada",
    "antiguedad_verificada", "telefono",
    "registro_turistico", "registro_alquiler", "referencia_rentalia",
    "enlace", "fecha_extraccion", "hora_extraccion"
]

df.insert(0, "id", [f"R{i:05d}" for i in range(1, len(df) + 1)])
df = df[columnas_ordenadas]

fecha = datetime.now().strftime("%Y-%m-%d")
nombre = f"rentalia_cadiz_{fecha}.csv"
df.to_csv(nombre, index=False, sep=";", encoding="utf-8-sig")
print(f"\u2705 {len(df)} anuncios guardados en {nombre}")
