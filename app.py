import streamlit as st
from indic_transliteration import sanscript
from sandhi_helper import sandhi_all

st.title("सन्धिं कुरु")
st.markdown('''
    Please enter a single sentence without any period (.) or (।)
    **Note**: Sometimes the sandhi results may not be complete/accurate
    
    Acknowledgements: This UI relies on:
    * [sandhi](https://github.com/hrishikeshrt/sandhi) python library
    * [indic_transliteration](https://github.com/indic-transliteration/indic_transliteration_py).
'''    
)

schemes = list(sanscript.brahmic.SCHEMES)
schemes.extend(sanscript.roman.SCHEMES)
dev_index = schemes.index(sanscript.DEVANAGARI)

with st.form("input_form"):
    left, right = st.columns(2, vertical_alignment="bottom")
    with left:
        input_trans = st.selectbox(
            "Input Transliteration",
            schemes,
            index=dev_index,
            key = "input_trans"
        )
    with right:
        output_trans = st.selectbox(
            "Output Transliteration",
            schemes,
            index=dev_index,
            key = "output_trans"
        )
        
    input_text = st.text_area("Input text to be sandhi-ed")
        
    submitted = st.form_submit_button("Submit")
    if submitted:
        input_text_dev = sanscript.transliterate(input_text, input_trans, sanscript.DEVANAGARI)
        # result = sandhi_builder(input_text_dev)
        result = sandhi_all(input_text_dev)
        st.subheader("Possible Sandhi-ed forms")
        for r in result:
            r_output = sanscript.transliterate(r, sanscript.DEVANAGARI, output_trans)
            st.text(r_output)