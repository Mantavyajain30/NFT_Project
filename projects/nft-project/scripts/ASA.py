import json
import time
from algosdk import account, transaction, mnemonic
from algosdk.v2client import algod

# Initialize the client
#algod_address = "http://localhost:4001"
#algod_token = "a" * 64  # 
#creator_address = "OI26U2QOXU4DUPVATTSVW52DRCLWRIIBB6OLNUSJOIIXP7TGADIVHTW6TI"  # Replace with your address
#passphrase = "century feature infant demand curious inform stadium tonight squeeze pumpkin sample abuse viable confirm rally young simple time announce decade amazing brief indoor able solid"  # Replace with your mnemonic




def create_asa_nft(algod_address, algod_token, creator_address, passphrase, asset_name, unit_name, ipfs_url=None):
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Get private key from mnemonic
    private_key = mnemonic.to_private_key(passphrase)

    # Define asset parameters
    total_supply = 1
    decimals = 0

    # Optional: add IPFS URL for metadata
    ipfs_url = "https://green-able-hornet-226.mypinata.cloud/ipfs/QmSHe6DzHo6fxbAdbiUpA2qDedrSckiZLc522yNbAkUKY4"

    # Get suggested transaction parameters
    params = algod_client.suggested_params()

    # Create the asset creation transaction
    txn = transaction.AssetConfigTxn(
        sender=creator_address,
        sp=params,
        total=total_supply,
        default_frozen=False,
        unit_name=unit_name,
        asset_name=asset_name,
        manager=creator_address,
        reserve=creator_address,
        freeze=creator_address,
        clawback=creator_address,
        url=ipfs_url,  # Metadata (optional)
        metadata_hash=None,
        decimals=decimals
    )

    # Sign the transaction
    signed_txn = txn.sign(private_key)

    # Send the transaction
    txid = algod_client.send_transaction(signed_txn)

    # Wait for transaction confirmation
    results = transaction.wait_for_confirmation(algod_client, txid, 4)

    asset_id = results["asset-index"]
    return {"status": "success", "txid": txid, "asset_id": asset_id, "confirmed_txn": results}


