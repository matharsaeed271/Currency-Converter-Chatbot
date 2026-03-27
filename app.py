import os
import json
import requests
import streamlit as st
# from dotenv import load_dotenv
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# -----------------------------
# Load .env
# -----------------------------
# load_dotenv()  # make sure GROQ_API_KEY is set here

# -----------------------------
# Full Currency List
# -----------------------------
CURRENCIES = [
    "USD", "EUR", "GBP", "PKR", "INR", "AUD", "CAD", "SGD", "AED", "SAR",
    "JPY", "CNY", "CHF", "NZD", "HKD", "SEK", "NOK", "DKK", "ZAR",
    "TRY", "RUB", "BRL", "MXN", "KRW", "MYR", "THB", "IDR",
    "PLN", "HUF", "CZK", "ILS", "PHP", "EGP", "KWD", "QAR",
    "BHD", "OMR", "LKR", "BDT", "NPR", "VND", "NGN", "KES"
]

# -----------------------------
# Helper Functions
# -----------------------------
def get_currency_param(param):
    if isinstance(param, list):
        param = param[0]
    if isinstance(param, dict) and 'currency' in param:
        param = param['currency']
    return param

def fetch_conversion_factor(source, target):
    api_key = "976a15c6f5679f761785d6a1"  # ExchangeRate API key
    source = source.upper()
    target = target.upper()
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{source}/{target}"
    response = requests.get(url).json()
    if response.get('result') == 'success':
        return response['conversion_rate']
    else:
        raise ValueError(f"Failed to get conversion rate: {response.get('error-type', 'Unknown error')}")

# -----------------------------
# Groq Chatbot Function with retry
# -----------------------------
# def ask_groq_llama(prompt):
#     api_key = os.environ.get("GROQ_API_KEY")
#     if not api_key:
#         raise ValueError("GROQ_API_KEY not set in environment")
    
#     url = "https://api.groq.com/openai/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json",
#     }

#     groq_prompt = f"""
# You are a JSON parser for currency conversion queries.
# Extract AMOUNT, SOURCE_CURRENCY, TARGET_CURRENCY.
# Always respond in *valid JSON only*, no extra text.

# Example:
# Input: "Convert 150 USD to PKR"
# Output: {{"amount":150,"source":"USD","target":"PKR"}}

# Now parse this query:
# \"\"\"{prompt}\"\"\"
# """

# body = {
#     "model": "llama-3.1-8b-instant",
#     "messages": [
#         {
#             "role": "system",
#             "content": """You are a JSON parser for currency conversion queries.
# Extract AMOUNT, SOURCE_CURRENCY, TARGET_CURRENCY.
# Return ONLY valid JSON like:
# {"amount":150,"source":"USD","target":"PKR"}"""
#         },
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ],
#     "temperature": 0.0,
#     "max_tokens": 80
# }

#     # Retry session for robustness
# session = requests.session()
# retries = Retry(total=3, backoff_factor=2, status_forcelist=[500,502,503,504])
# session.mount('https://', HTTPAdapter(max_retries=retries))

# res = session.post(url, json=body, headers=headers)
# res.raise_for_status()

# data = res.json()


# return data["choices"][0]["message"]["content"]
#######################################################
def ask_groq_llama(prompt):
    api_key = st.secrets["GROQ_API_KEY"]

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Return JSON only"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 80
    }

    session = requests.Session()
    retries = Retry(total=3, backoff_factor=2, status_forcelist=[500,502,503,504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    res = session.post(url, json=body, headers=headers)
    res.raise_for_status()

    data = res.json()

    return data["choices"][0]["message"]["content"]
#######################################################
# -----------------------------
# Handle User Queries (currency + normal conversation)
# -----------------------------
def handle_user_query(user_query):
    # Check if it's a currency conversion query
    if re.search(r"\d+", user_query) and re.search(r"(USD|PKR|EUR|GBP|INR|JPY|AUD|CAD|\$)", user_query.upper()):
        try:
            groq_response = ask_groq_llama(user_query)
            output_text = groq_response.strip()
            
            # Extract JSON safely
            match = re.search(r"\{.*?\}", output_text, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                amt = float(parsed.get("amount"))
                src = parsed.get("source").upper()
                tgt = parsed.get("target").upper()
                cf = fetch_conversion_factor(src, tgt)
                conv_result = round(amt * cf, 2)
                return f"{amt} {src} = {conv_result} {tgt}"
            else:
                return "Sorry, I couldn't parse the query 🤖"
        except Exception as e:
            return f"Error: {e}"
    else:
        # Normal conversation replies (brief)
        greetings = ["hi", "hello", "hey", "good morning", "good evening"]
        msg = user_query.lower()
        if msg in greetings:
            return "Hello! 😊"
        elif "how are you" in msg:
            return "I'm good, thanks! How about you? 🤗"
        else:
            return "I can help with currency conversion 💱. Try: 'Convert 100 USD to PKR'"

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Currency Converter & Chatbot", page_icon="💱")
st.title("💱 Currency Converter & Chatbot")
st.markdown("### Convert currencies instantly or ask in plain language 🌍💬")

# Classic Converter
st.subheader("🔁 Classic Currency Converter")
col1, col2 = st.columns(2)
with col1:
    source_currency = st.selectbox("From Currency", CURRENCIES, index=0)
with col2:
    target_currency = st.selectbox("To Currency", CURRENCIES, index=3)

amount = st.number_input("Amount", min_value=0.0, value=1.0)

if st.button("Convert 💸"):
    try:
        src = get_currency_param(source_currency)
        tgt = get_currency_param(target_currency)
        cf = fetch_conversion_factor(src, tgt)
        result = round(amount * cf, 2)
        st.success(f"{amount} {src} = {result} {tgt}")
    except Exception as e:
        st.error(f"Error: {e}")

# Chatbot Section
st.markdown("---")
st.subheader("🤖 Chatbot (Natural Language)")

user_query = st.text_input("Ask something like: 'Convert 150 USD to PKR'")

if st.button("Ask Chatbot"):
    reply = handle_user_query(user_query)
    st.success(reply)

# Footer
st.markdown("<hr style='border: 2px solid black;'>", unsafe_allow_html=True)
st.markdown("*Copy© 2026 M.Athar | Made With ❤️ by Muhammad Athar Ur Rahman*")
