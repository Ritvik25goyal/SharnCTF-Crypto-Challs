## Papa RSA Writeup

**Challenge Authors**: Het Patel(Y20) and Ritvik Goyal(Y22)

---

Challenge Source File which was given:
```python
import random
import hashlib
from Crypto.Util.number import bytes_to_long , long_to_bytes
from Crypto.Cipher import AES

flag = b"Redacted Flag"
p = 93576037242746035035473867525061528770699004259621835804706054919620431867384593570762571145024654596138800886191166013690519482839454556118280586882046257401523288037480820562710115034130518166976813626453105737758796190609809841257608490608130876515174748404405126112466055935640736486247486137965941288359
secret = b"Redacted Secret"
key = hashlib.sha256(secret[:16]).digest()[:16]
cipher = AES.new(key, AES.MODE_ECB)
padded_flag = flag + b'\x00'*(-len(flag)%16)
ciphertext = cipher.encrypt(padded_flag)
print(f"Ciphertext: {ciphertext.hex()}\n\n")
print(pow(bytes_to_long(secret),2,p))

# Ciphertext: 478419f4c39e20c12772470a3bc4545066eb3d71ddb0721886bc866c148680411a5767347c8ba81003ac52f8a873cff4
# Output: 1253374543256850702638941421606
```

The code was doing secret<sup>2</sup> (mod p).   
[Quadratic Residue Wiki](https://en.wikipedia.org/wiki/Quadratic_residue)    
The Legendre Symbol gives an efficient way to determine whether an integer is a quadratic residue modulo an odd prime p.

Legendre's Symbol: (a / p) ≡ a<sup>(p-1)/2</sup> mod p obeys:
```
(a / p) = 1 if a is a quadratic residue and a ≢ 0 mod p
(a / p) = -1 if a is a quadratic non-residue mod p
(a / p) = 0 if a ≡ 0 mod p
```
calculate the legendres symbol :
```python
>>> a = 1253374543256850702638941421606
>>> p = 93576037242746035035473867525061528770699004259621835804706054919620431867384593570762571145024654596138800886191166013690519482839454556118280586882046257401523288037480820562710115034130518166976813626453105737758796190609809841257608490608130876515174748404405126112466055935640736486247486137965941288359
>>> pow(a,(p-1)//2,p)
1
```
So residue does exist.

Now as p = 3 (mod 4),
[3mod4 prime residue](https://crypto.stackexchange.com/questions/20993/significance-of-3mod4-in-squares-and-square-roots-mod-n/20994#20994)

```python
>>> import hashlib
>>> from Crypto.Util.number import long_to_bytes
>>> p%4
3
>>> secret = pow(a,(p+1)//4,p)
>>> secret
58517767920011569596136114279494082332629843727082536879606938183128470918193793153713924217472098113969299754237756517438800352968598378883811243817411444538439814658571312062031228147793343107299110461467715057881690367873619551874256849134631253532237273072668197747356634822477079350257811205102008446671
>>> secret = long_to_bytes(secret)
>>> key = hashlib.sha256(secret[:16]).digest()[:16]
>>> cipher = AES.new(key, AES.MODE_ECB)
>>> ciphertext = int("478419f4c39e20c12772470a3bc4545066eb3d71ddb0721886bc866c148680411a5767347c8ba81003ac52f8a873cff4",16)
>>> ciphertext
11007323066017732254112028948687434672676395830872967468196398866706698928824955835858484870898504802569889319735284
>>> cipher.decrypt(long_to_bytes(ciphertext))
b'pclub{legendre_lagrangian_type_shit}\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
```

Hence we got our flag: 
pclub{legendre_lagrangian_type_shit}