import pandas as pd
from pathlib import Path
RAW = Path(r"C:\Users\AMISHA KAVDIA\khoj\data\raw\esci-data\shopping_queries_dataset")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

examples = pd.read_parquet(RAW / "shopping_queries_dataset_examples.parquet")
products = pd.read_parquet(RAW / "shopping_queries_dataset_products.parquet")

# the smaller, fully-judged subset, English only
subset = examples[
    (examples["small_version"] == 1) & (examples["product_locale"] == "us")
].copy()

# # attach product details to each judgement
df = subset.merge(
    products,
    on=["product_id", "product_locale"],
    how="left",
    validate="many_to_one",
)

print("judgements:", len(df))
print("unique queries:", df["query"].nunique())
print("unique products:", df["product_id"].nunique())
print("missing titles:", df["product_title"].isna().sum())

df.to_parquet(OUT / "judgements.parquet", index=False)
print("File created successfully")