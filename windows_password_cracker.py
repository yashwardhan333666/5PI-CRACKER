import hashlib
import codecs
import os
from urllib.request import urlopen

global guesspasswordlist
guesspasswordlist = []

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
        input()
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
			# If the password is found then it will terminate the script here
			input()
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

>> """))

def local():

	global actual_password_hash
	global guesspasswordlist_path
	global hash_type
	encodee = ''
	guesspasswordlist = []
	actual_password_hash = input("\nEnter hash\n\n>> ")
	actual_password_hash = actual_password_hash.strip()
	askhash()
	guesspasswordlist_path = input("\nEnter wordlist path\nPlease give the Full Path, unless the wordlist is in the same folder as this script\n\n>> ")
	guesspasswordlist_path = guesspasswordlist_path.strip()
	# enc = int(input("\nIs the encoding\n1) Ascii.\n2) UTF-8.\n\n>> "))

	# if enc == 1:
	# 	encodee = 'ascii'
	# elif enc == 2:
	# 	encodee = 'utf-8'
# , encoding=encodee
	try:
	    guesspasswordlistfile = codecs.open(guesspasswordlist_path, mode='r', errors='ignore', buffering=-1)
	except Exception as error:
	    print("\nThere was an error while reading the wordlist ->", error)
	    input()
	    exit()

	print("\nProcessing Wordlist.\nTime taken will depending upon the length of the wordlist.\n ")

	for linee in guesspasswordlistfile:
		word = linee
		guesspasswordlist.append(word[:-1]) 
	guesspasswordlistfile.close()

	print('\nBruteforcing now\n')
	bruteforce(guesspasswordlist, actual_password_hash)

def online():
	global actual_password_hash
	global hash_type

	actual_password_hash = input("\nEnter password hash\n\n>> ")
	actual_password_hash = actual_password_hash.strip()
	askhash()
	url = input("\nEnter url.\nIt should be a raw file ending in .txt\nExample - https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt\n\n>> ")
	url = url.strip()
	print("\nProcessing Wordlist.\nTime taken will depending upon the length of the wordlist and your internet connection\n ")
	wordlist = readwordlist(url).decode('UTF-8')
	guesspasswordlist = wordlist.split('\n')

	print('\nBruteforcing now\n')
	bruteforce(guesspasswordlist, actual_password_hash)

print("Welcome to 5PICRACKER")
print("Solve hashes super quick. Don't have a large wordlist locally saved? No isses :) ")

check_online = int(input("""\nIs your wordlist text file

1) Locally saved
2) Online (Generally Faster)

>> """))

if check_online == 1:
	local()
elif check_online == 2:
	online()

os.system('cls')
print("""
Failed. The reasons are given below

1) If you were cracking locally, the relavent password is not in the wordlist provided, try again with another wordlist.

2) If you were cracking online

 A) If you immediately got this message, then the url is not a raw word list.
 B) Check your internet connection.
 C) If you did not get the fail immediately, then the password is not in the wordlist provided. Try again with another list.

3) For both Local and Online (consider this only if you have tried multiple large wordlists)

The hash you picked must be unsupported by your python or hashlib version.
Check and update accordingly -  https://docs.python.org/3/library/hashlib.html#hash-algorithms

""")

input("Press enter to continue")

#End of Code