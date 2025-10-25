ShopLink Order Pipeline — Week 3 Advanced Testing

This project is part of my Data Engineering Week 3 assignment — focused on building and testing a data pipeline for ShopLink, an online marketplace.
The goal is to make sure every stage of the pipeline works perfectly and can handle messy data without breaking.


What This Project Does

The pipeline:

Reads order data from JSON.

Validates each record (no missing or invalid fields).

Transforms messy values — like “N2500”, “45 dollars”, or “Paid” — into clean numeric and text formats.

Analyzes results (total revenue, average revenue, and payment status counts).

Exports the cleaned data into a new JSON file.


Testing

All parts of the pipeline are tested using Pytest:

The reader raises errors for empty or unsupported files.

The validator skips bad rows (like negative or missing quantities).

The transformer handles tricky formats with Regex.

The analyzer produces correct totals.

The exporter writes results successfully.

There’s also a full integration test that runs the whole pipeline end-to-end.
Each stage has at least 60% test coverage.


 How To Run
# clone the repo
git clone https://github.com/marviee/de-week3-advancedtesting-marvelousoluwasina.git
cd de-week3-advancedtesting-marvelousoluwasina

# setup environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# run tests
pytest -v

# run the pipeline manually
python -m order_pipeline.pipeline data/shoplink.json data/shoplink_cleaned.json

 Folder Overview
order_pipeline/     main pipeline modules
tests/              all pytest files
data/               raw and cleaned JSON data
README.md           project overview
requirements.txt    dependencies
.gitignore


👨🏽‍💻 Author

Marvelous Oluwasina
GitHub: @marviee