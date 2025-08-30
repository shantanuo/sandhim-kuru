import streamlit as st
from indic_transliteration import sanscript
from sandhi_helper import sandhi_all as sandhi_sandhi
from sanskrit_parser_helper import sandhi_all as sp_sandhi
from streamlit_arborist import tree_view


st.title("सन्धिं कुरु")
st.markdown(
    """    
    **Note**: Sometimes the sandhi results may not be complete/accurate
    
    Acknowledgements:  [sandhi](https://github.com/hrishikeshrt/sandhi), 
    [indic_transliteration](https://github.com/indic-transliteration/indic_transliteration_py).
"""
)

if "sandhi_output" not in st.session_state:
    st.session_state.sandhi_output = None

schemes = list(sanscript.brahmic.SCHEMES)
schemes.extend(sanscript.roman.SCHEMES)
dev_index = schemes.index(sanscript.DEVANAGARI)

with st.form("input_form"):
    left, right = st.columns(2, vertical_alignment="bottom")
    with left:
        input_trans = st.selectbox(
            "Input Transliteration", schemes, index=dev_index, key="input_trans"
        )
    with right:
        output_trans = st.selectbox(
            "Output Transliteration", schemes, index=dev_index, key="output_trans"
        )
    library = st.radio("Sandhi library to use:", ["sandhi", "sanskrit_one", "sanskrit_parser"], horizontal=True)

    if library == "sandhi":
        sandhi_fn = sandhi_sandhi
    elif library == "sanskrit_one":
        sandhi_fn = sanskrit_one
    else:
        sandhi_fn = sp_sandhi


    top_n = st.slider("No. of forms to retain at each stage", 1, 10, 5, 1)
    input_text = st.text_area(
        "Input text to be sandhi-ed (Please enter a single sentence)"
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        results, graph = sandhi_fn(
            input_text, top_n, input_trans, output_trans
        )
        st.session_state.sandhi_output = results
        st.session_state.graph_data = graph.to_tree_view()

if result := st.session_state.sandhi_output:
    st.subheader("Possible Sandhi-ed form:")
    st.text(result[0])
    if result[1:]:
        with st.expander("Show additional results"):
            for r in result:
                st.text(r)

    with st.expander("Show Full Sandhi Graph"):
        st.markdown("Use the arrows to navigate the graph and select the desired form")
        selected = tree_view(
            data=[st.session_state.graph_data],
            icons={
                "open": ":material/arrow_drop_down:",
                "closed": ":material/arrow_right:",
                "leaf": ":material/arrow_right_alt:"
            },
            open_by_default=False
        )
        if selected:
            st.markdown(f"Selected final form: {selected["name"]}")
