#!/ust/bin/python

import unittest, sys

import test_schedule


def test_all():
	suite = unittest.TestSuite()

	suite.addTest(test_schedule.suite())

	result = unittest.TextTestRunner(verbosity = 2).run(suite)

	if not result.wasSuccessful():
		sys.exit(1)


if __name__ == '__main__':
	test_all()
