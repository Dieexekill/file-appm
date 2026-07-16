import streamlit as st
import pandas as pd

st.set_page_config(page_title="File Merger Agent", page_icon="📊", layout="centered")

st.title("📊 Google Sheets File Merger")
st.write("Upload two downloaded files (CSV or Excel) with identical headers to merge them into a single dataset.")

# File upload widgets
col1, col2 = st.columns(2)

with col1:
    file1 = st.file_uploader("Upload First File", type=["csv", "xlsx"])

with col2:
    file2 = st.file_uploader("Upload Second File", type=["csv", "xlsx"])

def load_data(file):
    """Utility function to read CSV or Excel files into a DataFrame."""
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if file1 and file2:
    try:
        df1 = load_data(file1)
        df2 = load_data(file2)

        # Check if column headers match
        if list(df1.columns) != list(df2.columns):
            st.warning("⚠️ Warning: Column headers do not match exactly. Pandas will align columns with matching names, but missing columns will have null values.")
        else:
            st.success("✅ Headers match successfully!")

        # Combine DataFrames
        combined_df = pd.concat([df1, df2], ignore_index=True)

        st.subheader("Data Summary")
        m1, m2, m3 = st.columns(3)
        m1.metric("File 1 Rows", len(df1))
        m2.metric("File 2 Rows", len(df2))
        m3.metric("Total Merged Rows", len(combined_df))

        # Data preview
        st.subheader("Preview of Merged Data")
        st.dataframe(combined_df.head(10))

        # Output format options
        export_format = st.radio("Select Output Format:", ["CSV", "Excel (.xlsx)"], horizontal=True)

        if export_format == "CSV":
            data_to_download = combined_df.to_csv(index=False).encode("utf-8")
            file_name = "merged_data.csv"
            mime_type = "text/csv"
        else:
            import io
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                combined_df.to_excel(writer, index=False)
            data_to_download = buffer.getvalue()
            file_name = "merged_data.xlsx"
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        # Download button
        st.download_button(
            label=f"📥 Download {file_name}",
            data=data_to_download,
            file_name=file_name,
            mime=mime_type,
            type="primary"
        )

    except Exception as e:
        st.error(f"An error occurred while processing the files: {e}")
