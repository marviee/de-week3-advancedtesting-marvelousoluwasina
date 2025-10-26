import os
from order_pipeline.reader import read_json
from order_pipeline.validator import validate_orders
from order_pipeline.transformer import transform_orders
from order_pipeline.analyzer import analyze_orders
from order_pipeline.exporter import export_to_json


def run_pipeline(input_path, output_dir="output"):
    """
    Runs the complete data pipeline for ShopLink.
    Returns a summary dictionary of results.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Step 1: Read raw data
    raw_data = read_json(input_path)
    print(f"Loaded {len(raw_data)} records from {input_path}")

    # Step 2: Validate data
    valid_data = validate_orders(raw_data)
    print(f"{len(valid_data)} valid records after validation")

    # Step 3: Transform data
    transformed_data = transform_orders(valid_data)
    print(f"Transformed {len(transformed_data)} records successfully")

    # Step 4: Analyze
    analytics = analyze_orders(transformed_data)
    print("Analysis complete:", analytics)

    # Step 5: Export results
    os.makedirs(output_dir, exist_ok=True)
    cleaned_path = os.path.join(output_dir, "shoplink_cleaned.json")
    analysis_path = os.path.join(output_dir, "shoplink_analysis.json")

    export_to_json(transformed_data, cleaned_path)
    export_to_json(analytics, analysis_path)
    print ("Export completed successfully")

    return {
        "raw_count": len(raw_data),
        "valid_count": len(valid_data),
        "transformed_count": len(transformed_data),
        "analytics": analytics,
        "cleaned_file": cleaned_path,
        "analysis_file": analysis_path,
    }


if __name__ == "__main__":
    # Run manually
    result = run_pipeline("shoplink.json")
    print("Pipeline summary:", result)




