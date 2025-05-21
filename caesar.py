notconverted = ' \n.,\"\'()=0123456789!' # Added digits and !
def caesar(sample, key):
    sample = sample.lower()
    converted = ''
    for i in sample:
        if i in notconverted:
            converted += i
            continue
        converted+=chr((ord(i)+key-97)%26 + 97)
    return converted

def check(sample, dictionary_path=None): # Corrected signature
    word_file_path = dictionary_path if dictionary_path else '/usr/share/dict/words'
    try:
        with open(word_file_path) as wordFile:
            wordList = wordFile.read().splitlines()
    except FileNotFoundError:
        if dictionary_path: # A custom path was given but not found
            raise
        else: # Default path not found
            # This case should be handled by the test_default_dictionary_not_found
            # For now, let it print and return False as per original partial instructions
            # but the test expects it to just return False without printing if it can't find default
            # print(f"Error: Default dictionary {word_file_path} not found.")
            return False
    sampleWordList = sample.split(' ')
    # Filter out empty strings that can result from multiple spaces
    sampleWordList = [word for word in sampleWordList if word]
    wordCount = len(sampleWordList)
    if wordCount == 0: # Handle empty string or string with only spaces
        return False
    validWords = 0
    for word in sampleWordList:
        if word in wordList: # Check against the loaded wordList
            validWords+=1
    if validWords * 2 > wordCount: # check if validWords > wordCount / 2
        return True
    return False


def crack(sample, dictionary_path=None): # Modified signature
    for i in range(0,26):
        temp = caesar(sample,i)
        # Pass the dictionary_path to check
        if check(temp, dictionary_path=dictionary_path): 
            return i,temp
    return None

def main():
    sample = input('Enter cipher : ')
    k = crack(sample)
    if k==None:
        print("Crack failed")
    else:
        print('Key = ', 26 - k[0])
        print('Plaintext = ', k[1])

if __name__ == '__main__':
    main()
