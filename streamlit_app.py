import streamlit as st
import pandas as pd

# --- Title ---
st.title("Marketing Tactic Classifier")

# --- Upload CSV ---
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # --- Display preview ---
    st.subheader("Dataset Preview")
    st.write(df.head())

    # --- Dictionary input ---
    st.sidebar.header("Modify Dictionaries")

    def parse_keywords(input_text):
        return set([kw.strip().lower() for kw in input_text.split(",") if kw.strip()])

    default_urgency = "limited, limited time, order now, hurry, last chance, today only"
    default_exclusive = "exclusive, vip, members only, early access, private sale"

    urgency_input = st.sidebar.text_area(
        "Urgency Marketing Keywords (comma-separated)", value=default_urgency
    )
    exclusive_input = st.sidebar.text_area(
        "Exclusive Marketing Keywords (comma-separated)", value=default_exclusive
    )

    dictionaries = {
        'urgency_marketing': parse_keywords(urgency_input),
        'exclusive_marketing': parse_keywords(exclusive_input)
    }

    # --- Lowercase text for matching ---
    if 'Statement' not in df.columns:
        st.error("The uploaded file must have a 'Statement' column.")
    else:
        df['statement_lower'] = df['Statement'].str.lower()

        # --- Apply keyword tagging ---
        for category, keywords in dictionaries.items():
            df[category] = df['statement_lower'].apply(
                lambda text: int(any(kw in text for kw in keywords))
            )

        df.drop(columns=['statement_lower'], inplace=True)

        # --- Show result ---
        st.subheader("Classified Data")
        st.write(df.head())

        # --- Download result ---
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Processed CSV", csv, "classified_data.csv", "text/csv")
