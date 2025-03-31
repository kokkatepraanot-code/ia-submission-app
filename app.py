import streamlit as st
import os
import shutil
from pathlib import Path
import zipfile

# === Streamlit UI ===
st.title("IB DP Computer Science IA Submission")
st.markdown("Upload your IA documents below. This will create the correct folder structure automatically.")

# --- Candidate number input ---
candidate_suffix = st.text_input("Enter your candidate number (e.g. krn1234):", value="krn1234")
if candidate_suffix:
    st.markdown(f"**Your full candidate folder will be named:** 000091_{candidate_suffix}_candidate")
candidate_number = f"000091_{candidate_suffix}" if candidate_suffix else ""
folder_prefix = "000091_"
candidate_folder_name = f"{candidate_number}" if candidate_number else ""

# --- Info collection ---
solution_title = st.text_input("Enter the title of your solution:")
instructions = st.text_area("Enter instructions for using the product:", value="Please check the Product folder to access all the code and database files.")
word_count = st.number_input("Enter total word count:", min_value=0, step=1)

# --- File uploads ---

# Upload code files (any type)
st.markdown("### Upload your code files (drag and drop supported)")
code_files = st.file_uploader("Upload code files", accept_multiple_files=True)

# Upload database files (any type)
st.markdown("### Upload your database files")
db_files = st.file_uploader("Upload database files", accept_multiple_files=True, key="db")

st.markdown("### Upload your documentation PDFs (Criteria A, B, C, E, Appendix, Record of Tasks)")
doc_files = st.file_uploader("Upload PDF files (A, B, C, E, Appendix, Record of Tasks)", type="pdf", accept_multiple_files=True)

st.markdown("### Upload your product video (Criterion D)")
video = st.file_uploader("Upload video file (e.g. MP4)", type=["mp4"])

# --- Mapping of uploaded docs to required filenames ---
required_docs = {
    "planning": "Crit_A_Planning.pdf",
    "design": "Crit_B_Design.pdf",
    "record": "Crit_B_Record_of_Tasks.pdf",
    "development": "Crit_C_Development.pdf",
    "evaluation": "Crit_E_Evaluation.pdf",
    "appendix": "Appendix.pdf"
}

if len(doc_files) < 6 or not video or not code_files or not db_files:
    st.warning("Please upload all 6 required documents, the video, code files, and database files before proceeding.")
elif candidate_suffix == "krn1234":
    st.error("Please change the default candidate number to your own before continuing.")
elif not solution_title.strip():
    st.error("Please enter the title of your solution before continuing.")
elif word_count <= 0:
    st.error("Please enter a valid total word count before continuing.")
elif st.button("Create IA Folder Structure"):
    if not candidate_folder_name:
        st.error("Please enter your candidate number.")
    else:
        base_path = Path(f"{candidate_folder_name}_candidate")
        doc_path = base_path / "Documentation"
        prod_path = base_path / "Product"

        # Create folder structure
        doc_path.mkdir(parents=True, exist_ok=True)
        prod_path.mkdir(parents=True, exist_ok=True)

        # Save code files with progress
        code_success = []
        for i, file in enumerate(code_files):
            st.progress((i + 1) / len(code_files), text=f"Saving code file {file.name}")
            with open(prod_path / file.name, "wb") as f:
                f.write(file.read())
            code_success.append(file.name)
        st.success(f"Uploaded code files: {', '.join(code_success)}")

        # Save database files with progress
        db_success = []
        for i, file in enumerate(db_files):
            st.progress((i + 1) / len(db_files), text=f"Saving database file {file.name}")
            with open(prod_path / file.name, "wb") as f:
                f.write(file.read())
            db_success.append(file.name)
        st.success(f"Uploaded database files: {', '.join(db_success)}")

        # Save and rename uploaded documentation
        doc_success = []
        for file in doc_files:
            matched = False
            for key, filename in required_docs.items():
                if key in file.name.lower().replace("_", "").replace(" ", ""):
                    with open(doc_path / filename, "wb") as f:
                        f.write(file.read())
                    doc_success.append(filename)
                    matched = True
                    break
            if not matched:
                with open(doc_path / file.name, "wb") as f:
                    f.write(file.read())
                doc_success.append(file.name)
        st.success(f"Uploaded documentation files: {', '.join(doc_success)}")

        # Save video
        if video:
            with open(doc_path / "Crit_D_Video.mp4", "wb") as f:
                f.write(video.read())
            st.success(f"Uploaded video: {video.name}")

        # Generate HTML cover page (saved in base folder)
        html_content = f"""
        <html>
        <head>
        <title>IB DP CS IA Packaging</title>
        <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9; }}
        h2 {{ text-align: center; color: #2c3e50; }}
        ul {{ line-height: 1.8; }}
        li b {{ color: #34495e; }}
        a {{ color: #2980b9; text-decoration: none; }}
        .section-title {{ color: #2c3e50; margin-top: 30px; }}
        </style>
        </head>
        <body>
        <h2>IB DP Computer Science Solution (IA) Cover Page</h2>
        <p><b>Candidate number:</b> {candidate_number}</p>
        <p><b>Solution title:</b> {solution_title}</p>

        <h3 class='section-title'>Product</h3>
        <ul>
            <li><b>Product files:</b> <a href='Product'>Product folder</a></li>
            <li><b>Product instructions:</b> {instructions}</li>
        </ul>

        <h3 class='section-title'>Documentation</h3>
        <p>Links to documentation:</p>
        <ul>
            <li><b>Planning:</b> <a href='Documentation/Crit_A_Planning.pdf'>Crit_A_Planning.pdf</a></li>
            <li><b>Design:</b> <a href='Documentation/Crit_B_Design.pdf'>Crit_B_Design.pdf</a></li>
            <li><b>Record of Tasks:</b> <a href='Documentation/Crit_B_Record_of_Tasks.pdf'>Crit_B_Record_of_Tasks.pdf</a></li>
            <li><b>Development:</b> <a href='Documentation/Crit_C_Development.pdf'>Crit_C_Development.pdf</a></li>
            <li><b>Functionality (Video):</b> <a href='Documentation/Crit_D_Video.mp4'>Crit_D_Video.mp4</a></li>
            <li><b>Evaluation:</b> <a href='Documentation/Crit_E_Evaluation.pdf'>Crit_E_Evaluation.pdf</a></li>
            <li><b>Appendix:</b> <a href='Documentation/Appendix.pdf'>Appendix.pdf</a></li>
            <li><b>Word Count:</b> {word_count}</li>
        </ul>
        </body>
        </html>
        """
        with open(base_path / "cover_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        # Zip the entire folder
        zip_filename = f"{candidate_number}.zip"
        shutil.make_archive(base_path, 'zip', base_path)

        st.success(f"Folder structure created and zipped for candidate {candidate_folder_name}.")
        with open(f"{base_path}.zip", "rb") as zip_file:
            st.download_button(label="Download Zip File", data=zip_file, file_name=zip_filename, mime="application/zip")
