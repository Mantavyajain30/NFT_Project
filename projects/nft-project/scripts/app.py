from flask import Flask, jsonify, request
from flask_cors import CORS
from ASA import create_asa_nft  # Import the function you created
import os
from algosdk import account, transaction, mnemonic

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])


# Endpoint to mint NFT
@app.route('/mint-nft', methods=['POST'])
def mint_nft():
    data = request.form
    file = request.files['image']
    
    # Define Algorand credentials and connection parameters
    algod_address = "http://localhost:4001"
    algod_token = "a" * 64  
    creator_address = "L3BARDXYUN35W2O2VEKGOPVWFJ6JZZZX2XGJU4CJQVY5UEBDJLN7NVGGZY"  # Replace with your address
    passphrase = "robot absent donor define lumber great save have assist sorry consider render test video stone actress leopard pretty agent can dial capital broom abandon echo"
    
    # Save the uploaded image (optional - for local storage or IPFS upload)
    image_path = f"./uploads/{file.filename}"
    file.save(image_path)

    # Call create_asa_nft function to mint the NFT
    result = create_asa_nft(
        algod_address=algod_address,
        algod_token=algod_token,
        creator_address=creator_address,
        passphrase=passphrase,
        asset_name=data['name'],
        unit_name="MYNFT",  # Unit name can be same or different
        ipfs_url=image_path  # Replace with an actual IPFS URL if needed
    )

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
