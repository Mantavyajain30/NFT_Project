from algosdk import account, mnemonic

# Generate account
private_key, address = account.generate_account()

# Print details
print(f"Address: {address}")
print(f"Private Key: {private_key}")
print(f"Mnemonic: {mnemonic.from_private_key(private_key)}")
