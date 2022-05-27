#!/usr/bin/python3
# Script works on both linux and windows. The only thing that does not workn in windows is checking the file encoding if the wordlist is local

import hashlib
import codecs
import os
from urllib.request import urlopen

global guesspasswordlist
guesspasswordlist = []

global skip
skip = 0

global guesspasswordlist_path
guesspasswordlist_path = ''

global actual_password_hash
actual_password_hash = ''

global hash_type
hash_type = 0

def readwordlist(url):
    try:
        wordlistfile = urlopen(url).read()
    except Exception as error:
        print("\nThere was an error while reading the wordlist ->", error)
        exit()
    return wordlistfile
 
def hash(wordlistpassword):
	global hash_type

	# You can view the Hashing Algos that hashlib supports in the given link
	# https://docs.python.org/3/library/hashlib.html#hash-algorithms
	# To change the algorithm, edit the line below
	# Also, i could have added an option to pick the algo during runtime, but for some reason, python kept on giving me an indentation error. I had no idea what was causing the error.
	try:
		if hash_type == 0:
			result = hashlib.md5(wordlistpassword.encode())
			return result.hexdigest()
		elif hash_type == 1:
			result = hashlib.sha1(wordlistpassword.encode())
			return result.hexdigest()
		elif hash_type == 2:
			result = hashlib.sha224(wordlistpassword.encode())
			return result.hexdigest()
		elif hash_type == 3:
			result = hashlib.sha256(wordlistpassword.encode())	
			return result.hexdigest()
		elif hash_type == 4:
			result = hashlib.sha384(wordlistpassword.encode())
			return result.hexdigest()
		elif hash_type == 5:
			result = hashlib.sha512(wordlistpassword.encode())
			return result.hexdigest()
		elif hash_type == 6:
			result = hashlib.sha3_224(wordlistpassword.encode())
			return result.hexdigest()
		elif hash_type == 7:
			result = hashlib.sha3_256(wordlistpassword.encode())
			return result.hexdigest()
		elif hash_type == 8:
			result = hashlib.sha3_384(wordlistpassword.encode())
			return result.hexdigest()
		elif hash_type == 9:
			result = hashlib.sha3_512(wordlistpassword.encode())
			return result.hexdigest()
		# elif hash_type == 10:
		# 	result = hashlib.shake_128(wordlistpassword.encode())
		# 	return result.hexdigest(256)
		# elif hash_type == 11:
		# 	result = hashlib.shake_256(wordlistpassword.encode())
		# 	return result.digest(512)
	except Exception as error:
		print("\nHad an error while processing -> ",error)
	
def bruteforce(guesspasswordlist, actual_password_hash):
	for guess_password in guesspasswordlist:
		if hash(guess_password) == actual_password_hash:
			print("\nYour password is:", guess_password)
			exit()

def askhash():
	global hash_type
	hash_type = int(input("""\nWhat pick your password hash type

0)  md5
1)  sha1
2)  sha224
3)  sha256
4)  sha384
5)  sha512
6)  sha3_224
7)  sha3_256
8)  sha3_384
9)  sha3_512
10) shake_128 [Under dev]
11) shake_256 [Under dev]
12) [adding more ...]

>> """))

def local():
	global skip
	global actual_password_hash
	global guesspasswordlist_path
	global hash_type
	encodee = ''
	guesspasswordlist = []
	if skip == 0:
		actual_password_hash = input("\nEnter hash\n>> ")
		askhash()
		guesspasswordlist_path = input("\nEnter wordlist path\nPlease give the Full Path, unless the wordlist is in the same folder as this script\n\n>> ")
	enc = int(input("\nIs the encoding\n1) Ascii.\n2) UTF-8.\n3) Check\n\n>> "))

	if enc == 1:
		encodee = 'ascii'
	elif enc == 2:
		encodee = 'utf-8'
	elif enc ==3:
		skip = 1
		os.system(f'file {guesspasswordlist_path}')
		input()
		local()

	try:
	    guesspasswordlistfile = codecs.open(guesspasswordlist_path, mode='r', encoding=encodee, errors='ignore', buffering=-1)
	except Exception as error:
	    print("\nThere was an error while reading the wordlist ->", error)
	    exit()

	print("\nProcessing Wordlist.\nTime taken will depending upon the length of the wordlist.\n ")

	for linee in guesspasswordlistfile:
		word = linee
		guesspasswordlist.append(word[:-1]) 
	guesspasswordlistfile.close()

	print('\nBruteforcing now\n')
	bruteforce(guesspasswordlist, actual_password_hash)

def online():

	# Preferred wordlists -> https://github.com/danielmiessler/SecLists/tree/master/Passwords/Common-Credentials
	# Enter the raw.github.com url while executing
	# For Example -> https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt
	
	actual_password_hash = input("\nEnter password hash\n\n>> ")
	askhash()
	url = input("\nEnter url.\nIt should be a raw file ending in .txt (head over to line 87 inside the script for more info)\n\n>> ")
	print("\nProcessing Wordlist.\nTime taken will depending upon the length of the wordlist and your internet connection\n ")
	wordlist = readwordlist(url).decode('UTF-8')
	guesspasswordlist = wordlist.split('\n')

	print('\nBruteforcing now\n')
	bruteforce(guesspasswordlist, actual_password_hash)

print("Welcome to the Bare-Bones Password Cracker by 5PID3RH7CK3R")
print("There have been some measures taken to avoid script-kiddie abuse. Script settings are within the code itself.\nWherever you see comments, you can read through and edit accordingly.")


check_online = int(input("""\nIs your wordlist TEXT file

1) Locally saved
2) Online (Suggested)

>> """))

if check_online == 1:
	local()
elif check_online == 2:
	online()

print("\nFailed. The reasons are given below\n")
print("\n If you were cracking locally\n\nA) Check the wordlist encoding.\n\nB) The relavent password is not in the wordlist provided, try again with another wordlist. \n")
print("\n If you were cracking online\n\nA) If you immediately got this message, then the url is not a raw text file.\nCheck line 144 in the script for more info and example url.\n\nB) If you did not get the fail immediately, the the password is not in the wordlist provided. Try again with another list")
print("\n OR the hash you picked must be unsupported by your python or hashlib version.\nCheck and update accordingly -  https://docs.python.org/3/library/hashlib.html#hash-algorithms\n")

#End of Code
