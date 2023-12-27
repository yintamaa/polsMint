from web3 import Web3
import random
import threading

threads_count = 5

# private_key = ''
# address = ''

rpc_urls = [
    # Polygon
    # "https://polygon.llamarpc.com",
    # "https://polygon-pokt.nodies.app",
    # "https://rpc-mainnet.matic.quiknode.pro",
    # "https://polygon.rpc.blxrbdn.com",
    # "https://rpc.ankr.com/polygon",
    # "https://api.zan.top/node/v1/polygon/mainnet/public",
    # "https://endpoints.omniatech.io/v1/matic/mainnet/public",
    # "https://polygon.meowrpc.com",
    # "https://polygon-bor.publicnode.com",
    # "https://rpc-mainnet.maticvigil.com",
    # "https://1rpc.io/matic",
    # "https://polygon-rpc.com",
    # "https://polygon.drpc.org",
    # "https://polygon.gateway.tenderly.co",
    # "https://polygon-mainnet.rpcfast.com?api_key=xbhWBI1Wkguk8SNMu1bvvLurPGLXmgwYeC4S6g2H7WdwFigZSmPWVZRxrskEQwIf",
    # "https://polygon-mainnet.public.blastapi.io",
    # "https://polygon.api.onfinality.io/public",
    # "https://getblock.io/nodes/matic",
    # "https://gateway.tenderly.co/public/polygon",
    # "https://polygon.blockpi.network/v1/rpc/public",
    # "https://polygon-mainnet.g.alchemy.com/v2/demo",
    # "https://polygon-mainnet-public.unifra.io",
    # "https://polygonapi.terminet.io/rpc",
    # "https://matic-mainnet-archive-rpc.bwarelabs.com",
    # "https://matic-mainnet-full-rpc.bwarelabs.com",
    # "https://rpc-mainnet.matic.network"

    # "https://matic-mainnet.chainstacklabs.com",


    # avax
    # "https://api.avax.network/ext/bc/C/rpc",
    # "https://endpoints.omniatech.io/v1/avax/mainnet/public",
    # "https://avalanche.drpc.org",
    # "https://avalanche-c-chain.publicnode.com",
    # "https://1rpc.io/avax/c",
    # "https://avax-pokt.nodies.app/ext/bc/C/rpc",
    # "https://avax.meowrpc.com"

    # TIA
#    "https://celestia-rpc.polkachu.com"
#    "https://public-celestia-rpc.numia.xyz"
#    "https://celestia-rpc.mesa.newmetric.xyz"
#    "https://rpc.lunaroasis.net"
#    "https://rpc.celestia.nodestake.top "
#    "https://rpc-celestia.cosmos-spaces.cloud "
#    "https://rpc-celestia-01.stakeflow.io "
#    "http://celestia.rpc.nodersteam.com:29657"
#    "https://celestia-rpc.lavenderfive.com:443 "
#    "https://celestia-rpc.publicnode.com:443 "
#    "https://rpc-celestia.theamsolutions.info"
#    "https://celestia-rpc.enigma-validator.com "
#    "https://rpc-celestia.mzonder.com "
#    "https://celestia.rpc.stakin-nodes.com"
    
    # bsc-20 bnb
    # "https://rpc-bsc.48.club"
    # "https://bsc-dataseed4.defibit.io" 不能用，会panic

    # private rpc

    # polygon
    # "https://go.getblock.io/c9ba89c3a3d94089b6ad83f7504339a6"

    # bsc-20 bsb
    # "https://rpc.ankr.com/bsc/45d2800cd1e3b6aa412c7123b9d95a1ba2b6619c6003db75d1ee91d882632b41"

    # op_bnb
    # "https://opbnb-mainnet.nodereal.io/v1/e9a36765eb8a40b9bd12e680a1fd2bc5"
    "https://opbnb-mainnet.nodereal.io/v1/0a0e6a3aa19e4d5da06d2584d90c6b84"
]

lock = threading.Lock()
address2 = Web3.to_checksum_address(address)
print(address2)
web3 = Web3(Web3.HTTPProvider(random.choice(rpc_urls)))
print("connect", web3.is_connected())
print(Web3.from_wei(web3.eth.get_balance(address2), 'ether'))
c = 0
global nonce
nonce=web3.eth.get_transaction_count(address2)
print("nonce:" , nonce)

def mint():
    while True:
        lock.acquire()
        # print(f"nonce")
        global nonce
        global c
        tx = {
            'nonce': nonce,
            'chainId': 204, # OPBNB 
            # 'chainId': 137, # Polygon
            # 'chainId': 43114, # avax
            # 'chainId': 56, # BSC
            # 'chainId': 66,  # OKTC
            # 'chainId': 42161,  # Arbitrum One
            'to': address2,
            'from': address2,
            # mint 16进制数据
            'data': '0x646174613a6170706c69636174696f6e2f6a736f6e2c7b2270223a226f70627263222c226f70223a226d696e74222c227469636b223a226f70626e227d',
            'gasPrice': int(web3.eth.gas_price*1.1),
            'value': Web3.to_wei(0, 'ether')
        }
        nonce=nonce+1
        lock.release()
        try:
            gas = web3.eth.estimate_gas(tx)
            tx['gas'] = gas
            print(tx)
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            print("send_raw_transaction start")
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print("send_raw_transaction end")
            print("tx_hash: ", web3.to_hex(tx_hash))
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print("wait_for_transaction_receipt end")
            if receipt.status == 1:
                c += 1
                print(f"{c} Mint Success!")
            else:
                continue
        except Exception as e:
            print(e)


# 创建并启动线程
threads = []
for _ in range(threads_count):
    nonce=web3.eth.get_transaction_count(address2)
    t = threading.Thread(target=mint)
    t.start()
    threads.append(t)

# 等待所有线程完成
for t in threads:
    t.join()
