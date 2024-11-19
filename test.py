import time
import os
from pathlib import Path
from dotenv import load_dotenv
from multiversx_sdk import Address
from multiversx_sdk.abi import Abi
from multiversx_sdk import (ProxyNetworkProvider, QueryRunnerAdapter,
                            SmartContractQueriesController,ApiNetworkProvider)
from multiversx_sdk import UserSigner,UserPEM, TransactionComputer, Token, TokenTransfer
from multiversx_sdk import SmartContractTransactionsFactory,TransactionsFactoryConfig
import base64
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

contract = Address.new_from_bech32("erd1qqqqqqqqqqqqqpgqrqz7r8yl5dav2z0fgnn302l2w7xynygruvaq76m26j")
query_runner = QueryRunnerAdapter(ProxyNetworkProvider("https://devnet-api.multiversx.com"))
provider = ApiNetworkProvider("https://devnet-api.multiversx.com")
abi = Abi.load(Path("./tema-1.abi.json"))
query_controller = SmartContractQueriesController(query_runner,abi)
# signer = UserSigner.from_pem_file(Path(r"D:\UPB SAS\Anul 1\BPDA\wallet_online.pem"))
# signer_address = signer.get_pubkey().to_address(hrp="erd")
# account_on_network = provider.get_account(signer_address)


app = Flask(__name__)
CORS(app, origins="http://localhost:3000") 
UPLOAD_FOLDER = './uploaded_pem_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pem'}

gas_limit = 3000000 
chain_id = "D"
config = TransactionsFactoryConfig(chain_id)
factory = SmartContractTransactionsFactory(config)


DB_HOST = "localhost"       
DB_USER = "root"            
DB_PASSWORD = "root"     
DB_NAME = "nft_transactions" 

def get_db_connection():
    """Connect to MySQL database, optionally specifying a database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_database():
    """Create the database if it doesn't exist."""
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
        connection.close()
    print(f"Database `{DB_NAME}` is ready.")

def create_transaction_table():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS transaction_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                transaction_hash VARCHAR(255),
                function_called VARCHAR(255),
                pem_used VARCHAR(255),
                transaction_response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        connection.close()
        print("Table `transaction_logs` is ready.")

