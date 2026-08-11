import streamlit as st

st.set_page_config(page_title="Kalkulator BBATS - FCL & LCL", page_icon="🚢", layout="centered")

LOGO_URL = "https://raw.githubusercontent.com/kaosbbats-web/kalkulator-frachtu/main/logo.png"

try:
    st.image(LOGO_URL, width=220)
except:
    pass

st.title("📦 Kalkulator Frachtu BBATS")
st.caption("Kompleksowe wyceny RAIL (LCL/FCL) oraz SEA (FCL)")

# --- STAWKI FCL RAIL (Małaszewicze) ---
RAIL_FCL_RATES = {
    "Shanghai": {"40'HC": 4800},
    "Shenzhen": {"40'HC": 4500},
    "Ningbo": {"40'HC": 4700},
    "Tianjin": {"40'HC": 5100},
    "Xiamen": {"40'HC": 4800},
    "Dalian": {"40'HC": 5400},
    "Wuhan": {"40'HC": 4600},
    "Changsha": {"40'HC": 4100},
    "Chengdu": {"40'HC": 4100}
}

# --- STAWKI FCL MORSKI (Gdańsk/Gdynia) ---
SEA_FCL_RATES = {
    "Shanghai": {"20'DV": 625, "40'HC": 1075},
    "Shenzhen": {"20'DV": 625, "40'HC": 1075},
    "Ningbo": {"20'DV": 625, "40'HC": 1075},
    "Guangzhou": {"20'DV": 675, "40'HC": 1075},
    "Qingdao": {"20'DV": 675, "40'HC": 1100},
    "Tianjin": {"20'DV": 675, "40'HC": 1100},
    "Xiamen": {"20'DV": 625, "40'HC": 1075},
    "Dalian": {"20'DV": 675, "40'HC": 1100}
}

# --- FORMULARZ ---
service_type = st.selectbox("Wybierz usługę", ["Kolej FCL (RAIL)", "Morski FCL (SEA)", "Kolej LCL (Drobnica)"])

if service_type == "Kolej FCL (RAIL)":
    pol = st.selectbox("POL (Port załadunku)", list(RAIL_FCL_RATES.keys()))
    container = st.selectbox("Typ kontenera", ["40'HC"])
    rate_usd = RAIL_FCL_RATES[pol][container]
    pod = "Małaszewicze"

elif service_type == "Morski FCL (SEA)":
    pol = st.selectbox("POL (Port załadunku)", list(SEA_FCL_RATES.keys()))
    container = st.selectbox("Typ kontenera", ["20'DV", "40'HC"])
    rate_usd = SEA_FCL_RATES[pol][container]
    pod = "Gdańsk / Gdynia"

else:
    st.info("Dla LCL przejdź do widoku przelicznika wagi/objętości CBM.")
    rate_usd = 0
    pod = "Polska"

usd_rate = st.number_input("Kurs USD/PLN", min_value=3.0, value=4.00, step=0.01)

st.divider()

# --- WYNIK ---
if service_type != "Kolej LCL (Drobnica)":
    total_pln = rate_usd * usd_rate
    
    st.subheader(f"📊 Trasa: {pol} ➔ {pod}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Stawka USD", f"${rate_usd:,.2f}")
    col2.metric("Suma PLN", f"{total_pln:,.2f} PLN")
    col3.metric("Sprzęt", container)
