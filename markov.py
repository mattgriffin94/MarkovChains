from random import choice
people = {}

class Person(object):
  
  def __init__(self,file,name):
    people[name] = self
    self.name = name
    self.data = open(file).read().lower()
    #For simplicity sake, remove punctuations except for periods (which denote end of sentences).
    self.data = self.data.replace("/","").replace("-"," . ").replace("--"," . ").replace("\"","").replace("\'","").replace(";",".").replace(":","").replace("."," . ").split()
    self.cache = {} #map previous word to tuple of next words
    self.cache2 = {} #map previous two words to tuple of next words
      
    #map previous word to tuple of nexxt words
    prev = "."
    for word in self.data:
      if prev in self.cache:
        self.cache[prev] = self.cache[prev] + (word,)
      else:
        self.cache[prev] = (word,)
      prev = word

    #map previous two words to tuple of next words
    prev1 = "."
    prev2 = "."
    for word in self.data:
      if (prev1,prev2) in self.cache2:
        self.cache2[(prev1,prev2)] = self.cache2[(prev1,prev2)] + (word,)
      else:
        self.cache2[(prev1,prev2)] = (word,)
      prev1 = prev2
      prev2 = word
  


  def makeSent(self,word):
    word = word.lower()
    if word not in self.cache: word = "the" #if the topic isn't in the dictionary, defualt to the
    result = word
    
    if(len(result.split()) == 1):
      word = choice(self.cache[word]) #choose randomly from the next words possible.  Note that this will be weighted to choose the most common follow up words because you could have something like "the": ("cat","cat","cat", "dog",)
      result = result + " " + word
    
    while word[-1] != ".":
      
      if((result.split()[-2],word) in self.cache2): # prioritize the two word cache
        word = choice(self.cache2[(result.split()[-2],word)])
        result = result + " " + word
      else:
        word = choice(self.cache[word])
        result = result + " " + word
    return result


def main():

  print("Fake Conversations")
  name1 = input("What is the name of the first person? ")
  file1 = input("Where is the data file for " + name1 + "? ")
  name2 = input("What is the name of the second person? ")
  file2 = input("What is the data file for " + name2 + "? ")
  topic = input("What should the conversation be about? ")
  num = int(input("How long should the conversation be? "))

  p1 = Person(file1,name1)
  p2 = Person(file2,name2)
  
  for i in range(num):
    x = p1.makeSent(topic)
    print(p1.name +": ")
    print(x)
    if(i!=0): topic = x.split()[-2]
    r = p2.makeSent(topic)
    print(p2.name +": ")
    print(r)
    topic = r.split()[-2]


if __name__ == "__main__":
  main()