import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="File Merger Agent", page_icon="📊", layout="centered")

st.title("📊 Google Sheets File Merger")
st.write("Upload three downloaded files (CSV or Excel) with identical headers to merge them into a single dataset.")

# File upload widgets
col1, col2, col3 = st.columns(3)

with col1:
    file1 = st.file_uploader("Upload First File", type=["csv", "xlsx"])

with col2:
    file2 = st.file_uploader("Upload Second File", type=["csv", "xlsx"])

with col3:
    file3 = st.file_uploader("Upload Third File", type=["csv", "xlsx"])


def load_data(file):
    """Read CSV or Excel into a DataFrame."""
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)


if file1 and file2 and file3:
    try:
        df1 = load_data(file1)
        df2 = load_data(file2)
        df3 = load_data(file3)

        # Check headers
        headers = [list(df.columns) for df in [df1, df2, df3]]

        if headers[0] == headers[1] == headers[2]:
            st.success("✅ All headers match successfully!")
        else:
            st.warning(
                "⚠️ Warning: Column headers do not match exactly. "
                "Pandas will align matching columns and fill missing ones with null values."
            )

        # Merge all three files
        combined_df = pd.concat([df1, df2, df3], ignore_index=True)

        # Metrics
        st.subheader("Data Summary")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("File 1 Rows", len(df1))
        m2.metric("File 2 Rows", len(df2))
        m3.metric("File 3 Rows", len(df3))
        m4.metric("Total Rows", len(combined_df))

        # Preview
        st.subheader("Preview of Merged Data")
        st.dataframe(combined_df.head(10))

        # Export options
        export_format = st.radio(
            "Select Output Format:",
            ["CSV", "Excel (.xlsx)"],
            horizontal=True
        )

        if export_format == "CSV":
            data_to_download = combined_df.to_csv(index=False).encode("utf-8")
            file_name = "merged_data.csv"
            mime_type = "text/csv"
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                combined_df.to_excel(writer, index=False)
            data_to_download = buffer.getvalue()
            file_name = "merged_data.xlsx"
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        st.download_button(
            label=f"📥 Download {file_name}",
            data=data_to_download,
            file_name=file_name,
            mime=mime_type,
            type="primary"
        )

    except Exception as e:
        st.error(f"An error occurred while processing the files: {e}")
