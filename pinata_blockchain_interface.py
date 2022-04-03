# importing required libraries
import os
import json
import time
import flask
import vendor
import requests
import http.client
from sympy import re
from pathlib import Path
from datetime import datetime
from flask import jsonify, request
from requests.exceptions import HTTPError


# API config
API_KEY = 'f694c3630069a7eb90c8'
API_SECRET = '64497681bcf6ea841511b3e1dafdb1158874e68ef420af2bb701dd20a93680b3'

# configure your moibit base API
API_ENDPOINT = 'https://api.pinata.cloud'

# No need to update for use with Pinata
# test URL : API_URL = "http://api.open-notify.org/astros.json"
# check connection stability , makes it easier to debug , default ping URL = 'https://google.com'
def check_connection_status(API_URL='https://google.com'):
    # try to get a valid HttpResponse from google
    try:
        response = requests.get(API_URL)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
        print('Connection Stable')
        # True => the connection is stable and the network libraries are working properly
        return True
    # catch error if server sends a response code other than 'OK' - 200
    except HTTPError as http_err:
        # if it is a known error , output the error on the terminal and return False
        print("False , Error : {error}".format(error=http_err))
        return False
    # if an unknown exception , i.e. other than an Http Exception occurs , then catch here
    except Exception as err:
        # print to console and return false
        print("False , Error : {error}".format(error=err))
        return False
    # if the raised error is completely unexpected 
    else:
        # simply print the following message to the terminal and return false
        print("An UnKnown Error Occured")
        return False

# Pinata API based getter function - Updated to Use Pinata
# returns the amount of consumed storage on moibit : total alloted = 2 GB free space decentralized on pinata blockchain
def get_used_storage():
    # fetch the storage usage data
    try:
        # default parameters containing tokens required for authorization
        PARAMS = {
            'api_key': API_KEY,
            'api_secret': API_SECRET
        }
        # test using requests library : response = requests.get('{API}/moibit/v0/storageused'.format(API=API_ENDPOINT), params=PARAMS)
        # passing tokens in request header , request times out after 10 seconds : Counter measure for sniffing
        response = requests.get(
            '{API}/data/userPinnedDataTotal'.format(API=API_ENDPOINT),
            headers={
                'pinata_api_key': str(API_KEY),
                'pinata_secret_api_key': str(API_SECRET)
            },
            timeout=10
        )
        # check the status code returned by the moibit server
        # response.raise_for_status()
        # print the status code to the terminal
        print(response.status_code)
        # convert the data into json format
        json_response = response.json()
        # print this json data to the console
        print(response.json())
        # return the json response for use by the calling function
        return json_response
    
    # catch the error which might be thrown
    except HTTPError as http_err:
        # if it is a known error , output the error on the terminal and return False
        print("False , Error : {error}".format(error=http_err))
        return json.loads({'error' : 'unsuccessful fetch'})
    # if it is a known error but not a HttpResponse error , output the error on the terminal and return False
    except Exception as err:
        print("False , Error : {error}".format(error=err))
        return json.loads({'error' : 'unsuccessful fetch'})
    
def temp_file(message):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    filename = "txn " + vendor.create_transaction_id() + " " + dt_string
    
    with open(filename, 'w') as tempfile:
        tempfile.write(vendor.create_transaction_id() + "\n" + message)
    
    return filename
    
# experimental requests , secure header method ; DO NOT USE 
def write_to_pinata(message, filepath = None, pinataMetadata = None, pinataOptions = None):
    # trying fetching response
    files = None
    delete_file_post_op = False
    if filepath is None:
        delete_file_post_op = True
        filepath = temp_file(message)
    try:
        files = { 'file' : open(filepath, 'rb') }
    except Exception as error:
        print(error)
        print("Could not open the required file")
        return json.loads({'message' : 'could not load file'})
    try:
        # body parameters required for fetching
        data = {}
        data['pinataMetadata'] = json.dumps({
            "name" : filepath,
            "keyvalues" : {
                "time" : str(datetime.now())
            }
        })
        # if pinataMetadata is not None:
        #     data['pinataMetadata'] = pinataMetadata
        print(data)
        if pinataOptions is not None:
            data['pinataOptions'] = json.dumps(pinataOptions)
        # PARAMS = {
        #     'fileName': 'matic_transaction_ledger',
        #     'text': message,
        #     'create': 'false',
        #     'createFolders': 'false',
        #     'pinVersion': 'false'
        # }
        # fetching using requests : response = requests.get('{API}/moibit/v0/storageused'.format(API=API_ENDPOINT), params=PARAMS)
        # posting message and appending to end of existing file
        response = requests.post(
            '{API}/pinning/pinFileToIPFS'.format(API=API_ENDPOINT),
            headers={
                'pinata_api_key': API_KEY,             # API_KEY : to be shifted and stored into .env file
                'pinata_secret_api_key': API_SECRET    # API_SECRET :  to be shifted and stored into .env file
            },
            # params=PARAMS,
            data=data,
            files=files,
            timeout=10                                # timeout after 10 seconds , to avoid hanging of server and occupied ports
        )
        files['file'].close()
        if delete_file_post_op == True:
            try:
                os.remove(filepath)
            except Exception as error:
                print(error)
                pass
        # check the status code sent by moibit server
        # response.raise_for_status()
        # print the response to the terminal
        print(response.status_code)
        # convert response to json format
        json_response = response.json()
        # print out the json object to the console
        print(response.json())
        
        if response.status_code == 200:
            print("Uploaded At : {ipfs_url}".format(ipfs_url = read_from_pinata("pinned", filepath)))
    
    # if it is a known error , output the error on the terminal and return False
    except HTTPError as http_err:
        print("False , Error : {error}".format(error=http_err))
        return json.loads({'error' : 'unsuccessful fetch'})
    # if it is a known error but not a HttpResponse error , output the error on the terminal and return False
    except Exception as err:
        print("False , Error : {error}".format(error=err))
        return json.loads({'error' : 'unsuccessful fetch'})

