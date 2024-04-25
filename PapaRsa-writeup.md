## Papa RSA Writeup

**Challenge Authors**: Het Patel(Y20) and Ritvik Goyal(Y22)

---

Challenge Source File which was given:

```python
from Crypto.Util.number import bytes_to_long, getPrime

def encrypt_message(message):
    m = bytes_to_long(message)
    p = getPrime(1024)
    q = getPrime(1024)
    N = p * q
    e = 3
    c = pow(m, e, N)
    return N, e, c

# 30 messages
messages = [?????]


message_index = input("Enter the index of the message you want (0-29): ")
try:
    message_index = int(input_data)
    if 0 <= message_index < NumofMess:
        selected_message = messages[message_index]
        N, e ,c = encrypt_message(selected_message)
        client_socket.send(b"Encrypted Message: \n")
        message = {"N":N,"e":e,"ciphertext":c}
        message = json.dumps(message)
        client_socket.send(message.encode())
        client_socket.send(b"\n")
    else:
        client_socket.send(b"Invalid index. Please enter a number between 0 and 29.\n")
except ValueError:
    client_socket.send(b"Invalid input. Please enter a number.\n")
```

Server is encrypting every message with e = 3 and p , q of 1024 bits prime which definitely can't be fractorise with current factor algos in small time.

e = 3 make it easy to do cube root the cipher test only if  
x<sup>3</sup> = x<sup>3</sup> mod N
but as the challenge was designed such a way that message length > 100 which make  M<sup>3</sup> mod (N) != M<sup>3</sup>.  

So here Chinese Remainder Theorem come into play !!
See Hastad's Broadcast Attack on Page 208   
[Twenty Years of Attacks on the RSA Cryptosystem](https://www.ams.org/notices/199902/boneh.pdf)

As there is no limit on how many times we encrypt the message this attack works.  
We are going to encrypt every message 3-4 times . and then apply Chinese Remainder Theorem ,   
C<sub>1</sub> = M<sup>3</sup> (mod N<sub>1</sub>)   
C<sub>2</sub> = M<sup>3</sup> (mod N<sub>2</sub>)   
C<sub>3</sub> = M<sup>3</sup> (mod N<sub>3</sub>)   

Then CRT will give us,   
C = M<sup>3</sup> (mod (N<sub>1</sub>\*N<sub>2</sub>\*N<sub>3</sub>)))   
and as M<sup>3</sup> will get smaller than (N<sub>1</sub>\*N<sub>2</sub>\*N<sub>3</sub>) finally, if not then we consider 4 equations.    
Then Simple Cube root of C will give the Cipher text.

Code for decryption is as follows:
```python
# ! pip install pyCryptodome
# ! pip install gmpy2
from itertools import combinations
from Crypto.Util.number import inverse , isPrime , long_to_bytes
from gmpy2 import iroot

messages = [(n1,3,c1),(n2,3,c2),(n3,3,c3),(n4,3,c4)]
x = iroot(messages[0][0],3)[0]
print(long_to_bytes(x)) # As this will not decrypt the flag
for comb in combinations(messages,4):
  sum =0
  N =1
  for i in comb:
    n , e, ct = i[0], i[1], i[2]
    N *= n
  for i in comb:
    n , e, ct = i[0], i[1], i[2]
    sum += (ct*(N//n)*(inverse(N//n,n)))
  sum %= N
  x , exact = iroot(sum,3)
  if exact:
    print(long_to_bytes(x).decode())
 ```
For connecting to the binary, you can use [Pwntools](https://github.com/Gallopsled/pwntools)

Hence here our flag :
pclub{rsa_is_not_easier_than_you_think_but_if_ur_well_equipped_with_mathematics_you_can_solve_any_rsa_problem_just_like_you_did_this_one_keep_decrypting_messages_sharn_ctf_lessgo}

