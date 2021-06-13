from BitHash import BitHash
from BitVector import BitVector

class BloomFilter(object):
    # Return the estimated number of bits needed (N in the slides) in a Bloom 
    # Filter that will store numKeys (n in the slides) keys, using numHashes 
    # (d in the slides) hash functions, and that will have a
    # false positive rate of maxFalsePositive (P in the slides).
    # See the slides for the math needed to do this.  
    # You use Equation B to get the desired phi from P and d
    # You then use Equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        #Here I calculate phi
        phi = 1 - (maxFalsePositive) ** (1/numHashes)
        
        #here I calculate the number of bits needed
        bitsNeeded = numHashes/(1 - phi ** (1/numKeys))
        
        #I turn this number into an int
        bitsNeeded = int(bitsNeeded) 
        
        #now I return the number of bits needed
        return bitsNeeded   
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        # In addition to the BitVector, might you need any other attributes?
        
        #count the keys
        self.__numKeys = numKeys
        
        #count the hashes
        self.__numHashes = numHashes
        
        #keep track of the false positive rate
        self.__maxFalsePositive = maxFalsePositive 
        
        #N
        self.__numBits = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        
        #create the bit vector
        self.__bitVector = BitVector(size = self.__numBits)
        
        #count the bits 
        self.__bitCount = 0
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    # See the "Bloom Filter details" slide for how insert works.
    def insert(self, key):
        #set a variable to keep track of where I'm hashing
        a = 0 
        
        #insert the key into the vector numHashes times 
        for i in range(self.__numHashes): 
            #number from bithash function
            hash = BitHash(key, a)
            
            #position in bitvector 
            num = hash % self.__numBits
            
            #check if the bit has been set
            if self.__bitVector[num] == 0: 
               
                #it has not been set so set it
                self.__bitVector[num] = 1
                
                #update the amount of bits we've set
                self.__bitCount += 1 
            
            #now update the hash positions for the next insertion    
            a = hash    
            
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    # See the "Bloom Filter details" slide for how find works.
    def find(self, key):
        
        #set a variable to keep track of where I'm hashing
        a = 0 
        
        #attempt to find the key numHashes amount of times
        for i in range(self.__numHashes): 
            
            #find the position where the key can be found
            hash = BitHash(key, a)
            
            #update the position
            a = hash
            
            #position in bit vector
            num = hash % self.__numBits
            
            #now check if the position has been set
            if self.__bitVector[num] == 0: 
                #it hasn't been set so it definitely has not been inserted
                return False 
        
        #it has probably been inserted    
        return True  
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        #Calulate the projected false positive rate
        phi = (1 - (self.__numHashes/self.__bitCount)) ** (self.__numKeys)
        P = (1 - phi) ** self.__numHashes 
        return P
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    #Keep track of how many bits are still set 
    def numBitsSet(self):
        #return how many bits we've set
        return self.__bitCount 

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalsePositive = .05
    
    # create the Bloom Filter
    b = BloomFilter(numKeys, numHashes, maxFalsePositive) 
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    file = open("wordlist.txt")
    line = file.readline()
    numLines = 1
    while numLines <= numKeys: 
        b.insert(line) 
        numLines += 1 
        line = file.readline()
    file.close()
        
    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    print("The projected false positive rate:", b.falsePositiveRate()) 

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file.
    file = open("wordlist.txt")
    line = file.readline()
    numLines = 1
    notFound = 0
    while numLines <= numKeys: 
        if b.find(line) == False: 
            notFound += 1 
        numLines += 1 
        line = file.readline()
    
    print(notFound, "bits are missing") 
    
    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    found = 0
    while numLines <= numKeys * 2: 
        if b.find(line) == True: 
            found += 1 
        numLines += 1 
        line = file.readline()   
    
    print(found, "bits are falsley found") 
    file.close()
    # Print out the percentage rate of false positives.
    falsePositiveRate = found / numKeys 
    print("The actual false positive rate is:", falsePositiveRate)
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE

    
if __name__ == '__main__':
    __main()       

