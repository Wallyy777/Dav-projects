'''
The algorithm below works as follows:
Suppose we want to encrypt the string
			"abcde",
using the initial nonce
			[23, 108].
The first thing is to encode the string into ascii bytes:
			[97, 98, 99, 100, 101],
Next, these bytes must be "packaged" into blocks of two bytes each:
			[[97, 98], [99, 100], [101, 0]].
(Notice that a "0" byte is appended on the end if the message is has an odd length.)
Now, the message will be encrypted block by block.
To encrypt a block, it is first xored with the current nonce:
			[97 ^ 23, 98 ^ 108] = [118, 14],
Then the resulting block is chunked:
			[118, 14] --> [14, 6, 0, 14]
and this chunked block goes through 16 iterations of encryption.
Each iteration maps the elements in the list to corresponding 4-bit values using the "table" function (see below).
Then, the 4-bit chunks are scrambled using the "shuffle" function (see below).
After 16 rounds of encryption, the first chunk is encrypted as:
			[62, 218].
The nonce is updated so that it equals [62, 218], and the next block is encrypted.
This continues until all blocks are encrypted.
The resulting ciphertext is:
				[62, 218, 59, 87, 211, 85]
Each of these steps is invertible, so carefully undoing them in the correct order decrypts the cipher text.
Please note that the original nonce is needed for successful decryption.

****Your Task****
Your task is to implement the first three functions in this file.
You may not alter __anything__ else.
You may not change the name or parameters of these functions.
Have fun!

When you are done, your program should be able to encrypt and decrypt a file.
'''

import sys
import random
		
def encryptit(bits4array):
    # One iteration ("it") of encryption on a block
    mapped_block = []
    for i in bits4array :
        mapped_block.append(table(i))
        
    # Scramble the 4-bit chunks using the shuffle function
    chunked_block = shuffle(mapped_block)
    
    return chunked_block
	
def encrypt4b(bits4array):
    # Fully encrypts (16 encryptit iterations) a block
    for _ in range(16):
        bits4array = encryptit(bits4array)
    return bits4array

def encrypt(message, nonce):
    # Get the message in blocked form
    blkd_msg = package(message)
    
    # An empty list variable to hold the answer
    ciphertext = []
    
    # For each block (a list of two bytes)
    for block in blkd_msg:
        # XOR the chunk with the nonce
        xored_block = [block[0] ^ nonce[0], block[1] ^ nonce[1]]
        
        # Encrypt the chunk
        encrypted_block = encrypt4b(to4bitarray(xored_block))
        
        
        encrypted_block = tobytesarray(encrypted_block)
        
        # Add the chunk to the end of the ciphertext
        ciphertext.append(encrypted_block)
        
        # Update the nonce to be the most recently encrypted block
        nonce = encrypted_block  # Ensure nonce has length 2
    
    # Unpackage answer to a list of bytes
    encrypted_message = unpackage(ciphertext)
    
    return encrypted_message


def table(bits) :
		'''
		encrypts a single chunk.
		bits is a 4 bit plaintext chunk (0-15).
		returns the corresponding encrypted 4-bit chunk.
		'''
		if bits == 1 :
				return 2
		if bits == 2 :
				return 8
		if bits == 3 :
				return 15
		if bits == 4 :
				return 3
		if bits == 5 :
				return 5
		if bits == 6 :
				return 4
		if bits == 7:
				return 0
		if bits == 8 :
				return 1
		if bits == 9 :
				return 6
		if bits == 10 :
				return 7
		if bits == 11 :
				return 12
		if bits == 12 :
				return 13
		if bits == 13 :
				return 10
		if bits == 14 :
				return 9
		if bits == 15 :
				return 14
		if bits == 0 :
				return 11
				
def itable(bits) :
		'''
		decrypts a single chunk.
		bits is a 4 bit encrypted chunk.
		returns the corresponding decrypted 4-bit chunk.
		'''
		if bits == 11 :
				return 0
		if bits == 14 :
				return 15
		if bits == 9 :
				return 14
		if bits == 10 :
				return 13
		if bits == 13 :
				return 12
		if bits == 12 :
				return 11
		if bits == 7 :
				return 10
		if bits == 6 :
				return 9
		if bits == 1 :
				return 8
		if bits == 0:
				return 7
		if bits == 4:
				return 6
		if bits == 5 :
				return 5
		if bits == 3 :
				return 4
		if bits == 15 :
				return 3
		if bits == 8 :
				return 2
		if bits == 2 :
				return 1
				
def to4bitarray(bytes) :
		'''
		converts a list of bytes (a block) into a list of values less than 16 (a list of chunks).
		For example if the bytes are [63, 31] = [00111111, 00011111],
		this function returns [0011, 1111, 0001, 1111] = [3, 15, 1, 15].
		'''
		answer = []
		while len(bytes) > 0 :
				byte = bytes.pop()
				oldlen = len(answer)
				while len(answer) < oldlen + 2 :
						answer = [byte % 16] + answer
						byte = byte // 16
		return answer
		
def tobytesarray(bit4array) :
		'''
		converts a list of 4-bit values (a list of chunks) into an array of bytes (a block).
		bit4array is an array of values which are all between 0 and 15, inclusive.
		For example, if bit4array is [3, 15, 1, 15] = [0011, 1111, 0001, 1111],
		this function returns [00111111, 00011111] = [63, 31]
		'''
		big = 1
		v = 0
		answer = []
		for i in bit4array :
				if big :
						v = i
						v *= 16
						big = 0
				else :
						big = 1
						v += i
						answer.append(v)
		return answer
		
