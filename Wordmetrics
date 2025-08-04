import ipywidgets as widgets
from IPython.display import display, clear_output, FileLink
import pandas as pd
import io

# Cell 2: Default dictionary
default_dictionary = {
    "urgency_marketing": {"hurry", "now", "limited", "last chance", "act fast", "soon"},
    "luxury_marketing": {"exclusive", "premium", "luxury", "designer", "high-end"},
    "discount_marketing": {"sale", "free", "discount", "save", "off", "deal"},
}

# Cell 3: File upload widget
upload = widgets.FileUpload(accept=".csv,.xlsx", multiple=False)
display(widgets.HTML(value="<h3>1. Upload your CSV or XLSX file</h3>"))
display(upload)

# Placeholders
df = None
text_column_dropdown = None
dictionary_input = None
output_area = widgets.Output()

def on_upload_change(change):
    global df, text_column_dropdown
    if upload.value:
        file_info = list(upload.value.values())[0]
        filename = file_info['metadata']['name']
        content = file_info['content']
        try:
            if filename.endswith(".csv"):
                df = pd.read_csv(io.BytesIO(content))
            elif filename.endswith(".xlsx"):
                df = pd.read_excel(io.BytesIO(content))
            else:
                print("Unsupported file type. Please upload .csv or .xlsx only.")
                return
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        text_column_dropdown = widgets.Dropdown(
            options=df.columns.tolist(),
            description="Text Column:"
        )
        display(widgets.HTML(value="<h3>2. Select the text column</h3>"))
        display(text_column_dropdown)
        display(dictionary_ui())

upload.observe(on_upload_change, names='value')

# Cell 4: Dictionary and run UI
def dictionary_ui():
    global dictionary_input
    dictionary_input = widgets.Textarea(
        value=str(default_dictionary),
        placeholder="Enter your dictionary here...",
        description="Dictionary:",
        layout=widgets.Layout(width='100%', height='150px')
    )
    run_button = widgets.Button(description="Run Analysis", button_style='success')
    run_button.on_click(run_analysis)
    return widgets.VBox([
        widgets.HTML(value="<h3>3. Edit Dictionary (optional)</h3>"),
        dictionary_input,
        run_button,
        widgets.HTML(value="<h3>4. Output</h3>"),
        output_area
    ])

# Cell 5: Run analysis function
def run_analysis(b):
    with output_area:
        clear_output()
        if df is None or text_column_dropdown is None:
            print("Missing data or column selection.")
            return

        text_column = text_column_dropdown.value
        try:
            user_dict = eval(dictionary_input.value)
            assert isinstance(user_dict, dict)
        except Exception as e:
            print("Invalid dictionary format:", e)
            return

        # Initialize results
        category_matches = {cat: [] for cat in user_dict}
        keyword_hits = []

        for i, row in df.iterrows():
            text = str(row[text_column]).lower()
            row_hits = {cat: [] for cat in user_dict}
            for category, keywords in user_dict.items():
                matched = [kw for kw in keywords if kw.lower() in text]
                if matched:
                    category_matches[category].append(i)
                    row_hits[category] = matched
            keyword_hits.append(row_hits)

        # Summary Table
        summary = {cat: len(indices) for cat, indices in category_matches.items()}
        print("Category Frequency Summary:\n")
        display(pd.DataFrame(summary.items(), columns=["Category", "Match Count"]))

        # Add results to dataframe
        for cat in user_dict:
            df[f"{cat}_match"] = df.index.isin(category_matches[cat])
            df[f"{cat}_keywords"] = [kw[cat] for kw in keyword_hits]

        # Show preview
        display(widgets.HTML(value="<h4>5 Sample Results</h4>"))
        display(df[[text_column] + [f"{cat}_match" for cat in user_dict]].head())

        # Download button
        create_download_button(df)

# Cell 6: Save and offer download link
def create_download_button(df):
    out_path = "/content/classified_results.csv"
    df.to_csv(out_path, index=False)
    display(widgets.HTML(value="<h3>6. Download Results</h3>"))
    display(FileLink(out_path, result_html_prefix="Click to download: "))
