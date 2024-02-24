import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

def main():
    st.title('Welcome to SliderStats!')
    st.write('SliderStats allows you to explore data using sliders.')
    

if __name__ == "__main__":
    main()