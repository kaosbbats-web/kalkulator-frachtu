import streamlit as st

st.set_page_config(page_title="Kalkulator Frachtu", page_icon="🚢", layout="centered")

st.title("🚢 Kalkulator Wyceny Frachtu do Polski")
st.caption("Przykładowe szacunkowe wyceny transportu międzynarodowego")

# --- WPROWADZANIE DANYCH ---
col1, col2 = st.columns(2)

with col1:
    origin = st.selectbox("Kraj pochodzenia", ["Chiny", "Wietnam", "Indie", "USA"])
    mode = st.selectbox("Środek transportu", ["Morski LCL (dodrobnica)", "Morski FCL (20' DV)", "Kolejowy LCL", "Lotniczy"])

with col2:
    weight = st.number_input("Waga ładunku (kg)", min_value=1.0, value=500.0, step=10.0)
    volume = st.number_input("Objętość (CBM / m³)", min_value=0.1, value=2.5, step=0.1)

incoterm = st.radio("Warunki dostawy (Incoterm)", ["FOB (Dostawca płaci za transport do portu)", "EXW (Pełny koszt od fabryki)"], horizontal=True)

# --- PRZYKŁADOWY CENNIK (BAZA STAWEK BIZNESOWYCH) ---
# Stawki w USD (można łatwo zmieniać na własne)
RATES = {
    "Morski LCL (dodrobnica)": {"unit": "CBM", "price": 85, "min": 150, "time": "35-45 dni"},
    "Morski FCL (20' DV)": {"unit": "FLAT", "price": 2100, "min": 2100, "time": "35-40 dni"},
    "Kolejowy LCL": {"unit": "CBM", "price": 160, "min": 250, "time": "16-22 dni"},
    "Lotniczy": {"unit": "KG", "price": 4.8, "min": 120, "time": "4-7 dni"}
}

USD_PLN = 4.00  # Stały przelicznik lub pobierany z API NBP
CUSTOMS_FEE = 350 # Koszt odprawy celnej w PLN
THC_FEE = 450     # Koszt obsługi portowej/terminalowej w PLN

# --- OBLICZENIA ---
selected_mode = RATES[mode]
transit_time = selected_mode["time"]

if selected_mode["unit"] == "CBM":
    freight_usd = max(volume * selected_mode["price"], selected_mode["min"])
elif selected_mode["unit"] == "KG":
    # W lotnictwie obowiązuje waga płatna (Volume Weight: 1 CBM = 167 kg)
    chargeable_weight = max(weight, volume * 167)
    freight_usd = max(chargeable_weight * selected_mode["price"], selected_mode["min"])
else:  # FLAT rate dla kontenera
    freight_usd = selected_mode["price"]

if incoterm.startswith("EXW"):
    exw_pickup_usd = 150 + (volume * 15)  # Szacowany koszt podjęcia z fabryki
else:
    exw_pickup_usd = 0

freight_pln = (freight_usd + exw_pickup_usd) * USD_PLN
total_pln = freight_pln + CUSTOMS_FEE + THC_FEE

# --- WYŚWIETLANIE WYNIKÓW ---
st.divider()
st.subheader("📊 Szacowany koszt transportu")

col_res1, col_res2 = st.columns(2)
col_res1.metric("Łączna kwota PLN", f"{total_pln:,.2f} PLN")
col_res2.metric("Czas transportu", transit_time)

st.write("**Rozbicie kosztów na czynniki pierwsze:**")
st.write(f"- Fracht główny: **${freight_usd:.2f} USD** ({freight_usd * USD_PLN:,.2f} PLN)")
if exw_pickup_usd > 0:
    st.write(f"- Podjęcie EXW od dostawcy: **${exw_pickup_usd:.2f} USD** ({exw_pickup_usd * USD_PLN:,.2f} PLN)")
st.write(f"- Portowe opłaty lokalne (THC/Handling): **{THC_FEE} PLN**")
st.write(f"- Agencja celna (odprawa w PL): **{CUSTOMS_FEE} PLN**")

st.info("💡 Wskazówka: Ostateczna cena zależy od klasyfikacji kodu HS towaru oraz cen paliwa (BAF/CAF).")