def read_from_pinata(content_status, content_name):
    try:
        PARAMS = {
            "status" : content_status,
            "metadata[name]" : content_name
        }
        response = requests.get(
            '{API}/data/pinList'.format(API=API_ENDPOINT),
            headers={
                'pinata_api_key': API_KEY,             # API_KEY : to be shifted and stored into .env file
                'pinata_secret_api_key': API_SECRET    # API_SECRET :  to be shifted and stored into .env file
            },
            params=PARAMS,
            timeout=10                                # timeout after 10 seconds , to avoid hanging of server and occupied ports
        )
        # print the response to the terminal
        print(response.status_code)
        # convert response to json format
        json_response = response.json()
        # print out the json object to the console
        print(response.json())
        
        if response.status_code == 200:
            ipfs_url = "https://gateway.pinata.cloud/ipfs/{content_id}".format(content_id = json_response["rows"][0]["ipfs_pin_hash"])
            
        return ipfs_url
    
    # if it is a known error , output the error on the terminal and return False
    except HTTPError as http_err:
        print("False , Error : {error}".format(error=http_err))
        return json.loads({'error' : 'unsuccessful fetch'})
    # if it is a known error but not a HttpResponse error , output the error on the terminal and return False
    except Exception as err:
        print("False , Error : {error}".format(error=err))
        return json.loads({'error' : 'unsuccessful fetch'})

# Pinata API based setter function
# pushing the completed transaction once it has been completed to the pinata blockchain
def pinata_push(completed_transactions, transactionID):
    # the sha checksum of the transaction
    sha256_checksum = completed_transactions[transactionID][0]                              # added
    # the transaction ID 
    transaction_ID = completed_transactions[transactionID][1]                               # added
    # just another extra check just before pushing to the blockchain
    if transactionID == transaction_ID:
        # the customer ID
        customerID = completed_transactions[transactionID][2]                               # added
        # public key of the customer
        customerPublicKey = completed_transactions[transactionID][3]                        # added
        # time at which the post / transaction was created : UNIX
        transaction_creation_timestamp = completed_transactions[transactionID][4]           # added
        # the bidder ID
        bidderID = completed_transactions[transactionID][5]                                 # added
        # the public key of the bidder
        bidderPublicKey = completed_transactions[transactionID][6]                          # added
        # the time at which the bid was made
        bid_creation_timestamp = completed_transactions[transactionID][7]                   # added
        # verification message which was used to verify the transaction
        verification_message_sha = completed_transactions[transactionID][8]                 # added
        
        # making the transaction string for easy writing to the pinata blockchain using moibit API
        # adding sha checksum
        transaction_string = "sha256_trans : " + str(sha256_checksum) + " , "
        # adding transaction ID
        transaction_string += "transID : " + str(transaction_ID) + " , "
        # adding custoemr ID
        transaction_string += "customerID : " + str(customerID) + " , "
        # adding customer public key
        transaction_string += "customerPublicKey : " + str(customerPublicKey) + " , "
        # adding the transaction creation timestamp
        transaction_string += "trans_timestamp : " + str(transaction_creation_timestamp) + " , "
        # adding the bidder ID
        transaction_string += "bidderID : " + str(bidderID) + " , "
        # adding the bidder public key 
        transaction_string += "bidderPublicKey : " + str(bidderPublicKey) + " , "
        # adding the bid timestamp
        transaction_string += "bid_timestamp : " + str(bid_creation_timestamp) + " , "
        # adding the sha code of the verification message used to verify the message
        transaction_string += "message_sha : " + str(verification_message_sha) + " ."
        
        write_to_pinata(transaction_string)
        
# For DEBUGGING : 
# check_connection_status()
# print("Testing the used storage function : ")
# get_used_storage()
# write_to_pinata("check check 2")
# read_from_pinata("pinned", "txn eD8yhzSF7rdTjRJzTINovxxdf6MICkkJwkxjjAFt581pxkffow2rIzXTLlx23P2j 03_04_2022_19_47_01")
# print("Testing the moibit write function : ")
# write_message_to_moibit('my name is ansh sarkar and I have written this message using an API')
