import streamlit as st
import re
from difflib import unified_diff

def convert_rmd_to_qmd(rmd_content):
    """
    Converts RMD content to QMD format by updating syntax for references to sections,
    tables, and figures.
    """
    # Convert section references (\@ref(idOfReference) -> @sec-idOfReference)
    qmd_content = re.sub(r"\\@ref\(([^:]*?)\)", r"@sec-\1", rmd_content)

    # Convert figure references (\@ref(fig:idOfReference) -> @fig-idOfReference)
    qmd_content = re.sub(r"\\@ref\(fig:(.*?)\)", r"@fig-\1", qmd_content)

    # Convert table references (\@ref(tab:idOfReference) -> @tab-idOfReference)
    qmd_content = re.sub(r"\\@ref\(tab:(.*?)\)", r"@tab-\1", qmd_content)

    # Replace R Markdown YAML blocks (if any) with Quarto YAML format
    # Placeholder: Add logic here for more complex YAML conversion if needed

    return qmd_content

def generate_diff(original, converted):
    """
    Generate a unified diff highlighting the differences between the original and converted content.
    """
    original_lines = original.splitlines(keepends=True)
    converted_lines = converted.splitlines(keepends=True)
    diff = unified_diff(original_lines, converted_lines, lineterm="")
    return "".join(diff)

# Set Streamlit app configuration
st.set_page_config(page_icon = "👾", page_title="RMD to QMD Converter", layout="wide")

# App title
st.title("👾 RMD to QMD Converter")
st.write("&nbsp;")

# File uploader for RMD files
uploaded_file = st.file_uploader("Upload your RMD file")

if uploaded_file is not None:
    # Extract the uploaded file name without extension
    input_filename = uploaded_file.name
    output_filename = input_filename.replace(".Rmd", ".qmd")

    # Read and decode uploaded file
    rmd_content = uploaded_file.read().decode("utf-8")

    # Convert RMD content to QMD
    qmd_content = convert_rmd_to_qmd(rmd_content)

    # Generate differences for highlighting
    diff_content = generate_diff(rmd_content, qmd_content)

    # Provide a download button for the converted QMD file
    st.download_button(
        label="Download QMD file",
        data=qmd_content,
        file_name=output_filename,
        mime="text/markdown"
    )

    # Display the content in three columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("RMD File Content")
        st.code(rmd_content, language="markdown", wrap_lines=True)

    with col2:
        st.header("QMD File Content")
        st.code(qmd_content, language="markdown", wrap_lines=True)

    with col3:
        st.header("Highlighted Differences")
        st.code(diff_content, language="diff", wrap_lines=True)

else:
    # Inform the user to upload a file if none is provided
    st.info("Please upload your RMD file to begin the conversion.")
