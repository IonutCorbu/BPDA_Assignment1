import time
from pathlib import Path
from dotenv import load_dotenv
from multiversx_sdk import Address
from multiversx_sdk.abi import Abi
from multiversx_sdk import (ProxyNetworkProvider, QueryRunnerAdapter,
                            SmartContractQueriesController,ApiNetworkProvider)
from multiversx_sdk import UserSigner,UserPEM, TransactionComputer, Token, TokenTransfer
from multiversx_sdk import SmartContractTransactionsFactory,TransactionsFactoryConfig
import base64


contract = Address.new_from_bech32("erd1qqqqqqqqqqqqqpgqrqz7r8yl5dav2z0fgnn302l2w7xynygruvaq76m26j")
query_runner = QueryRunnerAdapter(ProxyNetworkProvider("https://devnet-api.multiversx.com"))
provider = ApiNetworkProvider("https://devnet-api.multiversx.com")
abi = Abi.load(Path("./tema-1.abi.json"))
query_controller = SmartContractQueriesController(query_runner,abi)
signer = UserSigner.from_pem_file(Path(r"D:\UPB SAS\Anul 1\BPDA\wallet_online.pem"))
signer_address = signer.get_pubkey().to_address(hrp="erd")
account_on_network = provider.get_account(signer_address)



gas_limit = 3000000 
chain_id = "D"
config = TransactionsFactoryConfig(chain_id)
factory = SmartContractTransactionsFactory(config)

    
    
def query_nftSupply():

    query = query_controller.create_query(
        contract=contract.to_bech32(),
        function="nftSupply",
        arguments=[]
    )
    response = query_controller.run_query(query)
    data_parts = query_controller.parse_query_response(response)
    return data_parts



def transNftProperties():

    tx = factory.create_transaction_for_execute(
    sender=signer_address,
    contract=contract,
    function="getYourNftCardProperties",
    gas_limit=30000000,
    arguments=[]
    )
    
    account_on_network = provider.get_account(signer_address)
    tx.nonce = account_on_network.nonce
    transaction_computer = TransactionComputer()
    bytes_for_signing = transaction_computer.compute_bytes_for_signing(tx)
    tx.signature = signer.sign(bytes_for_signing)
    hash = provider.send_transaction(tx)
    
    is_completed = False
    while not is_completed:
        time.sleep(5) 
        tx_status = provider.get_transaction(hash)
        is_completed = tx_status.is_completed
        if is_completed:
            break
    try:
        return [hash,base64.b64decode(provider.get_transaction(hash).raw_response['results'][0]['data']).decode("utf-8").split("@")[2]]
    except:
        return [hash,base64.b64decode(provider.get_transaction(hash).raw_response['logs']['events'][0]['data']).decode('utf-8').split('@')[2]]

def getNftDetails():
    tx_details = base64.b64decode(provider.get_transaction("a04b71c17845418872b81718bb550c5801e13d9f116135dccb3474a1b7c8bd68").raw_response['logs']['events'][0]['data']).decode('utf-8').split('@')[2]
    return tx_details
    
#CIDNFT-13c571
#ionut_daniel.corbu
#https://upload.wikimedia.org/wikipedia/en/5/5c/Mario_by_Shigehisa_Nakaue.png
def createNft(ntf_identifier,nftName,nftDetails,uri):
    # nftDetails=getNftDetails()

    tx = factory.create_transaction_for_execute(
    sender=signer_address,
    contract=signer_address,
    gas_limit=3000000,
    function="ESDTNFTCreate",
    arguments=[ntf_identifier,1,nftName,1000,0,int(nftDetails,16),uri]
    )
    
    account_on_network = provider.get_account(signer_address)
    tx.nonce = account_on_network.nonce
    transaction_computer = TransactionComputer()
    bytes_for_signing = transaction_computer.compute_bytes_for_signing(tx)
    tx.signature = signer.sign(bytes_for_signing)
    hash = provider.send_transaction(tx)
    
    is_completed = False
    while not is_completed:
        time.sleep(5) 
        tx_status = provider.get_transaction(hash)
        is_completed = tx_status.is_completed
        if is_completed:
            break
    
    
    return [hash,base64.b64decode(provider.get_transaction(hash).raw_response['results'][0]['data']).decode("utf-8").split("@")[2]]




def searchForNFT(nftDetails,nfts):
    index=1
    for nft in nfts[0]:
        formatted_string = ''.join(f'{byte:02x}' for byte in nft.attributes)
        if formatted_string==nftDetails:
            return index
        index = index + 1

def exchangeNFT(nftDetails,ntf_identifier,own_nft_nounce):
    
    nonce=searchForNFT(nftDetails,query_nftSupply())
    
    token = Token(identifier=ntf_identifier, nonce=int(own_nft_nounce,16))
    transfer = TokenTransfer(token=token, amount=1)

    tx = factory.create_transaction_for_execute(
    sender=signer_address,
    contract=contract,
    function="exchangeNft",
    gas_limit=30000000,
    arguments=[nonce],
    token_transfers=[transfer]
    )
    
    account_on_network = provider.get_account(signer_address)
    tx.nonce = account_on_network.nonce
    transaction_computer = TransactionComputer()
    bytes_for_signing = transaction_computer.compute_bytes_for_signing(tx)
    tx.signature = signer.sign(bytes_for_signing)
    hash = provider.send_transaction(tx)
    return hash


    

[_,nftDetails]=transNftProperties()
[_,nonce]=createNft("CIDNFT-13c571","ionut_daniel.corbu",nftDetails,"https://upload.wikimedia.org/wikipedia/en/5/5c/Mario_by_Shigehisa_Nakaue.png")
hash=exchangeNFT(nftDetails,"CIDNFT-13c571",nonce)
print(hash)