def shuffle(b4a) :
		'''
		shuffles the 4-bit chunks of a 16 bit block around, as the code described below.
		This is the scrambler.
		'''
		i0 = b4a[0]
		i1 = b4a[1]
		i2 = b4a[2]
		i3 = b4a[3]
		return [i3, i1, i0, i2]
		
def ishuffle(b4a) :
		'''
		unshuffles the 4-bit chunks of a 16 bit block around, as the code described below.
		This is the descrambler.
		'''
		i0 = b4a[2]
		i1 = b4a[1]
		i2 = b4a[3]
		i3 = b4a[0]
		return [i0, i1, i2, i3]
			
def package(message) :
		'''
		packs a message into arrays of two bytes each (into blocks).
		a message is an list of bytes.
		returns a list of 2 byte lists (a list of blocks).
		For example, if message = [1, 2, 3, 4], then this returns [[1, 2], [3, 4]].
		'''
		if len(message) % 2 != 0 :
				message += b'\0'
		part1 = message
		big = 0
		part2 = []
		for d in part1 :
				if big == 0 :
						big = 1
						a = [d]
				else :
						big = 0
						a.append(d)
						part2 += [a]
		return part2
		
def unpackage(array) :
		'''
		unpacks an array of blocks (2 byte lists) into a message of bytes.
		array is a list of 2-byte lists (blocks).
		returns a list of bytes (flattens the list).
		For example, if array = [[1, 2], [3, 4]], then this returns [1, 2, 3, 4].
		'''
		answer = []
		for a in array :
				for d in a :
						answer += [d]
		return answer
		
def decryptit(bits4array) :
		'''
		does one iteration ("it") of decryption on block.
		'''
		part1 = ishuffle(bits4array) #unscramble
		return [itable(d) for d in part1] #map encrypted chunks to plaintext chunks
		
def decrypt4b(bits4array) :
		'''
				Fully encrypts (16 decryptit iterations) a block.
				bits4array is a single block of plaintext.
		'''
		answer = bits4array
		for i in range(16) :
				answer = decryptit(answer)
		return answer

def decrypt(cipher, nonce) :
		'''
		Encrypts a message, using cipher block chaining.
		nonce is the random 16-bit number (expressed as a list of two bytes).
		message is a list of bytes to be encrypted.
		'''
		cipher = [to4bitarray(c) for c in package(cipher)] #get cipher text in chunked form.
		plain = [] #the answer.
		i = 0
		for d in cipher : #for each block (a list of chunks)
				p = tobytesarray(decrypt4b(d)) #decrypt the block
				p = [p[0] ^ nonce[0], p[1] ^ nonce[1]] #xor the decrypted block with the nonce
				plain.append(p) #append to the end of the plaintext.
				nonce = tobytesarray(cipher[i]) #update the nonce to be the most recently decrypted ciphered block
				i += 1
		return unpackage(plain) #return answer as a list of bytes.
		
def main() :
		filename = "" #the name of the file to decrypt
		direction = "" #the direction: "E" for encrypt, "D" for decrypt.
		if len(sys.argv) < 2 : #if no command line args are used, use input.
				direction = input("(E)ncrypt or (D)ecrypt? ")
				filename = input("Enter file name: ")
		else : #use command line args.
				direction = sys.argv[1]
				filename = sys.argv[2]
		
		if direction == "E" : #encryption code.
				f = open(filename, "r") #open the plaintext for reading.
				nonce = [int(random.random() * 256), int(random.random() * 256)] #generate nonce.
				print("Original nonce:", nonce)
				cipher = encrypt(f.read().encode(), nonce) #encrypt the plaintext encoded into bytes.
				print(cipher)
				f.close() #close reading file.
				f = open(filename + ".encrypted", "wb") #open encrypted file for writing.
				f.write(nonce[0].to_bytes(8, "big")) #write the nonce at the beginning of the file.
				f.write(nonce[1].to_bytes(8, "big")) #write the nonce at the beginning of the file.
				f.write(bytes(cipher)) #write the cipher (as bytes)
				f.close() #close the encrypted file.
		elif direction == "D" :
				f = open(filename, "rb") #open the encrypted file.
				nonce = [int.from_bytes(f.read(8), "big"), int.from_bytes(f.read(8), "big")] #read nonce
				cipher = f.read() #read the ciphertext.
				plain = decrypt(cipher, nonce) #decrypt the ciphertext.
				plaintext = "" #convert plaintext to string.
				for p in plain : #loop for conversion
						plaintext += chr(p) #char by char conversion
				f.close() #close encrypted file
				f = open(filename + ".decrypted", "w") #open plaintext file for writing.
				f.write(plaintext) #write plaintext.
				f.close() #close plaintext file.
				

if __name__ == "__main__" :
		main()

print("############## DEMO ##############")
print("\t(demo is printed regardless of what happens with files above)")
print("encrypting and decrypting \"test messages\"")
cipher = encrypt(bytes("abcde", "ascii"), [23, 108]) #encrypt "test messages"
print("ciphertext: ", cipher) #print the ciphertext (may not print entirely).
plain = decrypt(cipher, [23, 108]) #decrypt the cipher text.
plaintext = "" #convert bytes to chars.
for p in plain : #loop for conversion
		plaintext += chr(p) #convert char by char
print("plaintext: ", plaintext) #print decrypted message.
print("############## END  ##############")