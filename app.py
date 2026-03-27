import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Currency Converter 💱", layout="centered")

# ----------- STYLE (Premium Look) -----------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.card {
    background-color: #1C1F26;
    padding: 40px;
    border-radius: 18px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
}
.title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 5px;
}
.subtitle {
    text-align: center;
    color: #A0A0A0;
    margin-bottom: 30px;
}
.result {
    text-align: center;
    font-size: 26px;
    font-weight: 600;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

# ----------- API FUNCTION -----------
def fetch_conversion_factor(source, target):
    api_key = "976a15c6f5679f761785d6a1"
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{source}/{target}"
    response = requests.get(url).json()

    if response['result'] == 'success':
        return response['conversion_rate']
    return None

# ----------- ALL CURRENCIES -----------
currencies = sorted([
    "USD","PKR","EUR","GBP","INR","AUD","CAD","AED","SAR","CNY","JPY","CHF",
    "NZD","ZAR","TRY","SGD","HKD","SEK","NOK","DKK","RUB","BRL","MXN","MYR",
    "THB","IDR","KRW","PLN","PHP","CZK","HUF","ILS","CLP","BDT","EGP"
])

# ----------- UI CARD -----------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="title">💱 Currency Converter</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Accurate • Clean • Professional</div>', unsafe_allow_html=True)

    # 🔹 LARGE AMOUNT BOX (Top Priority)
    amount = st.number_input(
        "Amount",
        min_value=0.0,
        value=100.0,
        step=1.0,
        format="%.2f"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 🔹 FROM currency (full width)
    from_currency = st.selectbox("From Currency", currencies, index=0)

    st.markdown("<br>", unsafe_allow_html=True)

    # 🔹 TO currency (full width)
    to_currency = st.selectbox("To Currency", currencies, index=1)

    # 🔹 BUTTON
    st.markdown("<br><br>", unsafe_allow_html=True)
    convert = st.button("Convert 💱", use_container_width=True)

    # 🔹 RESULT
    if convert:
        rate = fetch_conversion_factor(from_currency, to_currency)

        if rate:
            result = round(amount * rate, 2)

            st.markdown(f"""
                <div class="result">
                    {amount} {from_currency} = {result} {to_currency}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Conversion failed ❌")

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 M. Athar | Premium Converter UI")
