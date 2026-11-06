# scripts/02_make_catalogue.py
import pandas as pd
from pathlib import Path
import numpy as np


OUT = Path("data/processed")
df = pd.read_parquet(OUT / "judgements.parquet")

# 8,000 queries, chosen reproducibly
queries = (
    df[["query_id", "query"]]
    .drop_duplicates()
    .sample(n=8000, random_state=42)
)

sub = df[df["query_id"].isin(queries["query_id"])].copy()

catalogue = (
    sub[[
        "product_id", "product_title", "product_description",
        "product_bullet_point", "product_brand", "product_color",
    ]]
    .drop_duplicates(subset=["product_id"])
    .reset_index(drop=True)
)

rng = np.random.default_rng(42)
catalogue["price_inr"] = np.round(
    rng.lognormal(mean=6.5, sigma=1.1, size=len(catalogue))
).astype(int).clip(99, 200000)
catalogue["rating"] = np.round(rng.normal(4.0, 0.6, len(catalogue)), 1).clip(1.0, 5.0)
catalogue["num_reviews"] = rng.integers(0, 5000, len(catalogue))

print("queries:", len(queries))
print("products:", len(catalogue))
print("judgements:", len(sub))

queries.to_parquet(OUT / "queries_en.parquet", index=False)
catalogue.to_parquet(OUT / "catalogue.parquet", index=False)
sub.to_parquet(OUT / "judgements_subset.parquet", index=False)