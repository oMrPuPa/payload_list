def decrypt(cipherText):
    for i in range(1,26):
        hasil=''
        for j in range(len(cipherText)):
            cipherChar = (((ord(cipherText[j].upper())-65) - i) % 26) + 65
            hasil+=chr(cipherChar)
        print(hasil)

def main():
    cipherText = input("input text caesar subnya: ")
    decrypt(cipherText)

if __name__ == "__main__":
    main()