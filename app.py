import streamlit as st

st.set_page_config(page_title="Kalkulator Frachtu BBA", page_icon="🔴", layout="centered")

# --- STYLOWANIE CSS ---
st.markdown("""
    <style>
        /* Tło aplikacji */
        .stApp {
            background-color: #c62828;
            color: #ffffff;
        }

        /* Stylizacja nagłówków i tekstów */
        h1, h2, h3, p, label, span {
            color: #ffffff !important;
            font-family: 'Arial', sans-serif;
        }

        /* WŁASNE KAFELKI WYNIKOWE */
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
            font-size: 14px !important;
            font-weight: bold !important;
            margin-bottom: 5px !important;
            text-transform: uppercase;
        }
        .bba-card-value {
            color: #000000 !important;
            font-size: 26px !important;
            font-weight: 900 !important;
            margin: 0 !important;
        }

        /* Styling pól formularza */
        div[data-baseweb="select"] > div, input {
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 6px !important;
        }
        
        /* Kolor ikon i napisów wewnątrz selectboxów */
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
    # Pobieranie logo - jeśli plik lokalny lub z GitHub
    try:
        st.image("logo.png", width=140)
    except:
        st.markdown("### **BBA**")

with col_title:
    st.title("Kalkulator Frachtu BBA")
    st.caption("Międzynarodowy Transport i Logistyka")

st.divider()

# --- BAZA STAWEK RAIL LCL ---
RAIL_LCL_CITIES = {
    "CHONGQING": {"1:300": 100, "1:500": 107}, "CHENGDU": {"1:300": 80, "1:500": 80},
    "XI'AN": {"1:300": 100, "1:500": 107}, "BEIJING": {"1:300": 107, "1:500": 114},
    "TIANJIN": {"1:300": 105, "1:500": 112}, "SHIJIAZHUANG": {"1:300": 257, "1:500": 264},
    "QINGDAO": {"1:300": 105, "1:500": 112}, "JINAN": {"1:300": 257, "1:500": 264},
    "GUANGZHOU": {"1:300": 100, "1:500": 107}, "SHENZHEN": {"1:300": 100, "1:500": 107},
    "ZHONGSHAN": {"1:300": 257, "1:500": 264}, "SHANTOU": {"1:300": 107, "1:500": 114},
    "FUZHOU": {"1:300": 105, "1:500": 112}, "XIAMEN": {"1:300": 107, "1:500": 114},
    "SHANGHAI": {"1:300": 100, "1:500": 107}, "NINGBO": {"1:300": 100, "1:500": 107},
    "HANGZHOU": {"1:300": 105, "1:500": 112}, "YIWU": {"1:300": 105, "1:500": 112},
    "CHANGSHA": {"1:300": 100, "1:500": 107}, "TAIZHOU": {"1:300": 257, "1:500": 264},
    "WENZHOU": {"1:300": 105, "1:500": 112}, "NANJING": {"1:300": 257, "1:500": 264},
    "WUXI": {"1:300": 105, "1:500": 112}, "KUNSHAI": {"1:300": 257, "1:500": 264},
    "SUZHOU": {"1:300": 105, "1:500": 112}, "WUHAN": {"1:300": 105, "1:500": 112},
    "LIAOCHENG": {"1:300": 257, "1:500": 264}, "HEFEI": {"1:300": 105, "1:500": 112},
    "ZHENGZHOU": {"1:300": 105, "1:500": 112}
}

# --- BAZA STAWEK RAIL FCL ---
RAIL_FCL_RATES = {
    "Shanghai": 4800, "Shenzhen": 4500, "Ningbo": 4700, "Tianjin": 5100,
    "Xiamen": 4800, "Dalian": 5400, "Wuhan": 4600, "Changsha": 4100, "Chengdu": 4100
}

# --- BAZA STAWEK SEA FCL ---
SEA_FCL_RATES = {
    "Shanghai": {"20'DV": 625, "40'HC": 1075}, "Shenzhen": {"20'DV": 625, "40'HC": 1075},
    "Ningbo": {"20'DV": 625, "40'HC": 1075}, "Guangzhou": {"20'DV": 675, "40'HC": 1075},
    "Qingdao": {"20'DV": 675, "40'HC": 1100}, "Tianjin": {"20'DV": 675, "40'HC": 1100},
    "Xiamen": {"20'DV": 625, "40'HC": 1075}, "Dalian": {"20'DV": 675, "40'HC": 1100}
}

def get_pickup_cost(cbm):
    if cbm <= 0.5: return 30
    elif cbm <= 3: return 65
    elif cbm <= 6: return 75
    elif cbm <= 9: return 75
    elif cbm <= 12: return 85
    else: return 95

# --- FORMULARZ WYBORU ---
service_type = st.selectbox("Środek transportu", ["Kolej LCL (Drobnica)", "Kolej FCL (RAIL)", "Morski FCL (SEA)"])
usd_rate = st.number_input("Kurs USD/PLN", min_value=3.0, value=4.00, step=0.01)

st.divider()

# --- LOGIKA OBLICZEŃ ---
if service_type == "Kolej LCL (Drobnica)":
    col1, col2 = st.columns(2)
    with col1:
        city = st.selectbox("Miasto nadania w Chinach", list(RAIL_LCL_CITIES.keys()))
        incoterm = st.radio("Warunki dostawy", ["FOB", "EXW"], horizontal=True)
    with col2:
        weight = st.number_input("Waga całkowita (kg)", min_value=1.0, value=500.0, step=10.0)
        volume = st.number_input("Objętość (CBM)", min_value=0.1, value=2.0, step=0.1)

    density_ratio = weight / volume if volume > 0 else 0
    rate_type = "1:500" if density_ratio > 300 else "1:300"
    chargeable_cbm = max(volume, weight / (500 if rate_type == "1:500" else 300))
    
    base_rate_usd = RAIL_LCL_CITIES[city][rate_type]
    fob_freight_usd = chargeable_cbm * base_rate_usd

    exw_total_usd = 0
    if incoterm == "EXW":
        pickup = get_pickup_cost(volume)
        doc = 100 if volume <= 1.0 else 150
        exw_total_usd = pickup + doc + 40 + 60

    total_usd = fob_freight_usd + exw_total_usd
    total_pln = total_usd * usd_rate

    st.subheader(f"📊 Wycena LCL: {city} ➔ Polska")
    
    # RĘCZNIE GENEROWANE KAFELKI
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Suma USD</div><div class="bba-card-value">${total_usd:,.2f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Suma PLN</div><div class="bba-card-value">{total_pln:,.2f} PLN</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Przelicznik</div><div class="bba-card-value">{rate_type}</div></div>', unsafe_allow_html=True)

    st.write("### Szczegóły składowe (USD):")
    st.write(f"- **Fracht główny (FOB):** ${fob_freight_usd:.2f} USD *(Płatne CBM: {chargeable_cbm:.2f})*")
    if incoterm == "EXW":
        st.write(f"- **Koszty lokalne EXW (Chiny):** ${exw_total_usd:.2f} USD *(Dojazd, Dokumenty, Licencja, Odprawa)*")

elif service_type == "Kolej FCL (RAIL)":
    pol = st.selectbox("POL (Port załadunku)", list(RAIL_FCL_RATES.keys()))
    container = st.selectbox("Typ kontenera", ["40'HC"])
    rate_usd = RAIL_FCL_RATES[pol]
    total_pln = rate_usd * usd_rate

    st.subheader(f"📊 Trasa: {pol} ➔ Małaszewicze")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Stawka USD</div><div class="bba-card-value">${rate_usd:,.2f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Suma PLN</div><div class="bba-card-value">{total_pln:,.2f} PLN</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Sprzęt</div><div class="bba-card-value">{container}</div></div>', unsafe_allow_html=True)

elif service_type == "Morski FCL (SEA)":
    pol = st.selectbox("POL (Port załadunku)", list(SEA_FCL_RATES.keys()))
    container = st.selectbox("Typ kontenera", ["20'DV", "40'HC"])
    rate_usd = SEA_FCL_RATES[pol][container]
    total_pln = rate_usd * usd_rate

    st.subheader(f"📊 Trasa: {pol} ➔ Gdańsk / Gdynia")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Stawka USD</div><div class="bba-card-value">${rate_usd:,.2f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Suma PLN</div><div class="bba-card-value">{total_pln:,.2f} PLN</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="bba-card"><div class="bba-card-title">Sprzęt</div><div class="bba-card-value">{container}</div></div>', unsafe_allow_html=True)
