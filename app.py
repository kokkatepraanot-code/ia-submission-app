import streamlit as st
import os
import shutil
from pathlib import Path
import zipfile

# === Streamlit UI ===
st.set_page_config(page_title="IA Submission Portal", layout="centered")
st.title("📄 IB DP Computer Science IA Submission Portal")
st.caption("Created by Praanot Kokkate")

st.markdown("---")
st.markdown("Upload your IA files and automatically generate the correct folder structure for submission.")

# --- Candidate Info Group ---
c1, c2 = st.columns(2)
with c1:
    candidate_suffix = st.text_input("Enter your candidate number (e.g. krn1234):", value="krn1234")
with c2:
    word_count = st.number_input("Enter total word count:", min_value=0, step=1)

candidate_number = f"000091_{candidate_suffix}" if candidate_suffix else ""
candidate_folder_name = f"{candidate_number}" if candidate_number else ""

if candidate_suffix:
    st.markdown(f"**📁 Your folder will be named:** `{candidate_folder_name}`")

# --- Solution Title and Instructions ---
st.markdown("---")
solution_title = st.text_input("📌 Title of your solution:")
instructions = st.text_area("📝 Instructions for using the product:", value="Please check the Product folder to access all the code and database files.")

# --- File Uploads ---
st.markdown("---")
st.subheader("📂 Upload Files")
st.markdown("#### 🔧 Code Files")
code_files = st.file_uploader("Upload code files", accept_multiple_files=True)

st.markdown("#### 🗃️ Database Files")
db_files = st.file_uploader("Upload database files", accept_multiple_files=True, key="db")

st.markdown("#### 📑 Documentation PDFs")
doc_files = st.file_uploader("Upload PDFs (A, B, C, E, Appendix, Record of Tasks)", type="pdf", accept_multiple_files=True)

st.markdown("#### 🎥 Product Video (Criterion D)")
video = st.file_uploader("Upload video file (e.g. MP4)", type=["mp4"])

# --- Required filenames map ---
required_docs = {
    "planning": "Crit_A_Planning.pdf",
    "design": "Crit_B_Design.pdf",
    "record": "Crit_B_Record_of_Tasks.pdf",
    "development": "Crit_C_Development.pdf",
    "evaluation": "Crit_E_Evaluation.pdf",
    "appendix": "Appendix.pdf"
}

# --- Validation ---
if len(doc_files) < 6 or not video or not code_files or not db_files:
    st.warning("🚨 Please upload all 6 required documents, the video, code files, and database files.")
elif candidate_suffix == "krn1234":
    st.error("⚠️ Please change the default candidate number to your own.")
elif not solution_title.strip():
    st.error("⚠️ Please enter the title of your solution.")
elif word_count <= 0:
    st.error("⚠️ Please enter a valid total word count.")
elif st.button("📁 Create IA Folder Structure"):
    base_path = Path(f"{candidate_folder_name}_candidate")
    doc_path = base_path / "Documentation"
    prod_path = base_path / "Product"
    doc_path.mkdir(parents=True, exist_ok=True)
    prod_path.mkdir(parents=True, exist_ok=True)

    code_success, db_success, doc_success = [], [], []

    for i, file in enumerate(code_files):
        st.progress((i + 1) / len(code_files), text=f"Saving code file {file.name}")
        with open(prod_path / file.name, "wb") as f:
            f.write(file.read())
        code_success.append(file.name)
    st.success(f"✅ Code files saved: {', '.join(code_success)}")

    for i, file in enumerate(db_files):
        st.progress((i + 1) / len(db_files), text=f"Saving database file {file.name}")
        with open(prod_path / file.name, "wb") as f:
            f.write(file.read())
        db_success.append(file.name)
    st.success(f"✅ Database files saved: {', '.join(db_success)}")

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
    st.success(f"✅ Documentation saved: {', '.join(doc_success)}")

    if video:
        with open(doc_path / "Crit_D_Video.mp4", "wb") as f:
            f.write(video.read())
        st.success(f"🎥 Video uploaded: {video.name}")

    html_content = f"""
    <html><head><title>Cover Page</title><style>
    body {{ font-family: Arial; padding: 20px; }}
h2 {{ color: #004466; text-align: center; }}
    </style></head><body>
    <h2>IB DP CS IA Cover Page</h2>
    <p><b>Candidate number:</b> {candidate_number}</p>
    <p><b>Solution title:</b> {solution_title}</p>
    <h3>Product</h3>
    <ul><li><b>Instructions:</b> {instructions}</li></ul>
    <h3>Documentation</h3>
    <ul>
        <li>Planning: Crit_A_Planning.pdf</li>
        <li>Design: Crit_B_Design.pdf</li>
        <li>Record of Tasks: Crit_B_Record_of_Tasks.pdf</li>
        <li>Development: Crit_C_Development.pdf</li>
        <li>Video: Crit_D_Video.mp4</li>
        <li>Evaluation: Crit_E_Evaluation.pdf</li>
        <li>Appendix: Appendix.pdf</li>
        <li>Word Count: {word_count}</li>
    </ul></body></html>
    """
    with open(base_path / "cover_page.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    zip_filename = f"{candidate_number}.zip"
    shutil.make_archive(base_path, 'zip', base_path)

    st.success(f"📦 Folder structure created and zipped for candidate {candidate_folder_name}.")
    with open(f"{base_path}.zip", "rb") as zip_file:
        st.download_button(label="⬇️ Download Zip File", data=zip_file, file_name=zip_filename, mime="application/zip")
