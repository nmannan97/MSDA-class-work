import hashlib

class HashFunction:
    def __init__(self):
        self.user_db = {}  # Dictionary to store user passwords as hashes

    def getHashValue(self, message, hash_type):
        hash_type = hash_type.upper()
        if hash_type == 'MD5':
            return hashlib.md5(message.encode()).hexdigest()  # 32-character hexadecimal
        elif hash_type == 'SHA256':
            return hashlib.sha256(message.encode()).hexdigest()  # 64-character hexadecimal
        else:
            print("Did not find the algorithm to produce the hash value. Possible types are MD5/SHA256")
            return None

    def register_user(self, username, password):
        """Stores the hashed password in the user database."""
        hash_password = self.getHashValue(password, 'SHA256')  # Using SHA256 for security
        self.user_db[username] = hash_password
        print(f"User {username} registered successfully.")

    def login_user(self, username, password):
        """Compares hashed password for authentication."""
        hash_password = self.getHashValue(password, 'SHA256')
        stored_password = self.user_db.get(username)
        
        if stored_password and stored_password == hash_password:
            print("Login successful!")
        else:
            print("Login failed! Invalid username or password.")


def hashComputation():
    hashObj = HashFunction()
    
    # Register users
    hashObj.register_user("user1", "password123")
    hashObj.register_user("user2", "securePass!@#")
    
    # Attempt login
    hashObj.login_user("user1", "password123")  # Should succeed
    hashObj.login_user("user2", "wrongPass")  # Should fail
    hashObj.login_user("unknown_user", "password123")  # Should fail
    print(hashObj.user_db)

if __name__ == "__main__":  
    hashComputation()
