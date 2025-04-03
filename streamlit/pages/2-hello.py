import streamlit as st

name = st.text_input('Nome')

if name:
    st.text(f'Hello {name}')
    st.session_state['name'] = name 
else:
    st.text('Hello World!')

