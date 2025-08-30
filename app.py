import streamlit as st
from indic_transliteration import sanscript
from sandhi_helper import sandhi_all as sandhi_sandhi
from sanskrit_parser_helper import sandhi_all as sp_sandhi
from sanskrit_parser_helper import sanskrit_one
# The tree_view is no longer used since we disabled graph generation
# from streamlit_arborist import tree_view


st.title("सन्धिं कुरु")
st.markdown(
    """    
    **Note**: Sometimes the sandhi results may not be complete/accurate
    
    Acknowledgements:  [sandhi](https://github.com/hrishikeshrt/sandhi), 
    [sanskrit_parser](https://github.com/sanskrit-coders/sanskrit_parser),
    [indic_transliteration](https://github.com/indic-transliteration/indic_transliteration_py).
"""
)

# Use a new session state variable to store results from all libraries
if "all_results" not in st.session_state:
    st.session_state.all_results = None

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
    
    # The radio button for selecting a library is no longer needed
    # library = st.radio("Sandhi library to use:", ["sandhi", "sanskrit_one", "sanskrit_parser"], horizontal=True)

    top_n = st.slider("No. of forms to retain at each stage", 1, 10, 5, 1)
    input_text = st.text_area(
        "Input text to be sandhi-ed (Please enter a single sentence)"
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        # Create a dictionary to hold results from all functions
        all_results_dict = {}
        
        # Define the functions to run
        functions_to_run = {
            "sandhi (hrishikeshrt/sandhi)": sandhi_sandhi,
            "sanskrit_parser": sp_sandhi,
            "sanskrit_one (wrapper for sanskrit_parser)": sanskrit_one
        }
        
        # Run each function and store its results
        with st.spinner("Processing with all libraries..."):
            for name, func in functions_to_run.items():
                try:
                    # We ignore the graph object (_)
                    results, _ = func(input_text, top_n, input_trans, output_trans)
                    all_results_dict[name] = results
                except Exception as e:
                    all_results_dict[name] = [f"Error: {e}"]

        st.session_state.all_results = all_results_dict


# Display the results from the session state
if all_results := st.session_state.get("all_results"):
    st.header("Comparison of Sandhi Results")

    for library_name, results in all_results.items():
        st.markdown("---")
        st.subheader(f"Library: `{library_name}`")

        if results:
            st.text(f"Top result: {results[0]}")
            if len(results) > 1:
                with st.expander("Show all results from this library"):
                    # Use a bulleted list for better readability
                    for r in results:
                        st.markdown(f"- `{r}`")
        else:
            st.warning("No sandhi results found from this library.")