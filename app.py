import streamlit as st
import requests

# Page settings
st.set_page_config(page_title="Currency Converter 💱", layout="centered")

# Title
st.title("💱 Currency Converter")

st.markdown("### Convert currencies easily")

# Function to fetch conversion rate
def fetch_conversion_factor(source, target):
    api_key = "976a15c6f5679f761785d6a1"

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{source}/{target}"
    response = requests.get(url).json()

    if response['result'] == 'success':
        return response['conversion_rate']
    else:
        return None

# UI Layout (Form)
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("💰 Amount", min_value=0.0, value=1.0)
        from_currency = st.text_input("From Currency (e.g. USD)", value="USD")

    with col2:
        st.write("")  # spacing
        st.write("")
        to_currency = st.text_input("To Currency (e.g. PKR)", value="PKR")

# Convert button
if st.button("🔄 Convert"):
    if from_currency and to_currency:
        rate = fetch_conversion_factor(from_currency.upper(), to_currency.upper())

        if rate:
            result = round(amount * rate, 2)

            st.success(f"{amount} {from_currency.upper()} = {result} {to_currency.upper()}")

        else:
            st.error("❌ Conversion failed. Check currency codes.")
    else:
        st.warning("⚠️ Please enter both currencies")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("© 2026 M. Athar | Simple Currency Converter")
