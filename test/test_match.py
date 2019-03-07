#!/usr/bin/python
__author__ = "Anneke Smitheram"

import unittest
from greedy import Match, Fragment, Position

class Test_Match(unittest.TestCase):
	"""unittests for greedy.py Match Class Methods."""

	def test_creation(self):
		f1 = Fragment("abcde")
		f2 = Fragment("def")

		match = Match(f1, f2, "de", Position.NO_OVERLAP)

		self.assertEqual(match.fragment1, f1)
		self.assertEqual(match.fragment2, f2)
		self.assertEqual(match.overlap, "de")
		self.assertEqual(match.length, 2)
		self.assertEqual(match.position, Position.NO_OVERLAP)

	def test_selfMatchIsLonger(self):
		f1 = Fragment("abc")
		f2 = Fragment("def")
		f3 = Fragment("bcd")

		m1 = Match(f1, f2, "", Position.NO_OVERLAP)
		m2 = Match(f1, f3, "bc", Position.FRONT_FRAGMENT_2)

		self.assertFalse(m1.isLongerOrEqual(m2))

	def test_argumentMatchIsLonger(self):
		f1 = Fragment("abc")
		f2 = Fragment("def")
		f3 = Fragment("bcd")

		m1 = Match(f1, f3, "bc", Position.FRONT_FRAGMENT_2)
		m2 = Match(f1, f2, "", Position.NO_OVERLAP)

		self.assertTrue(m1.isLongerOrEqual(m2))

	def test_selfAndArgmentMatchEqual(self):
		m1 = Match(Fragment("abc"), Fragment("bcd"),
			"bc", Position.FRONT_FRAGMENT_2)
		m2 = Match(Fragment("efg"), Fragment("hef"),
			"ef", Position.FRONT_FRAGMENT_1)

		self.assertTrue(m1.isLongerOrEqual(m2))

	def test_mergeNoOverlap(self):
		match = Match(Fragment("abc"), Fragment("def"),
			"", Position.NO_OVERLAP)

		self.assertEqual(match.getMerge(),"abcdef")

	def test_mergeInFirstFragment(self):
		match = Match(Fragment("abcd"), Fragment("bc"),
			"bc", Position.IN_FRAGMENT_1)

		self.assertEqual(match.getMerge(),"abcd")

	def test_mergeInSecondFragment(self):
		match = Match(Fragment("fg"), Fragment("efgh"),
			"fg", Position.IN_FRAGMENT_2)

		self.assertEqual(match.getMerge(),"efgh")

	def test_mergeFrontOfFirstFragment(self):
		match = Match(Fragment("abcd"), Fragment("efab"),
			"ab", Position.FRONT_FRAGMENT_1)

		self.assertEqual(match.getMerge(),"efabcd")

	def test_mergeFrontOfSecondFragment(self):
		match = Match(Fragment("ghij"), Fragment("ijkl"),
			"ij", Position.FRONT_FRAGMENT_2)

		self.assertEqual(match.getMerge(),"ghijkl")

	def test_mergeFrontOfFirstFragmentWithRepeat(self):
		match = Match(Fragment("abcdabef"), Fragment("ghabiab"),
			"ab", Position.FRONT_FRAGMENT_1)

		self.assertEqual(match.getMerge(),"ghabiabcdabef")

	def test_mergeFrontOfSecondFragmentWithRepeat(self):
		match = Match(Fragment("78128012"), Fragment("12341256"),
			"12", Position.FRONT_FRAGMENT_2)

		self.assertEqual(match.getMerge(),"78128012341256")