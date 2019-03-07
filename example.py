#!/usr/bin/python
__author__ = "Anneke Smitheram"

from random import shuffle
from greedy import Collection

fragmentedCollection = (["ve you", "give", "you up",
	"never", "eve", "r gonna g"])
shuffle(fragmentedCollection)
collection = Collection(fragmentedCollection)

print("-----------")
print("Fragmented Collection: " + str(collection.values))

collection.greedyMatchAndMerge()

print("After Greedy Match and Merge: " + str(collection.values))
print("-----------")