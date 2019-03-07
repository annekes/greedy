#!/usr/bin/python
__author__ = "Anneke Smitheram"

import unittest
from greedy import Collection, Match, Fragment, Position

class Test_CollectionMethods(unittest.TestCase):
	"""unittests for greedy.py Collection Class Methods."""

	def test_creation(self):
		testCollection = Collection(["abc", "bcd", "cdae"])

		self.assertEqual(testCollection.values,
			["abc", "bcd", "cdae"])

	def test_noOverlap(self):
		testCollection = Collection(["no ", "overlap"])

		testCollection.greedyMatchAndMerge()

		self.assertEqual(testCollection.values, ["no overlap"])

	def test_inFirstFragment(self):
		testCollection = Collection(["within left", "in"])

		testCollection.greedyMatchAndMerge()

		self.assertEqual(testCollection.values, ["within left"])

	def test_inSecondFragment(self):
		testCollection = Collection(["in", "within right"])

		testCollection.greedyMatchAndMerge()

		self.assertEqual(testCollection.values, ["within right"])

	def test_overlapFrontOfFirstFragment(self):
		testCollection = Collection(
			["front of first", "overlap at front"])

		testCollection.greedyMatchAndMerge()

		self.assertEqual(testCollection.values,
			["overlap at front of first"])

	def test_overlapFrontOfSecondFragment(self):
		testCollection = Collection(
			["overlap at front", "front of second"])

		testCollection.greedyMatchAndMerge()

		self.assertEqual(testCollection.values,
			["overlap at front of second"])

	def test_overlapBothSidesDifferent(self):
		testCollection = Collection(
			["overlaping on both sides", "both sides have overlaping"])

		testCollection.greedyMatchAndMerge()

		self.assertEqual(testCollection.values,
			["overlaping on both sides have overlaping"])

	def test_overlapBothSidesSame(self):
		testCollection = Collection(
			["overlaping aaa overlaping", "overlaping bbb overlaping"])

		testCollection.greedyMatchAndMerge()

		self.assertEqual(testCollection.values,
			["overlaping aaa overlaping bbb overlaping"])

	def test_overlapFrontOfFirstFragmentWithRepeat(self):
		testCollection = Collection(
			["eg _here_ and _here_", "_here_ should appear twice"])
		testCollection.greedyMatchAndMerge()
		self.assertEqual(testCollection.values,
			["eg _here_ and _here_ should appear twice"])

	def test_overlapFrontOfSecondFragmentWithRepeat(self):
		testCollection = Collection(
			["likewise", "wise it is wise to test the reverse"])
		testCollection.greedyMatchAndMerge()
		self.assertEqual(testCollection.values,
			["likewise it is wise to test the reverse"])

	def test_multipleFragments(self):
		testCollection = Collection(
			["an make th", "who ca", "sun", "!",
			"can make", "an", "make the sunshine"])
		testCollection.greedyMatchAndMerge()
		self.assertEqual(testCollection.values,
			["!who can make the sunshine"])

	def test_mergeNoOverlap(self):
		testCollection = Collection(["abcd", "efgh", "ijkl"])
		match = Match(Fragment("efgh"), Fragment("ijkl"),
			"", Position.NO_OVERLAP)

		testCollection.mergeMatch(match)

		self.assertEqual(testCollection.values,
			["abcd", "efghijkl"])

	def test_mergeInFirstFragment(self):
		testCollection = Collection(["abcdef", "cd", "ijkl"])
		match = Match(Fragment("abcdef"), Fragment("cd"),
			"cd", Position.IN_FRAGMENT_1)

		testCollection.mergeMatch(match)

		self.assertEqual(testCollection.values,
			["ijkl", "abcdef"])

	def test_mergeInSecondFragment(self):
		testCollection = Collection(["abcd", "efghi", "fg"])
		match = Match(Fragment("fg"), Fragment("efghi"),
			"fg", Position.IN_FRAGMENT_2)

		testCollection.mergeMatch(match)

		self.assertEqual(testCollection.values,
			["abcd", "efghi"])

	def test_mergeOverlapFrontOfFirst(self):
		testCollection = Collection(["abcd", "h", "efab"])
		match = Match(Fragment("abcd"), Fragment("efab"),
			"ab", Position.FRONT_FRAGMENT_1)

		testCollection.mergeMatch(match)

		self.assertEqual(testCollection.values,
			["h", "efabcd"])

	def test_mergeOverlapFrontOfSecond(self):
		testCollection = Collection(["1234", "h", "3456"])
		match = Match(Fragment("1234"), Fragment("3456"),
			"34", Position.FRONT_FRAGMENT_2)

		testCollection.mergeMatch(match)

		self.assertEqual(testCollection.values,
			["h", "123456"])