import streamlit as st
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage

if 'messages' not in st.session_state:
    st.session_state.messages = []

def stream_chat(model, messages):
    try:
        llm = Ollama(model=model, request_timeout=120.0)
        res = llm.stream_chat(messages)
        response = ""
        for chunk in res:
            chunk_content = chunk.content if hasattr(chunk, "content") else str(chunk)
            response += chunk_content
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title("Local LLM Chat")
    model = st.sidebar.selectbox("Choose a model", ["llama3", "phi3", "mistral","gemma:2b"])
    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Writing..."):
                    try:
                        messages = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in st.session_state.messages]
                        response_message = stream_chat(model, messages)
                        st.session_state.messages.append({"role": "assistant", "content": response_message})
                    except Exception as e:
                        st.session_state.messages.append({"role": "assistant", "content": str(e)})
                        st.error("An error occurred while generating the response.")

if __name__ == "__main__":
    main()
