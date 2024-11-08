import json
import base64
from typing import Dict, Any
from algosdk import transaction, mnemonic
from algosdk.v2client import algod

# Algod client setup
algod_address = "http://localhost:4001"
algod_token = "a" * 64
algod_client = algod.AlgodClient(algod_token, algod_address)

# Account details
account_address = "OI26U2QOXU4DUPVATTSVW52DRCLWRIIBB6OLNUSJOIIXP7TGADIVHTW6TI"  # Replace with your actual address
passphrase = "century feature infant demand curious inform stadium tonight squeeze pumpkin sample abuse viable confirm rally young simple time announce decade amazing brief indoor able solid"  # Replace with your mnemonic
private_key = mnemonic.to_private_key(passphrase)

# Asset ID of the DNFT - update this with your actual asset ID
asset_id = 1133

# Updated metadata for the NFT in ARC69 format
updated_metadata = {
    "standard": "arc69",
    "name": "My Dynamic NFT",
    "description": "Leveling up to Level 2",
    "image": "ipfs://Qm...newhash",
    "properties": {
        "level": 2,
        "experience": 100
    }
}

# Encode metadata as JSON in Note field
note_field = json.dumps(updated_metadata).encode()

# Create a transaction to update asset metadata
params = algod_client.suggested_params()
txn = transaction.AssetConfigTxn(
    sender=account_address,
    sp=params,
    index=asset_id,  # Use asset_id directly here
    note=note_field,
    strict_empty_address_check=False
)

# Sign and send the transaction
signed_txn = txn.sign(private_key)
txid = algod_client.send_transaction(signed_txn)
print(f"Transaction ID: {txid}")

# Wait for transaction confirmation
try:
    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Metadata update confirmed in round: {results['confirmed-round']}")
except Exception as e:
    print(f"Error during transaction confirmation: {e}")

# Fetch asset information after update
try:
    asset_info = algod_client.asset_info(asset_id)
    asset_params: Dict[str, Any] = asset_info["params"]
    print(f"Asset Name: {asset_params.get('name')}")
    print(f"Asset URL: {asset_params.get('url')}")
    print("Asset Properties:", json.dumps(asset_params, indent=4))
except Exception as e:
    print(f"Error fetching asset information: {e}")
