notconverted = ' \n.,\"\'()='
def caesar(sample, key):
		sample = sample.lower()
		converted = ''
		for i in sample:
			if i in notconverted:
				converted += i
				continue
			converted+=chr((ord(i)+key-97)%26 + 97)
		return converted

def check(sample):
		wordFile = open('/usr/share/dict/words')
		wordList = wordFile.read().split('\n')
		sampleWordList = sample.split(' ')
		wordCount = len(sampleWordList)
		validWords = 0
		for word in sampleWordList:
			if word in wordList:
				validWords+=1
		if validWords > wordCount/2:
			return True
		return False


def crack(sample):
		for i in range(0,26):
				temp = caesar(sample,i)
				if check(temp):
					return i,temp
		return None

def main():
	sample = raw_input('Enter cipher : ')
	k = crack(sample)
	if k==None:
		print "Crack failed"
	else:
		print 'Key = ',26 - k[0]
		print 'Plaintext = ',k[1]

main()
