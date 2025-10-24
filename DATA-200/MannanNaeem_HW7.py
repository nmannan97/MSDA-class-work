class hashFunction:
    def __init__(self):
       pass

    def getHashValue(self,message,type):
        if type.upper() == 'MD5':
           pass
          #32 exadecimal character 
          # nibbles 128/4 = 32 which means .5 byte or 4 bit?
          # This approach is not collision free
        elif type.upper() == 'SHA256':
           pass
           # 64 bit long
           # This is deterministic i.e. if the input is same then the output is same
           # It is extermly hard to generate the key from hash value, it is a trap door function
           # This is the way you identify the block in a block chain
        else:
            print("Did not find the algo to produce the hash value. Possible types are MD5/SHA256")
            
    ### Is it possible????
    def getHashKey(self,message,type):
        if type.upper() == 'MD5':
            pass
        elif type.upper() == 'SHA256':
          pass
        else:
            print("Did not find the algo to produce the hash key. Possible types are MD5/SHA256")

    

def hashComputation():
    hashObj=hashFunction()
    message1="Hello You dere!"


if __name__ == "__main__":  
    hashComputation()
    