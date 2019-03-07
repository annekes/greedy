#!/usr/bin/python

"""greedy.py supplies tools to run a greedy match and merge
algorithm on a simplified fractured list
"""

__author__ = "Anneke Smitheram"

from enum import Enum, auto

class Position(Enum):
	"""Identify where overlap occurs."""
	IN_FRAGMENT_1 = auto()
	IN_FRAGMENT_2 = auto()
	FRONT_FRAGMENT_1 = auto()
	FRONT_FRAGMENT_2 = auto()
	NO_OVERLAP = auto()

class Fragment:
	"""Supports finding a match between fragments.

	Attributes:
		value (str) -- value of fragment
		length (int) -- length of fragment
	"""

	def __init__(self, value):
		self.value = value
		self.length = len(value)

	def __getStart(self, lengthOfOverlap):
		return self.value[0:lengthOfOverlap]

	def __getEnd(self, lengthOfOverlap):
		return self.value[self.length-lengthOfOverlap:self.length]

	def getMatchForFragment(self, other, prevOverlapLength):
		"""Find longest overlap with other Fragment and return Match.

		Arguments:
			other (Fragment) -- the Fragment to find overlap with
			prevOverlapLength (int) -- the overlap length to skip
		"""

		# Check if self contains other and return Match
		if self.length > other.length:
			if self.value.find(other.value) >= 0:
				return Match(self, other, other.value,
					Position.IN_FRAGMENT_1)
			else:
				overlap = ""

			maxOverlapLength = other.length

		# Check if other contains self and return Match
		else :
			if (other.value.find(self.value) >= 0):
				return Match(self, other, self.value,
					Position.IN_FRAGMENT_2)
			else:
				overlap = ""

			maxOverlapLength = self.length

		# Finds longest overlap by comparing start and end of fragments
		# if no better overlap found, return Match with empty overlap
		position = Position.NO_OVERLAP
		if not overlap:
			# As opposed to starting at 0,
			# start at prevOverlapLength to reduce run time
			# and skip entirely if fragment is too short
			for l in range(prevOverlapLength, maxOverlapLength):
				if self.__getStart(l) == other.__getEnd(l):
					overlap = self.__getStart(l)
					position = Position.FRONT_FRAGMENT_1

				elif other.__getStart(l) == self.__getEnd(l):
					overlap = other.__getStart(l)
					position = Position.FRONT_FRAGMENT_2

		return Match(self, other, overlap, position)

class Match:
	"""Fragments and the overlap properties.

	Attributes:
		fragment1 (Fragment) -- the first Fragment
		fragment2 (Fragment) -- the second Fragment
		overlap (str) -- the overlap between fragments
		length (int) -- the length of overlap
		position (Position) -- the position of overlap in fragments
	"""

	def __init__(self, fragment1, fragment2, overlap, position):
		self.fragment1 = fragment1
		self.fragment2 = fragment2
		self.overlap = overlap
		self.length = len(overlap)
		self.position = position

	def NONE():
		"""Create empty Match."""
		return Match(None, None, "", Position.NO_OVERLAP)

	def isLongerOrEqual(self, other):
		"""Compare Matches, favour other and return Match."""
		return self.length >= other.length

	def getMerge(self):
		"""Merge Fragments and return str."""

		if self.position == Position.NO_OVERLAP:
			return self.fragment1.value + self.fragment2.value

		elif self.position == Position.IN_FRAGMENT_1:
			return self.fragment1.value

		elif self.position == Position.IN_FRAGMENT_2:
			return self.fragment2.value

		elif self.position == Position.FRONT_FRAGMENT_1:
			return (self.fragment2.value +
				self.fragment1.value[self.length:self.fragment1.length])

		elif self.position == Position.FRONT_FRAGMENT_2:
			return (self.fragment1.value +
				self.fragment2.value[self.length:self.fragment2.length])

class Collection:
	"""Supports merging a collection of fragments.

	Attribute:
		values (str list) -- collection of fragments
	"""

	def __init__(self, values):
		self.values = values

	def getLength(self):		
		"""Find length of collection and return int."""
		return len(self.values)

	def __getFragmentAtIndex(self, index):
		return Fragment(self.values[index])

	def __addFragment(self, fragment):
		self.values.append(fragment)

	def __removeFragment(self, fragment):
		self.values.remove(fragment.value)

	def getMatchWithLongestOverlapInCollection(self):
		"""Find longest overlap and return Match."""

		# Start comparing to nothing
		longestMatch = Match.NONE()

		for i in range(self.getLength()):
			match = self.__getMatchWithLongestOverlapForFragment(
				self.__getFragmentAtIndex(i), i, longestMatch.length)

			# Choose new match when equal,
			# so no overlap matches are still selected
			if match.isLongerOrEqual(longestMatch):
				longestMatch = match;

		return longestMatch;
	
	def __getMatchWithLongestOverlapForFragment(
		self, fragment, fragmentIndex, prevOverlapLength):
		"""Find longest overlap for given Fragment and return Match.

		Arguments:
			fragment (Fragment) -- the given Fragment
			fragmentIndex (int) -- the index to skip
			prevOverlapLength (int) -- the overlap length to skip
		"""

		# Start comparing to nothing
		longestMatchForFragment = Match.NONE()

		for i in range(self.getLength()):
			# Skip if fragment is self
			if fragmentIndex != i:
				match = fragment.getMatchForFragment(
					self.__getFragmentAtIndex(i), prevOverlapLength)

				# Choose new match when equal,
				# so no overlap matches are still selected
				if match.isLongerOrEqual(longestMatchForFragment):
					longestMatchForFragment = match

		return longestMatchForFragment

	def mergeMatch(self, match):
		"""Add merged Fragment and remove unmerged Fragments.

		Argument:
			match (Match) -- contains Fragments to merge
		"""

		self.__addFragment(match.getMerge())
		self.__removeFragment(match.fragment1)
		self.__removeFragment(match.fragment2)

	def greedyMatchAndMerge(self):
		"""Merge entire collection."""

		# Greedy match and merge only needs one less round
		# than length of collection
		for i in range(self.getLength() - 1):
			self.mergeMatch(
				self.getMatchWithLongestOverlapInCollection())