def save_transaction_to_db(transaction_hash, function_called, pem_used, response):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        query = """
            INSERT INTO transaction_logs (transaction_hash, function_called, pem_used, transaction_response)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (transaction_hash, function_called, pem_used, response))
        connection.commit()
        cursor.close()
        connection.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/list-pem', methods=['GET'])
def list_pem():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    pem_files = [f for f in files if f.endswith('.pem')]
    return jsonify({"uploaded_pem_files": pem_files}), 200

@app.route('/upload-pem', methods=['POST'])
def upload_pem():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200
    else:
        return jsonify({"error": "Invalid file type. Only .pem files are allowed."}), 400
    
    

def query_nftSupply():

    query = query_controller.create_query(
        contract=contract.to_bech32(),
        function="nftSupply",
        arguments=[]
    )
    response = query_controller.run_query(query)
    data_parts = query_controller.parse_query_response(response)
    return data_parts


@app.route('/nft-supply', methods=['GET'])
def get_nft_supply():
    try:
        nft_supply = query_nftSupply()
        return str(nft_supply), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/trans-nft-properties', methods=['POST'])
def trans_nft_properties_endpoint():
    file_name = request.json.get('file_name')  
    if not file_name:
        return jsonify({"error": "file_name is required"}), 400

    pem_path = Path(f"./uploaded_pem_files/{file_name}") 

    if not pem_path.exists():
        return jsonify({"error": "unexistent file"}), 400

    try:
        signer = UserSigner.from_pem_file(pem_path)
        signer_address = signer.get_pubkey().to_address(hrp="erd")
        account_on_network = provider.get_account(signer_address)

        tx = factory.create_transaction_for_execute(
            sender=signer_address,
            contract=contract,
            function="getYourNftCardProperties",
            gas_limit=60000000,
            arguments=[]
        )

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
        if provider.get_transaction(hash).raw_response['status']=='fail':
            return jsonify({"error": base64.b64decode(provider.get_transaction(hash).raw_response['logs']['events'][1]['data']).decode('utf-8') }), 400
        try:
            result = base64.b64decode(provider.get_transaction(hash).raw_response['results'][0]['data']).decode("utf-8").split("@")[2]
        except:
            result = base64.b64decode(provider.get_transaction(hash).raw_response['logs']['events'][0]['data']).decode('utf-8').split('@')[2]

        save_transaction_to_db(hash, "nftProperties", file_name, hash+" "+result)
        return jsonify({"transaction_hash": hash, "result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# def transNftProperties():

#     tx = factory.create_transaction_for_execute(
#     sender=signer_address,
#     contract=contract,
#     function="getYourNftCardProperties",
#     gas_limit=30000000,
#     arguments=[]
#     )
    
#     account_on_network = provider.get_account(signer_address)
#     tx.nonce = account_on_network.nonce
#     transaction_computer = TransactionComputer()
#     bytes_for_signing = transaction_computer.compute_bytes_for_signing(tx)
#     tx.signature = signer.sign(bytes_for_signing)
#     hash = provider.send_transaction(tx)
    
#     is_completed = False
#     while not is_completed:
#         time.sleep(5) 
#         tx_status = provider.get_transaction(hash)
#         is_completed = tx_status.is_completed
#         if is_completed:
#             break
#     try:
#         return [hash,base64.b64decode(provider.get_transaction(hash).raw_response['results'][0]['data']).decode("utf-8").split("@")[2]]
#     except:
#         return [hash,base64.b64decode(provider.get_transaction(hash).raw_response['logs']['events'][0]['data']).decode('utf-8').split('@')[2]]

# def getNftDetails():
#     tx_details = base64.b64decode(provider.get_transaction("a04b71c17845418872b81718bb550c5801e13d9f116135dccb3474a1b7c8bd68").raw_response['logs']['events'][0]['data']).decode('utf-8').split('@')[2]
#     return tx_details
    
# #CIDNFT-13c571
# #ionut_daniel.corbu
# #https://upload.wikimedia.org/wikipedia/en/5/5c/Mario_by_Shigehisa_Nakaue.png
# def createNft(ntf_identifier,nftName,nftDetails,uri):
#     # nftDetails=getNftDetails()

#     tx = factory.create_transaction_for_execute(
#     sender=signer_address,
#     contract=signer_address,
#     gas_limit=3000000,
#     function="ESDTNFTCreate",
#     arguments=[ntf_identifier,1,nftName,1000,0,int(nftDetails,16),uri]
#     )
    
#     account_on_network = provider.get_account(signer_address)
#     tx.nonce = account_on_network.nonce
#     transaction_computer = TransactionComputer()
#     bytes_for_signing = transaction_computer.compute_bytes_for_signing(tx)
#     tx.signature = signer.sign(bytes_for_signing)
#     hash = provider.send_transaction(tx)
    
#     is_completed = False
#     while not is_completed:
#         time.sleep(5) 
#         tx_status = provider.get_transaction(hash)
#         is_completed = tx_status.is_completed
#         if is_completed:
#             break
    
    
#     return [hash,base64.b64decode(provider.get_transaction(hash).raw_response['results'][0]['data']).decode("utf-8").split("@")[2]]

@app.route('/create-nft', methods=['POST'])
def create_nft_endpoint():

    try:
        data = request.json
        ntf_identifier = data.get('ntf_identifier')
        nftName = data.get('nftName')
        nftDetails = data.get('nftDetails')
        uri = data.get('uri')
        file_name = data.get('file_name')

        if not all([ntf_identifier, nftName, nftDetails, uri, file_name]):
            return jsonify({"error": "All fields (ntf_identifier, nftName, nftDetails, uri, file_name) are required"}), 400

        pem_path = Path(f"./uploaded_pem_files/{file_name}")
        if not pem_path.exists():
            return jsonify({"error": "unexistent file"}), 400

        signer = UserSigner.from_pem_file(pem_path)
        signer_address = signer.get_pubkey().to_address(hrp="erd")
        account_on_network = provider.get_account(signer_address)

        tx = factory.create_transaction_for_execute(
            sender=signer_address,
            contract=signer_address,
            gas_limit=3000000,
            function="ESDTNFTCreate",
            arguments=[
                ntf_identifier,
                1,  
                nftName,
                1000,  
                0,  
                int(nftDetails, 16), 
                uri
            ]
        )

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

        try:
            result = base64.b64decode(provider.get_transaction(hash).raw_response['results'][0]['data']).decode("utf-8").split("@")[2]
        except:
            result = base64.b64decode(provider.get_transaction(hash).raw_response['logs']['events'][0]['data']).decode("utf-8").split("@")[2]
        
        save_transaction_to_db(hash, "ESDTNFTCreate", file_name, result)
        return jsonify({"transaction_hash": hash, "result": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



def searchForNFT(nftDetails,nfts):
    index=1
    for nft in nfts[0]:
        formatted_string = ''.join(f'{byte:02x}' for byte in nft.attributes)
        if formatted_string==nftDetails:
            return index
        index = index + 1

# def exchangeNFT(nftDetails,ntf_identifier,own_nft_nounce):
    
#     nonce=searchForNFT(nftDetails,query_nftSupply())
    
#     token = Token(identifier=ntf_identifier, nonce=int(own_nft_nounce,16))
#     transfer = TokenTransfer(token=token, amount=1)

#     tx = factory.create_transaction_for_execute(
#     sender=signer_address,
#     contract=contract,
#     function="exchangeNft",
#     gas_limit=30000000,
#     arguments=[nonce],
#     token_transfers=[transfer]
#     )
    
#     account_on_network = provider.get_account(signer_address)
#     tx.nonce = account_on_network.nonce
#     transaction_computer = TransactionComputer()
#     bytes_for_signing = transaction_computer.compute_bytes_for_signing(tx)
#     tx.signature = signer.sign(bytes_for_signing)
#     hash = provider.send_transaction(tx)
#     return hash

def exchangeNFT(nftDetails, ntf_identifier, own_nft_nounce, pem_path):

    try:
        signer = UserSigner.from_pem_file(pem_path)
        signer_address = signer.get_pubkey().to_address(hrp="erd")
    except Exception as e:
        return str(e), 400
    
    nonce = searchForNFT(nftDetails, query_nftSupply())

    token = Token(identifier=ntf_identifier, nonce=int(own_nft_nounce, 16))
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

    is_completed = False
    while not is_completed:
        time.sleep(5)
        tx_status = provider.get_transaction(hash)
        is_completed = tx_status.is_completed

    if provider.get_transaction(hash).raw_response['status']=='fail':
            return jsonify({"error": base64.b64decode(provider.get_transaction(hash).raw_response['logs']['events'][1]['data']).decode('utf-8') }), 400

    save_transaction_to_db(hash, "exchangeNft", pem_path.name, hash)

    return hash

@app.route('/exchange-nft', methods=['POST'])
def exchange_nft_endpoint():

    data = request.json
    required_fields = ["file_name", "nftDetails", "ntf_identifier", "own_nft_nounce"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

    file_name = data["file_name"]
    nftDetails = data["nftDetails"]
    ntf_identifier = data["ntf_identifier"]
    own_nft_nounce = data["own_nft_nounce"]

    pem_path = Path(f"./uploaded_pem_files/{file_name}")

    if not pem_path.exists():
        return jsonify({"error": "unexistent file"}), 400

    try:
        hash = exchangeNFT(nftDetails, ntf_identifier, own_nft_nounce, pem_path)
        save_transaction_to_db(hash, "exchangeNFT", file_name, hash)
        return jsonify({"transaction_hash": hash}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# [_,nftDetails]=transNftProperties()
# [_,nonce]=createNft("CIDNFT-13c571","ionut_daniel.corbu",nftDetails,"https://upload.wikimedia.org/wikipedia/en/5/5c/Mario_by_Shigehisa_Nakaue.png")
# hash=exchangeNFT(nftDetails,"CIDNFT-13c571",nonce)
# print(hash)

#tx_details = provider.get_transaction("f743ec4408ba17d4a4f8fbc17f8aeda36a06c51c2a9c3e6b2067e94351ffc425")
#tx_details1 = base64.b64decode(provider.get_transaction("f743ec4408ba17d4a4f8fbc17f8aeda36a06c51c2a9c3e6b2067e94351ffc425").raw_response['logs']['events'][0]['data']).decode('utf-8').split('@')[2]
#print(tx_details1)

@app.route('/history', methods=['GET'])
def get_history():
    try:
        # Connect to the database
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Failed to connect to the database"}), 500

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Query to get all transaction logs
        cursor.execute("SELECT * FROM transaction_logs ORDER BY timestamp DESC")

        # Fetch all the rows from the executed query
        rows = cursor.fetchall()

        # List to store the formatted results
        transactions = []

        # Map each row into a dictionary and append it to the transactions list
        for row in rows:
            transaction = {
                "id": row[0],
                "transaction_hash": row[1],
                "function_called": row[2],
                "pem_used": row[3],
                "transaction_response": row[4],
                "timestamp": row[5].strftime('%Y-%m-%d %H:%M:%S')  # Format the timestamp
            }
            transactions.append(transaction)

        # Close the cursor and the database connection
        cursor.close()
        connection.close()

        # Return the transaction history as a JSON response
        return jsonify({"transaction_history": transactions}), 200

    except Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    create_database()
    create_transaction_table()
    
    app.run(debug=True, port=5000)






