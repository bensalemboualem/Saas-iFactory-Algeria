import streamlit as st
import sys
sys.path.append('/app/shared')
from streamlit_i18n import get_i18n, render_header

# Import agent components
from ai_consultant_agent import runner, APP_NAME, USER_ID, SESSION_ID

# Page config
st.set_page_config(
    page_title="AI Business Consultant",
    page_icon="🤖",
    layout="wide"
)

# Initialize i18n
i18n = get_i18n()

# Render trilingual header
render_header("consultant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input(i18n.t("consultant.input_placeholder")):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner(i18n.t("common.processing")):
            try:
                # Run the agent using the Google ADK Runner
                result = runner.run(
                    app_name=APP_NAME,
                    user_id=USER_ID,
                    session_id=SESSION_ID,
                    new_message=prompt
                )
                
                # Extract response
                if hasattr(result, 'messages') and result.messages:
                    # Get the last message from the agent
                    last_message = result.messages[-1]
                    if hasattr(last_message, 'content'):
                        response = last_message.content[0].text if hasattr(last_message.content[0], 'text') else str(last_message.content)
                    else:
                        response = str(last_message)
                else:
                    response = str(result)
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"{i18n.t('common.error')}: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar with info
with st.sidebar:
    st.markdown(f"### {i18n.t('consultant.features_title')}")
    st.markdown(i18n.t("consultant.features_list"))
    
    if st.button(i18n.t("common.clear_chat")):
        st.session_state.messages = []
        st.rerun()
