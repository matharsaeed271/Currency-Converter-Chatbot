import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Currency Chatbot 💱", page_icon="💱")

st.title("💱 Currency Converter Chatbot")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to fetch conversion rate
def fetch_conversion_factor(source, target):
    api_key = "976a15c6f5679f761785d6a1"

    source = source.upper()
    target = target.upper()

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{source}/{target}"

    response = requests.get(url).json()

    if response['result'] == 'success':
        return response['conversion_rate']
    else:
        return None

# Function to process user input
def convert_currency(user_input):
    try:
        words = user_input.upper().split()

        # Example: "100 USD TO PKR"
        amount = float(words[0])
        source = words[1]
        target = words[3]

        rate = fetch_conversion_factor(source, target)

        if rate:
            result = round(amount * rate, 2)
            return f"{amount} {source} is {result} {target}"
        else:
            return "❌ Conversion failed"

    except:
        return "⚠️ Format: 100 USD to PKR"

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input("Type like: 100 USD to PKR")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Bot response
    response = convert_currency(user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.write("© 2026 M. Athar | Made with ❤️")
