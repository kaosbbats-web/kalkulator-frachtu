import streamlit as st

st.set_page_config(page_title="Kalkulator Frachtu - BBATS", page_icon="🚆", layout="centered")

# --- TUTAJ WKLEJ LINK DO LOGO BBATS ---
# Podmień poniższy adres na bezpośredni link do Waszego logo PNG/SVG
LOGO_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSckOvYDAd2OtrIpos8b4aAm_OR2xgFTONnHhLMgDjHvOeo4DPD8W3v-s4&s=10"

# --- WYŚWIETLANIE LOGO I NAGŁÓWKA ---
try:
    st.image(LOGO_URL, width=220)
except:
    # W razie braku poprawnego linku do logo wyświetli się czysty napis
    pass

st.title("🚆 Kalkulator Frachtu Kolejowego (RAIL)")
st.caption("System wycen frachtu międzynarodowego BBATS")

# --- BAZA MIAST I STAWEK FOB (USD za CBM) ---
RAIL_CITIES = {
    "CHONGQING": {"1:300": 100, "1:500": 107},
    "CHENGDU": {"1:300": 80, "1:500": 80},
    "XI'AN": {"1:300": 100, "1:500": 107},
    "BEIJING": {"1:300": 107, "1:500": 114},
    "TIANJIN": {"1:300": 105, "1:500": 112},
    "SHIJIAZHUANG": {"1:300": 257, "1:500": 264},
    "QINGDAO": {"1:300": 105, "1:500": 112},
    "JINAN": {"1:300": 257, "1:500": 264},
    "GUANGZHOU": {"1:300": 100, "1:500": 107},
    "SHENZHEN": {"1:300": 100, "1:500": 107},
    "ZHONGSHAN": {"1:300": 257, "1:500": 264},
    "SHANTOU": {"1:300": 107, "1:500": 114},
    "FUZHOU": {"1:300": 105, "1:500": 112},
    "XIAMEN": {"1:300": 107, "1:500": 114},
    "SHANGHAI": {"1:300": 100, "1:500": 107},
    "NINGBO": {"1:300": 100, "1:500": 107},
    "HANGZHOU": {"1:300": 105, "1:500": 112},
    "YIWU": {"1:300": 105, "1:500": 112},
    "CHANGSHA": {"1:300": 100, "1:500": 107},
    "TAIZHOU": {"1:300": 257, "1:500": 264},
    "WENZHOU": {"1:300": 105, "1:500": 112},
    "NANJING": {"1:300": 257, "1:500": 264},
    "WUXI": {"1:300": 105, "1:500": 112},
    "KUNSHAI": {"1:300": 257, "1:500": 264},
    "SUZHOU": {"1:300": 105, "1:500": 112},
    "WUHAN": {"1:300": 105, "1:500": 112},
    "LIAOCHENG": {"1:300": 257, "1:500": 264},
    "HEFEI": {"1:300": 105, "1:500": 112},
    "ZHENGZHOU": {"1:300": 105, "1:500": 112}
}

# --- FUNKCJA OBLICZAJĄCA PICK-UP (EXW) ---
def get_pickup_cost(cbm):
    if cbm <= 0.5:
        return 30
    elif cbm <= 3:
        return 65
    elif cbm <= 6:
        return 75
    elif cbm <= 9:
        return 75
    elif cbm <= 12:
        return 85
    else:
        return 95

# --- FORMULARZ WEJŚCIOWY ---
col1, col2 = st.columns(2)

with col1:
    mode = st.selectbox("Środek transportu", ["Kolejowy (RAIL)", "Morski LCL (Wyzerowany)"])
    city = st.selectbox("Miasto nadania w Chinach", list(RAIL_CITIES.keys()))
    incoterm = st.radio("Warunki dostawy", ["FOB", "EXW"], horizontal=True)

with col2:
    weight = st.number_input("Waga całkowita (kg)", min_value=1.0, value=500.0, step=10.0)
    volume = st.number_input("Objętość (CBM)", min_value=0.1, value=2.0, step=0.1)
    usd_rate = st.number_input("Kurs USD/PLN", min_value=3.0, value=4.00, step=0.01)

st.divider()

# --- LOGIKA OBLICZEŃ ---
if mode == "Morski LCL (Wyzerowany)":
    st.warning("⚠️ Morski transport jest obecnie ustawiony na 0 USD.")
    st.metric("Koszt całkowity USD", "$0.00 USD")
else:
    density_ratio = weight / volume if volume > 0 else 0
    
    if density_ratio > 300:
        rate_type = "1:500"
        chargeable_cbm = max(volume, weight / 500)
    else:
        rate_type = "1:300"
        chargeable_cbm = max(volume, weight / 300)
    
    base_rate_usd = RAIL_CITIES[city][rate_type]
    fob_freight_usd = chargeable_cbm * base_rate_usd

    pickup_usd = 0
    doc_fee_usd = 0
    export_license_usd = 0
    customs_export_usd = 0

    if incoterm == "EXW":
        pickup_usd = get_pickup_cost(volume)
        doc_fee_usd = 100 if volume <= 1.0 else 150
        export_license_usd = 40
        customs_export_usd = 60

    exw_total_usd = pickup_usd + doc_fee_usd + export_license_usd + customs_export_usd
    total_usd = fob_freight_usd + exw_total_usd
    total_pln = total_usd * usd_rate

    # --- WYNIKI ---
    st.subheader(f"📊 Wycena BBATS: {city} ➔ Polska")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    col_res1.metric("Suma USD", f"${total_usd:,.2f}")
    col_res2.metric("Suma PLN", f"{total_pln:,.2f} PLN")
    col_res3.metric("Stawka za CBM", f"{rate_type} (${base_rate_usd}/CBM)")

    st.write("### Szczegółowe rozbicie kosztów (USD):")
    st.write(f"- **Fracht Kolejowy (FOB):** ${fob_freight_usd:.2f} USD *(Płatne CBM: {chargeable_cbm:.2f})*")
    
    if incoterm == "EXW":
        st.write("**Koszty lokalne EXW (Chiny):**")
        st.write(f"  - Pick-up (dojazd): ${pickup_usd:.2f} USD")
        st.write(f"  - Opłata dokumentacyjna: ${doc_fee_usd:.2f} USD")
        st.write(f"  - Licencja eksportowa: ${export_license_usd:.2f} USD")
        st.write(f"  - Odprawa eksportowa: ${customs_export_usd:.2f} USD")
        st.write(f"  - *Razem dopłata EXW:* **${exw_total_usd:.2f} USD**")
