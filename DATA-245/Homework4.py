"""
Azure ML SDK v2 tutorial-style script:
- Download CSV data to local folder
- Connect to Azure ML workspace (MLClient)
- Create a Data Asset (v1 = "initial") from a local CSV file
- Read data locally for EDA (avoids azureml:// auth issues with pandas/fsspec)
- Clean data + write Parquet locally
- Create a new Data Asset version (v2 = "cleanedYYYY.MM.DD.HHMMSS")
- Compare local raw vs local cleaned

Prereqs:
  python -m pip install -U azure-ai-ml azure-identity pandas pyarrow python-dotenv
"""

from __future__ import annotations

import os
import time
import subprocess
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from azure.ai.ml import MLClient
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# -----------------------------
# 0) Config from .env
# -----------------------------
load_dotenv()

SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP")
WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")

ASSET_NAME = os.getenv("ASSET_NAME", "credit-card")
V1 = os.getenv("V1", "initial")

DATA_DIR = Path("./data")
CSV_NAME = "default_of_credit_card_clients.csv"
CSV_URL = "https://azuremlexamples.blob.core.windows.net/datasets/credit_card/default_of_credit_card_clients.csv"

# Put this in .env if you want:
# AZURE_TENANT_ID=717a069d-61e1-44ba-8741-4e430517b89e
TENANT_ID = os.getenv("AZURE_TENANT_ID", "717a069d-61e1-44ba-8741-4e430517b89e")


def require_env(var_name: str, value: str | None) -> str:
    if not value:
        raise ValueError(f"Missing environment variable: {var_name}. Check your .env file.")
    return value


SUBSCRIPTION_ID = require_env("SUBSCRIPTION_ID", SUBSCRIPTION_ID)
RESOURCE_GROUP = require_env("RESOURCE_GROUP", RESOURCE_GROUP)
WORKSPACE_NAME = require_env("WORKSPACE_NAME", WORKSPACE_NAME)


# -----------------------------
# Helpers
# -----------------------------
def ensure_data_downloaded(data_dir: Path, csv_url: str, csv_name: str) -> Path:
    """Download the CSV into ./data if missing."""
    data_dir.mkdir(parents=True, exist_ok=True)
    csv_path = data_dir / csv_name

    if csv_path.exists() and csv_path.stat().st_size > 0:
        print(f"✅ Data already present at: {csv_path}")
        return csv_path

    print(f"⬇️ Downloading dataset to: {csv_path}")

    try:
        subprocess.run(["wget", "-O", str(csv_path), csv_url], check=True)
    except Exception:
        import urllib.request
        urllib.request.urlretrieve(csv_url, str(csv_path))

    print(f"✅ Download complete: {csv_path} ({csv_path.stat().st_size} bytes)")
    return csv_path


def get_ml_client() -> MLClient:
    """
    Create MLClient.
    - Try DefaultAzureCredential first
    - Fall back to InteractiveBrowserCredential pinned to the correct tenant
    """
    try:
        cred = DefaultAzureCredential(exclude_interactive_browser_credential=True)
        cred.get_token("https://management.azure.com/.default")
        print("🔐 Using DefaultAzureCredential.")
    except Exception:
        cred = InteractiveBrowserCredential(tenant_id=TENANT_ID)
        print(f"🔐 Using InteractiveBrowserCredential (tenant {TENANT_ID}).")

    return MLClient(
        credential=cred,
        subscription_id=SUBSCRIPTION_ID,
        resource_group_name=RESOURCE_GROUP,
        workspace_name=WORKSPACE_NAME,
    )


def create_data_asset_if_missing(
    ml_client: MLClient,
    name: str,
    version: str,
    description: str,
    path: str,
    asset_type=AssetTypes.URI_FILE,
    tags: dict | None = None,
) -> Data:
    """Create data asset if it doesn't exist; otherwise fetch it."""
    tags = tags or {}

    try:
        existing = ml_client.data.get(name=name, version=version)
        # Print actual name/version from the returned asset
        print(f"✅ Data asset already exists: {existing.name}:{existing.version}")
        return existing
    except Exception:
        pass

    asset = Data(
        name=name,
        version=version,
        description=description,
        path=path,
        type=asset_type,
        tags=tags,
    )
    created = ml_client.data.create_or_update(asset)
    print(f"✅ Data asset created: {created.name}:{created.version}")
    return created


# -----------------------------
# Main
# -----------------------------
def main() -> None:
    # 1) Download CSV
    csv_path = ensure_data_downloaded(DATA_DIR, CSV_URL, CSV_NAME)

    # 2) Connect to workspace
    ml_client = get_ml_client()
    print("✅ MLClient created (connects lazily on first call).")

    # 3) Upload CSV as Data Asset v1
    asset_v1 = create_data_asset_if_missing(
        ml_client=ml_client,
        name=ASSET_NAME,
        version=V1,
        description="Credit card data (raw CSV)",
        path=str(csv_path),
        asset_type=AssetTypes.URI_FILE,
    )

    # 4) Load locally into pandas (IMPORTANT: avoid pd.read_csv(asset_v1.path))
    print(f"V1 Data asset URI (cloud): {asset_v1.path}")
    print(f"Local CSV path: {csv_path}")

    df_v1_default = pd.read_csv(csv_path)
    print("\nV1 preview (read locally):")
    print(df_v1_default.head())

    # 5) Clean + write Parquet locally
    df_clean = pd.read_csv(csv_path, header=1)
    df_clean.rename(columns={"default payment next month": "default"}, inplace=True)
    if "ID" in df_clean.columns:
        df_clean.drop("ID", axis=1, inplace=True)

    parquet_path = DATA_DIR / "cleaned-credit-card.parquet"
    df_clean.to_parquet(parquet_path, index=False)
    print(f"\n✅ Cleaned data written to Parquet: {parquet_path}")
    print(df_clean.head())

    # 6) Create v2 data asset (Parquet)
    v2 = "cleaned" + time.strftime("%Y.%m.%d.%H%M%S", time.gmtime())
    asset_v2 = create_data_asset_if_missing(
        ml_client=ml_client,
        name=ASSET_NAME,
        version=v2,
        description="Default of credit card clients data (cleaned Parquet).",
        path=str(parquet_path),
        asset_type=AssetTypes.URI_FILE,
        tags={"training_data": "true", "format": "parquet"},
    )

    # 7) Compare locally (reliable)
    print("\n" + "_" * 110)
    print("LOCAL raw (CSV) head:")
    print(pd.read_csv(csv_path).head(5))

    print("\n" + "_" * 110)
    print("LOCAL cleaned (Parquet) head:")
    print(pd.read_parquet(parquet_path).head(5))

    print("\n✅ Done. You now have two data-asset versions in Azure ML:")
    print(f" - {ASSET_NAME}:{V1} (raw CSV)")
    print(f" - {ASSET_NAME}:{v2} (cleaned Parquet)")
    print("\n(And you successfully performed EDA/cleaning locally.)")


if __name__ == "__main__":
    main()