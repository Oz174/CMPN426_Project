# CMPN426 - Project

## Team Members

1. Ahmed Tarek Abdellatif 1190157

2. Kareem Yasser Ali Ragab 1190175

3. Nada Hesham Anwer Hussien 1190185

4. Mahmoud Khaled Mahmoud 1190141

## How to Run ?

- Open the first terminal and run the receiever script first

```sh
python receiver.py
```

- Open a second terminal and run the sender script

```sh
python sender.py
```

- To end chat , send an empty message ( press enter only)

## How does it work ?

1. Each of Alice (sender) and Bob (receiver) starts by calculating there DH and Algamal Pairs of Keys
2. They exchange Algamal public keys (each one's has its own seed for generating the keys to ensure randomness and also a consistent key)
3. They verify the signature with each one's DH public key as a Message M hashed by SHA1
4. If the signature is not verified , the chat is terminated
5. Otherwise, they generate a unified key using SHA256 for AES.mode_ECB
6. chat continues

## Testcases

- Invalid Signature test (By manipulating C1,C2 received or sent) -> exits the chat
- Different key used for decoding -> chat ends
