#!/usr/bin/python
__author__ = "Anneke Smitheram"

import unittest
from greedy import Fragment, Match, Position

class Test_FragmentMethods(unittest.TestCase):
	"""unittests for greedy.py Fragment Class Methods."""

	def __assertEqualMatch(self, testMatch, assertMatch):
		self.assertEqual(testMatch.fragment1.value,
			assertMatch.fragment1.value)
		self.assertEqual(testMatch.fragment2.value,
			assertMatch.fragment2.value)
		self.assertEqual(testMatch.overlap, assertMatch.overlap)
		self.assertEqual(testMatch.length, assertMatch.length)
		self.assertEqual(testMatch.position, assertMatch.position)

	def test_creation(self):
		f1 = Fragment("123456789")

		self.assertEqual(f1.value, "123456789")
		self.assertEqual(f1.length, 9)

	def test_ignoresTooShortOverlaping(self):
		f1 = Fragment("123 there is overlaping")
		f2 = Fragment("just not enough 123")

		testMatch = f1.getMatchForFragment(f2, 4)
		assertMatch = Match(f1, f2, "", Position.NO_OVERLAP)

		self.__assertEqualMatch(testMatch, assertMatch)

	def test_noOverlap(self):
		f1 = Fragment("xxxx")
		f2 = Fragment("yyyy")

		testMatch = f1.getMatchForFragment(f2, 0)
		assertMatch = Match(f1, f2, "", Position.NO_OVERLAP)

	def test_inFirstFragment(self):
		f1 = Fragment("123 or 456")
		f2 = Fragment("or")

		testMatch = f1.getMatchForFragment(f2, 0)
		assertMatch = Match(f1, f2, "or", Position.IN_FRAGMENT_1)

		self.__assertEqualMatch(testMatch, assertMatch)

	def test_inSecondFragment(self):
		f1 = Fragment("and")
		f2 = Fragment("123 and 456")

		testMatch = f1.getMatchForFragment(f2, 0)
		assertMatch = Match(f1, f2, "and", Position.IN_FRAGMENT_2)

	def test_overlapFrontOfFirstFragment(self):
		f1 = Fragment("123 or 456")
		f2 = Fragment("yyyy123")

		testMatch = f1.getMatchForFragment(f2, 0)
		assertMatch = Match(f1, f2, "123", Position.FRONT_FRAGMENT_1)

		self.__assertEqualMatch(testMatch, assertMatch)

	def test_overlapFrontOfSecondFragment(self):
		f1 = Fragment("123 or 456")
		f2 = Fragment("456xxxx")

		testMatch = f1.getMatchForFragment(f2, 0)
		assertMatch = Match(f1, f2, "456", Position.FRONT_FRAGMENT_2)

		self.__assertEqualMatch(testMatch, assertMatch)

	def test_overlapBothSides(self):
		f1 = Fragment("99_66")
		f2 = Fragment("66_99")

		testMatch = f1.getMatchForFragment(f2, 0)
		assertMatch = Match(f1, f2, "99", Position.FRONT_FRAGMENT_1)

		self.__assertEqualMatch(testMatch, assertMatch)

	def test_overlapFrontOfFirstFragmentWithRepeat(self):
		f1 = Fragment("aa_bb_cc_bb")
		f2 = Fragment("bb_dd")

		testMatch = f1.getMatchForFragment(f2, 0)
		assertMatch = Match(f1, f2, "bb", Position.FRONT_FRAGMENT_2)

		self.__assertEqualMatch(testMatch, assertMatch)

	def test_overlapFrontOfSecondFragmentWithRepeat(self):
		f1 = Fragment("22_44")
		f2 = Fragment("11_22_33_22")

		testMatch = f1.getMatchForFragment(f2, 0)
		assertMatch = Match(f1, f2, "22", Position.FRONT_FRAGMENT_1)

		self.__assertEqualMatch(testMatch, assertMatch)