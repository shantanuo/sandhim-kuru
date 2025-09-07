import streamlit as st
from indic_transliteration import sanscript
from sandhi_helper import sandhi_all as sandhi_sandhi
from sanskrit_parser_helper import sandhi_all as sp_sandhi
from sanskrit_parser_helper import sanskrit_one
from sanskrit_parser_helper import arindam_sandhi
import requests
import urllib.parse

# For demonstration purposes, we'll simulate a database interaction.
# In a real application, you would replace this with actual AWS DynamoDB calls.
def save_to_dynamodb(sandhi_texts, source_library, input_text):
    murl = 'https://mq3lf5q5bbbqkfwrvu6pniibxu0kxikz.lambda-url.us-east-1.on.aws/?'
    if sandhi_texts:
        mystring = f"Reported mistake for input '{input_text}' from '{source_library}': {sandhi_texts}"
        encoded_msg = urllib.parse.quote(mystring, safe="")
        mresponse = requests.get(murl + encoded_msg)
        st.warning(mresponse.text)
    else:
        st.warning(f"No results to report from '{source_library}'.")
        

st.set_page_config(layout="wide") # Use the wide layout for better side-by-side comparison

st.title("Sandhi Maker")
st.markdown(
    """    
    **Note**: Sometimes the sandhi results may not be complete/accurate
    
    Acknowledgements:  [sandhi](https://github.com/hrishikeshrt/sandhi), 
    [sanskrit_parser](https://github.com/kmadathil/sanskrit_parser),
    [sanskrit_one](https://github.com/shantanuo/sandhi)
    [arindam_sandhi](https://github.com/arindamsaha1507/sandhi)
    
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

    top_n = st.slider("No. of forms to retain at each stage", 1, 10, 5, 1)
    input_text = st.text_area(
        "Input text to be sandhi-ed (Please enter a single sentence)"
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        # Create a dictionary to hold results from all functions
        all_results_dict = {}
        
        # Define the functions to run with user-friendly names
        functions_to_run = {
            "sandhi (hrishikeshrt/sandhi)": sandhi_sandhi,
            "sanskrit_parser": sp_sandhi,
            "sandhi (shantanuo/sandhi)": sanskrit_one,
            "sandhi (arindamsaha1507/sandhi)": arindam_sandhi
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

    # Get the library names and their results in a list to ensure order
    results_list = list(all_results.items())
    
    # Create 4 columns, one for each library's results
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]

    # Iterate over the columns and the results simultaneously
    for i, col in enumerate(cols):
        # Check if there's a result for this column (in case a function fails)
        if i < len(results_list):
            library_name, results = results_list[i]
            
            with col:
                st.subheader(library_name)
                
                if results:
                    # Display all results directly as a bulleted list
                    for r in results:
                        # Using markdown with backticks for a clear, code-formatted look
                        st.markdown(f"- `{r}`")
                else:
                    st.info("No results found.")
                
                # Place the single "Report mistake" button at the bottom of the column
                if st.button(f"Report mistake", key=f"report_column_{library_name}"):
                    save_to_dynamodb(results, library_name, input_text)
