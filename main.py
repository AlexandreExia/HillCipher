from hill import Hill
import alphabet

if __name__ == "__main__":

    while(True):
        sentence = input("Enter the message to (de)crypt: ").lower()
        mode = input("Do you want to Encrypt (E) or Decrypt(D) the previous message? ")
        key = input("Enter the matrix (format: a b; c d) : ")
        alphabet.offset = int(input("A=0 or A=1 ? "))

        hill = Hill(key)

        if not hill.key.is_valid():
            print("The key does not respect Hill format")
            exit()

        if mode == 'E':
            print("Crypted message : " + hill.encrypt(sentence))
        elif mode == 'D':
            print(hill.decrypt(sentence))

        stop = input("Do you want continue ? (Y/N) ")

        if(stop == 'N'):
            exit()