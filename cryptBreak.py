import sys
from BitVector import *

BLOCKSIZE = 16  # Size of each block in bits
PassPhrase = "Hopes and dreams of a million years"  # Passphrase used for initial vector generation
numbytes = BLOCKSIZE // 8  # Number of bytes per block

def makeInitialVector():
    # Generate initial vector (IV) using PassPhrase
    bv_iv = BitVector(bitlist=[0]*BLOCKSIZE)  # Initialize bit vector with all zeros

    # Iterate through PassPhrase in blocks and XOR with IV
    for i in range(0, len(PassPhrase) // numbytes):
        textstr = PassPhrase[i*numbytes: (i+1)*numbytes]  # Extract block of PassPhrase
        bv_iv ^= BitVector(textstring=textstr)  # XOR operation with IV

    return bv_iv  # Return the resulting IV

def getEncryptedText():
    # Read encrypted text from file specified in command-line arguments
    FILEIN = open(sys.argv[1])  # Open file for reading
    encrypted_bv = BitVector(hexstring=FILEIN.read())  # Read hexadecimal string and convert to bit vector
    return encrypted_bv

def attack(key, bv_iv, encrypted_bv):
    # Attempt decryption using brute-force attack

    # Prepare key for XOR operation
    key_bv = BitVector(bitlist=[0]*BLOCKSIZE)
    for i in range(0, len(key) // numbytes):
        keyblock = key[i*numbytes: (i+1)*numbytes]
        key_bv ^= BitVector(textstring=keyblock)

    msg_decrypted_bv = BitVector(size=0)  # Initialize decrypted message bit vector

    previous_decrypted_block = bv_iv  # Initialize previous decrypted block as IV
    # Iterate through encrypted blocks and perform XOR operations
    for i in range(0, len(encrypted_bv) // BLOCKSIZE):
        bv = encrypted_bv[i * BLOCKSIZE: (i+1)*BLOCKSIZE]  # Extract encrypted block
        temp = bv.deep_copy()
        bv ^= previous_decrypted_block  # XOR with previous decrypted block
        previous_decrypted_block = temp
        bv ^= key_bv  # XOR with key
        msg_decrypted_bv += bv  # Append result to decrypted message

    outputText = msg_decrypted_bv.get_text_from_bitvector()  # Convert decrypted message to text
    return outputText  # Return the decrypted message

def main():
    bv_iv = makeInitialVector()  # Generate initial vector
    encrypted_bv = getEncryptedText()  # Read encrypted text
    key = ""  # Initialize key

    print('-----Kindly wait a few moment-----')
    # Brute-force attack: try all possible keys
    for i in range(0,256):
        for j in range(0,256):
            key = chr(i) + chr(j)  # Generate key
            outputText = attack(key, bv_iv, encrypted_bv)  # Attempt decryption
            # If 'Douglas Adams' is found in decrypted message, print key and original message
            if outputText.find('Douglas Adams') != -1:
                print('Key : '+key)
                print("Original Message : "+outputText)
                break

if __name__=="__main__":
    main()
