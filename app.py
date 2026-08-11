import streamlit as st

st.set_page_config(page_title="Kalkulator Frachtu BBA", page_icon="🔴", layout="centered")

# --- STYLOWANIE CSS ---
st.markdown("""
    <style>
        .stApp {
            background-color: #c62828;
            color: #ffffff;
        }
        h1, h2, h3, p, label, span {
            color: #ffffff !important;
            font-family: 'Arial', sans-serif;
        }
        .bba-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            margin-bottom: 10px;
        }
        .bba-card-title {
            color: #555555 !important;
            font-size: 13px !important;
            font-weight: bold !important;
            margin-bottom: 5px !important;
            text-transform: uppercase;
        }
        .bba-card-value {
            color: #000000 !important;
            font-size: 24px !important;
            font-weight: 900 !important;
            margin: 0 !important;
        }
        div[data-baseweb="select"] > div, input {
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 6px !important;
        }
        div[data-baseweb="select"] * {
            color: #000000 !important;
        }
        hr {
            border-top: 2px solid #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER Z LOGO ---
col_logo, col_title = st.columns([1, 3])
with col_logo:
    try:
        st.image("logo.png", width=140)
    except:
        st.markdown("### **BBA**")

with col_title:
    st.title("Kalkulator Frachtu BBA")
    st.caption("Międzynarodowy Transport i Logistyka")

st.divider()

# --- BAZA STAWEK WARSAW, POLAND (Z GRAFIKI) ---
# Format: "MIASTO": {"less_300": stawka, "more_300": stawka}
RAIL_LCL_CITIES = {
    "CHENGDU": {"less_300": 145, "more_300": 145},
    "SHENZHEN": {"less_300": 165, "more_300": 172},
    "GUANGZHOU": {"less_300": 165, "more_300": 172},
    "CHONGQING": {"less_300": 165, "more_300": 172},
    "NINGBO": {"less_300": 165, "more_300": 172},
    "SHANGHAI": {"less_300": 165, "more_300": 172},
    "CHANGSHA": {"less_300": 165, "more_300": 172},
    "XI'AN": {"less_300": 165, "more_300": 172},
    "ZHENGZHOU": {"less_300": 165, "more_300": 172},
    "WUHAN": {"less_300": 165, "more_300": 172},
    "YIWU": {"less_300": 165, "more_300": 172},
    "CHANGZHOU": {"less_300": 170, "more_300": 177},
    "QINGDAO": {"less_300": 170, "more_300": 177},
    "TIANJIN": {"less_300": 170, "more_300": 177},
    "WENZHOU": {"less_300": 170, "more_300": 177},
    "NANJING": {"less_300": 170, "more_300": 177},
    "YANGZHOU": {"less_300": 170, "more_300": 177},
    "NANTONG": {"less_300": 170, "more_300": 177},
    "SUZHOU": {"less_300": 170, "more_300": 177},
    "HANGZHOU": {"less_300": 170, "more_300": 177},
    "WUXI": {"less_300": 170, "more_300": 177},
    "HEFEI": {"less_300": 170, "more_300": 177},
    "FUZHOU": {"less_300": 170, "more_300": 177},
    "SHANTOU": {"less_300": 172, "more_300": 179},
    "XIAMEN": {"less_300": 172, "more_300": 179},
    "BEIJING": {"less_300": 172, "more_300": 179}
}

def get_cbm_margin(cbm):
    if cbm <= 1.0:
        return 150
    elif cbm <= 4.0:
        return 90
    elif cbm <= 10.0:
        return 75
    elif cbm <= 20.0:
        return 50
    else:
        return 30

def get_pickup_cost(cbm):
    if cbm <= 0.5: return 30
    elif cbm <= 3: return 65
    elif cbm <= 6: return 75
    elif cbm <= 9: return 75
    elif cbm <= 12: return 85
    else: return 95

# --- FORMULARZ WYBORU ---
service_type = st.selectbox(
    "Środek transportu", 
    ["Kolej LCL (Drobnica)", "Kolej FCL (RAIL) 🚧 W BUDOWIE", "Morski FCL (SEA) 🚧 W BUDOWIE"]
)

if "W BUDOWIE" in service_type:
    st.warning("🚧 Ta usługa jest obecnie w budowie. Wybierz **Kolej LCL (Drobnica)**.")
else:
    usd_rate = st.number_input("Kurs USD/PLN", min_value=3.0, value=4.00, step=0.01)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        city = st.selectbox("Miasto nadania w Chinach", list(RAIL_LCL_CITIES.keys()))
        incoterm = st.radio("Warunki dostawy", ["FOB", "EXW"], horizontal=True)
    with col2:
        weight = st.number_input("Waga całkowita (kg)", min_value=1.0, value=500.0, step=10.0)
        volume = st.number_input("Objętość (CBM)", min_value=0.1, value=2.0, step=0.1)

    # Obliczenie gęstości
    density_ratio = weight / volume if volume > 0 else 0
    is_over_300 = density_ratio > 300
    
    # Przeliczeniowe CBM (waga płatna)
    rate_key = "more_300" if is_over_300 else "less_300"
    chargeable_cbm = max(volume, weight / 300)

    # Pobranie stawek
    base_rate_usd = RAIL_LCL_CITIES[city][rate_key]
    margin_per_cbm = get_cbm_margin(chargeable_cbm)
    
    # Końcowa stawka za CBM (baza + narzut z przedziału)
    final_rate_per_cbm = base_rate_usd + margin_per_cbm
    fob_freight_usd = chargeable_cbm * final_rate_per_cbm

    exw_total_usd = 0
    if incoterm == "EXW":
        pickup = get_pickup_cost(volume)
        doc = 100 if volume <= 1.0 else 150
        exw_total_usd = pickup + doc + 40 + 60

    total_usd = fob_freight_usd + exw_total_usd
    total_pln = total_usd * usd_rate

    st.subheader(f"📊 Wycena LCL: {city} ➔ Warszawa, Polska")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Suma USD</div><div class="bba-card-value">${total_usd:,.2f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Suma PLN</div><div class="bba-card-value">{total_pln:,.2f} PLN</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Stawka za CBM</div><div class="bba-card-value">${final_rate_per_cbm:.0f}</div></div>', unsafe_allow_html=True)

    st.write("### Szczegóły wyliczenia:")
    st.write(f"- **Płatne CBM:** `{chargeable_cbm:.2f} CBM` *(Waga: {weight} kg | Objętość: {volume} CBM)*")
    st.write(f"- **Stawka bazowa:** `${base_rate_usd}/CBM` *({'waga > 300kg/CBM' if is_over_300 else 'waga < 300kg/CBM'})*")
    st.write(f"- **Dopłata BBA (przedział CBM):** `+${margin_per_cbm}/CBM` *(dla {chargeable_cbm:.2f} CBM)*")
    st.write(f"- **Łączny fracht główny (FOB):** `${fob_freight_usd:.2f} USD`")
    
    if incoterm == "EXW":
        st.write(f"- **Koszty lokalne EXW w Chinach:** `${exw_total_usd:.2f} USD` *(Dojazd, Dokumenty, Licencja, Odprawa)*")
