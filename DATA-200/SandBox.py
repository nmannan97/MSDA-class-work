import hashlib

class HashFunction:
    def __init__(self):
        pass

    def getHashValue(self, message, hash_type):
        hash_type = hash_type.upper()
        if hash_type == 'MD5':
            return hashlib.md5(message.encode()).hexdigest()  # 32-character hexadecimal
        elif hash_type == 'SHA256':
            return hashlib.sha256(message.encode()).hexdigest()  # 64-character hexadecimal
        else:
            print("Did not find the algorithm to produce the hash value. Possible types are MD5/SHA256")
            return None

    def getHashKey(self, message, hash_type):
        """
        The function generates a hash key using the specified algorithm.
        Note: Hash functions are one-way functions, and you cannot retrieve the original message from the hash.
        """
        return self.getHashValue(message, hash_type)


def hashComputation():
    hashObj = HashFunction()
    message1 = "Hello You dere!"
    
    print("MD5 Hash:", hashObj.getHashValue(message1, 'MD5'))
    print("SHA256 Hash:", hashObj.getHashValue(message1, 'SHA256'))

    print("MD5 Key:", hashObj.getHashKey(message1, 'MD5'))
    print("SHA256 Key:", hashObj.getHashKey(message1, 'SHA256'))


if __name__ == "__main__":  
    hashComputation()
