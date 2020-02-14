# mixin assert ids

# refers to: https://mixin.one/snapshots/
BTC_ASSET_ID = "c6d0c728-2624-429b-8e0d-d9d19b6592fa"
EOS_ASSET_ID = "6cfe566e-4aad-470b-8c9a-2fd35b49c68d"  # eos link
XIN_ASSET_ID = "c94ac88f-4671-3976-b60a-09064f1811e8"
BOX_ASSET_ID = "f5ef6b5d-cc5a-3d90-b2c0-a2fd386e7a3c"
PRS_ASSET_ID = "3edb734c-6d6f-32ff-ab03-4eb43640c758"  # press1
LY_ASSET_ID = "35f7a3a3-4335-3bf3-beca-685836602d72"  # Lilin & yangjihui
CNB_ASSET_ID = "965e5c6e-434c-3fa9-b780-c50f43cd955c"
USDT_ASSET_ID = "4d8c508b-91c5-375b-92b0-ee702ed2dac5"  # usdt 2.0
ETH_ASSET_ID = "43d61dcd-e413-450d-80b8-101d5e903357"
CANDY_ASSET_ID = "43b645fc-a52c-38a3-8d3b-705e7aaefa15"  # down...

# name:
asset_name = {
    "c6d0c728-2624-429b-8e0d-d9d19b6592fa": "BTC",
    "6cfe566e-4aad-470b-8c9a-2fd35b49c68d": "EOS",  # eos link
    "c94ac88f-4671-3976-b60a-09064f1811e8": "XIN",
    "f5ef6b5d-cc5a-3d90-b2c0-a2fd386e7a3c": "BOX",
    "3edb734c-6d6f-32ff-ab03-4eb43640c758": "PRS",  # press1
    "35f7a3a3-4335-3bf3-beca-685836602d72": "LY_ASSET_ID",  # Lilin & yangjihui
    "965e5c6e-434c-3fa9-b780-c50f43cd955c": "CNB",
    "4d8c508b-91c5-375b-92b0-ee702ed2dac5": "USDT",  # usdt 2.0
    "43d61dcd-e413-450d-80b8-101d5e903357": "ETH",
    "43b645fc-a52c-38a3-8d3b-705e7aaefa15": "CANDY"  # down...
}

def get_asset_name_by_uuid( uuid ):
    return asset_name[ uuid ]

def get_asset_name_box():
    return get_asset_name_by_uuid( BOX_ASSET_ID )

def get_asset_name_btc():
    return get_asset_name_by_uuid( BTC_ASSET_ID )

def get_asset_name_eos():
    return get_asset_name_by_uuid( EOS_ASSET_ID )

def get_asset_name_xin():
    return get_asset_name_by_uuid( XIN_ASSET_ID )

def get_asset_name_prs():
    return get_asset_name_by_uuid( PRS_ASSET_ID )

def get_asset_name_cnb():
    return get_asset_name_by_uuid( CNB_ASSET_ID )

def get_asset_name_usdt():
    return get_asset_name_by_uuid( USDT_ASSET_ID )

def get_asset_name_eth():
    return get_asset_name_by_uuid( ETH_ASSET_ID )
