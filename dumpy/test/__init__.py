#!/usr/bin/env python

# Copyright 2014 Gary Martin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import time
try:
    from unittest import mock
except ImportError:
    import mock

from dumpy import retry


class TestException(Exception):
    pass


class TestRetryDecorator(unittest.TestCase):
    """Tests for the retry decorator"""

    def setUp(self):
        self.n = 5
        self.fn = mock.MagicMock()
        self.exception = TestException
        self.fn.side_effect = self.exception('Boom')

    def test_repeats_N_times_on_exceptions(self):
        """on exceptions repeat specified number of times"""
        @retry(self.n)
        def myfunc():
            self.fn()

        # ignoring any exception here
        try:
            myfunc()
        except:
            pass

        self.assertEqual(self.fn.call_count, self.n)

    def test_final_exception_raised(self):
        """on all exceptions raise final exception"""
        @retry(self.n)
        def myfunc():
            self.fn()

        self.assertRaises(TestException, myfunc)

    def test_repeats_on_specified_exception(self):
        """repeat when a specified exception is raised"""
        @retry(self.n, self.exception)
        def myfunc():
            self.fn()

        self.assertRaises(self.exception, myfunc)
        self.assertEqual(self.fn.call_count, self.n)

    def test_no_repeats_on_unspecified_exception(self):
        """don't repeat if unspecifed exception is raised"""
        @retry(self.n, SyntaxError)
        def myfunc():
            self.fn()

        self.assertRaises(self.exception, myfunc)
        self.assertNotEqual(self.fn.call_count, self.n)

    def test_function_arguments_respected(self):
        """check that args are passed through"""
        @retry(self.n)
        def myfunc(a, b, c):
            self.fn(a, b, c=c)

        self.assertRaises(self.exception, myfunc, 1, 2, 3)
        self.fn.assert_called_with(1, 2, c=3)

    def test_timeout_terminates_early(self):
        """check that timeout exits early"""
        def side_effect():
            time.sleep(0.02)
            raise self.exception("Boom")

        f = mock.MagicMock()
        f.side_effect = side_effect

        @retry(self.n, timeout=0.05)
        def myfunc():
            f()

        try:
            myfunc()
        except:
            pass

        self.assertNotEqual(f.call_count, self.n)


def suite(dummy=None):
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestRetryDecorator, 'test'))
    return test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
else:
    test_suite = suite()
