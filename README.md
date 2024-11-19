# BPDA Assignment 1

## Overview
This project demonstrates the interaction with an NFT smart contract through various functions that help manage NFTs. The main functions used in this assignment are as follows:

### nftSupply
The `nftSupply` function was used to query the smart contract to obtain the existing NFTs. This function allows us to fetch the total supply of NFTs available in the contract.

### getYourNftCardProperties
The `getYourNftCardProperties` function was used as a transaction to "pick" the attributes for the NFT we need to create. The attributes for the NFT are chosen randomly, simulating the process of generating unique properties for each NFT.

### ESDTNFTCreate
The `ESDTNFTCreate` function was used to create the NFT with the attributes that we obtained earlier. This function ensures that the NFT is created within a specific collection tied to the wallet being used. The newly created NFT is added to the wallet's collection.

### Search for NFT Nonce
In order to perform an exchange of the NFT, we needed to find the nonce of the NFT within the smart contract's collection. A specific function was used to search for the first NFT with the same attributes that were obtained earlier.

### exchangeNFT(nonce)
The `exchangeNFT` function was used to perform the exchange. The argument passed to this function is the nonce of the NFT that we want to obtain. To select the correct NFT from our local collection, a `Token` object was created using the collection identifier and the nonce of the NFT. Additionally, a `TokenTransfer` object was used to specify the amount of NFTs being exchanged.

## Summary
This process involved querying the smart contract for existing NFTs, randomly selecting attributes for a new NFT, creating it, and performing an exchange with another NFT from the SC collection. The project demonstrates the use of smart contract interactions and the creation/exchange of NFTs in a blockchain-based environment.
