import json
import time
import requests
from algosdk import account, transaction, mnemonic
from algosdk.v2client import algod
from typing import Dict, Any

algod_address = "http://localhost:4001"
algod_token = "a" * 64  # Replace with your algod token
account_address = "L3BARDXYUN35W2O2VEKGOPVWFJ6JZZZX2XGJU4CJQVY5UEBDJLN7NVGGZY"  # Replace with your address
passphrase = "robot absent donor define lumber great save have assist sorry consider render test video stone actress leopard pretty agent can dial capital broom abandon echo"
algod_client = algod.AlgodClient(algod_token, algod_address)
# Get private key from mnemonic
private_key = mnemonic.to_private_key(passphrase)

# 1. Create ASA with initial metadata
initial_metadata = {
    "standard": "arc69",
    "name": "My Dynamic NFT",
    "description": "This is a practice DNFT with changeable metadata.",
    "image": "ipfs://Qm...examplehash",
    "properties": {
        "level": 1,
        "experience": 0
    }
}

# Encode metadata as JSON in Note Field
note_field = json.dumps(initial_metadata).encode()

# ASA creation parameters
params = algod_client.suggested_params()
txn = transaction.AssetConfigTxn(
    sender=account_address,
    sp=params,
    total=1,
    default_frozen=False,
    unit_name="DNFT",
    asset_name="DynamicNFT",
    manager=account_address,
    reserve=account_address,
    freeze=account_address,
    clawback=account_address,
    url="https://example.com/metadata",  # Optional: URL for additional metadata
    decimals=0,
    note=note_field  # Add metadata in the Note Field
)

# Sign the transaction
signed_txn = txn.sign(private_key)

# Send the transaction
txid = algod_client.send_transaction(signed_txn)
print(f"Transaction ID of ASA creation: {txid}")

# Wait for transaction confirmation
results = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"Result confirmed in round: {results['confirmed-round']}")

created_asset = results["asset-index"]
print(f"Asset ID created: {created_asset}")

# Fetch asset information after creation
asset_info = algod_client.asset_info(created_asset)
asset_params: Dict[str, Any] = asset_info["params"]
print(f"Asset Name: {asset_params['name']}")
print(f"Asset Params: {list(asset_params.keys())}")


