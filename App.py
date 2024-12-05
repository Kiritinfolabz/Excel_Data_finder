import streamlit as st
import pandas as pd


# Function to search for data
def search_data(search_value, sheets):
    results = {}
    for sheet_name, df in sheets.items():
        matches = df[
            df.apply(lambda row: row.astype(str).str.contains(search_value, case=False, na=False).any(), axis=1)
        ]
        if not matches.empty:
            results[sheet_name] = matches
    return results


# Main function for Streamlit UI
def main():
    st.title("Excel/CSV Data Search and Viewer Application")
    st.markdown("### Upload your Excel or CSV file to view data or search for specific entries.")

    # File upload
    uploaded_file = st.file_uploader("Upload a file (Excel or CSV)", type=["xlsx", "xls", "csv"])

    if uploaded_file:
        # File processing
        file_extension = uploaded_file.name.split(".")[-1].lower()

        try:
            if file_extension in ["xlsx", "xls"]:
                sheets = pd.read_excel(uploaded_file, sheet_name=None)  # Load all sheets
            elif file_extension == "csv":
                df = pd.read_csv(uploaded_file)  # Load CSV as a single sheet
                sheets = {"Sheet1": df}  # Treat CSV as a single sheet named "Sheet1"
            else:
                st.error("Unsupported file format!")
                return

            # Display sheet names
            st.sidebar.markdown("### Available Sheets")
            for sheet_name in sheets.keys():
                st.sidebar.write(f"- {sheet_name}")

            # Option selection
            st.sidebar.markdown("### Options")
            choice = st.sidebar.radio(
                "What would you like to do?",
                ["View Data", "Search Data", "Exit"]
            )

            if choice == "View Data":
                st.markdown("### View All Data")
                for sheet_name, df in sheets.items():
                    st.markdown(f"#### Data from sheet: {sheet_name}")
                    st.dataframe(df)  # Display data in an interactive table

            elif choice in ["Search Data", "Numerical Data"]:
                search_value = st.text_input(
                    f"Enter the {'Search' if choice == 'Search Data' else 'numerical'} value to search:"
                )

                if search_value:
                    results = search_data(search_value, sheets)

                    if results:
                        for sheet_name, matches in results.items():
                            st.markdown(f"### Matches found in sheet: {sheet_name}")
                            st.dataframe(matches)
                    else:
                        st.warning(f"No matches found for '{search_value}' in any sheet.")

            elif choice == "Exit":
                st.info("You selected Exit. Close the app or upload another file to start over.")

        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
