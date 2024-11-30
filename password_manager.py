from cryptography.fernet import Fernet
import os

# Function to generate and save encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the encryption key
def load_key():
    return open("secret.key", "rb").read()

# Function to encrypt a password
def encrypt_password(password, key):
    f = Fernet(key)
    encrypt_password = f.encrypt(password.encode())
    return encrypt_password

# Function to decrypt a password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Main function
def main():
    if not os.path.exists("secret.key"):
        generate_key()

    key = load_key()

    while True:
        print("\nPassword Manager Menu")
        print("1. Add Password")
        print("2.View Passwords")
        print("3. Exit")
        choice = input("Choose and option: ")

        if choice == '1':
           website = input("Enter the website: ")
           username = input("Enter the username: ")
           password = input("Enter the password: ")
           enc_password = encrypt_password(password, key)

           with open("passwords.txt", "a") as f:
               f.write(f"{website},{username},{enc_password.decode()}\n")

           print("Password saved!")

        elif choice == '2':
            if not os.path.exists("passwords.txt"):
                print("No password stored yet.")
            else:
                with open("passwords.txt","r") as f:
                    for line in f:
                        parts = line.strip().split(',')
                        if len(parts) == 3:
                          website, username, enc_password = parts
                          password = decrypt_password(enc_password.encode(), key)
                          print(f"Website: {website}, Username: {username}, Password: {password}")
                        else:
                            print("Skipping invalid line:", line)
                    

        elif choice == '3':
            print("Exiting Password Manger.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()