import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Currency Converter 💱", layout="centered")

# Custom CSS for beauty
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .card {
        background-color: #1E1E1E;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
    }
    .title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# API function
def fetch_conversion_factor(source, target):
    api_key = "976a15c6f5679f761785d6a1"
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{source}/{target}"
    response = requests.get(url).json()

    if response['result'] == 'success':
        return response['conversion_rate']
    return None

# UI Card
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="title">💱 Currency Converter</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Fast • Simple • Beautiful</div>', unsafe_allow_html=True)

    # Currency list
    currencies = ["USD", "PKR", "EUR", "GBP", "INR", "AED", "SAR", "CNY"]

    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("Amount", min_value=0.0, value=100.0)
        from_currency = st.selectbox("From", currencies, index=0)

    with col2:
        st.write("")  # spacing
        st.write("")
        to_currency = st.selectbox("To", currencies, index=1)

    # Convert button (centered)
    st.markdown("<br>", unsafe_allow_html=True)
    convert = st.button("Convert 💱", use_container_width=True)

    # Result
    if convert:
        rate = fetch_conversion_factor(from_currency, to_currency)

        if rate:
            result = round(amount * rate, 2)

            st.markdown(f"""
                <h2 style='text-align: center; margin-top:20px;'>
                    {amount} {from_currency} = {result} {to_currency}
                </h2>
            """, unsafe_allow_html=True)
        else:
            st.error("Conversion failed ❌")

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 M. Athar | Designed with ❤️")
