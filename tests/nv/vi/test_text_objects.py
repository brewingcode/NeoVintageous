# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

from collections import namedtuple

from NeoVintageous.tests import unittest

from NeoVintageous.nv.vi.text_objects import a_big_word
from NeoVintageous.nv.vi.text_objects import a_word
from NeoVintageous.nv.vi.text_objects import big_word_end
from NeoVintageous.nv.vi.text_objects import big_word_start
from NeoVintageous.nv.vi.text_objects import find_next_lone_bracket
from NeoVintageous.nv.vi.text_objects import find_prev_lone_bracket
from NeoVintageous.nv.vi.text_objects import get_text_object_region
from NeoVintageous.nv.vi.text_objects import is_at_punctuation
from NeoVintageous.nv.vi.text_objects import is_at_space


test = namedtuple('simple_test', 'content start brackets expected msg')

TESTS = (
    test(content='aaa', start=1, brackets=('\\{', '\\}'), expected=None, msg='should return none'),
    test(content='a{a}a', start=1, brackets=('\\{', '\\}'), expected=unittest.Region(1, 2), msg='should find bracket at caret position'),  # noqa: E501
    test(content='{aa}a', start=1, brackets=('\\{', '\\}'), expected=unittest.Region(0, 1), msg='should find bracket at BOF'),  # noqa: E501
    test(content='bbb{aa}a', start=2, brackets=('\\{', '\\}'), expected=None, msg='should not find brackets after caret'),  # noqa: E501
    test(content='a{bc', start=3, brackets=('\\{', '\\}'), expected=unittest.Region(1, 2), msg='should find unbalanced bracket before caret'),  # noqa: E501

    test(content='foo {bar {foo} bar}', start=16, brackets=('\\{', '\\}'), expected=unittest.Region(4, 5), msg='should find outer bracket from RHS'),  # noqa: E501
    test(content='foo {bar {foo} bar}', start=7, brackets=('\\{', '\\}'), expected=unittest.Region(4, 5), msg='should find outer bracket from LHS'),  # noqa: E501
    test(content='foo {bar {foo} bar}', start=13, brackets=('\\{', '\\}'), expected=unittest.Region(9, 10), msg='should find inner bracket'),  # noqa: E501

    test(content='foo {bar {foo} bar', start=16, brackets=('\\{', '\\}'), expected=unittest.Region(4, 5), msg='should find outer if unbalanced outer'),  # noqa: E501
    test(content='foo {bar {foo} bar', start=12, brackets=('\\{', '\\}'), expected=unittest.Region(9, 10), msg='should find inner if unbalanced outer'),  # noqa: E501
    test(content='foo {bar {foo} bar', start=4, brackets=('\\{', '\\}'), expected=unittest.Region(4, 5), msg='should find bracket at caret position'),  # noqa: E501

    test(content='foo <bar <foo> bar>', start=16, brackets=('<', '>'), expected=unittest.Region(4, 5), msg='should find outer angle bracket from RHS'),  # noqa: E501
    test(content='foo <bar <foo> bar>', start=7, brackets=('<', '>'), expected=unittest.Region(4, 5), msg='should find outer angle bracket from LHS'),  # noqa: E501
    test(content='foo <bar <foo> bar>', start=13, brackets=('<', '>'), expected=unittest.Region(9, 10), msg='should find inner angle bracket'),  # noqa: E501

    test(content='a\\{bc', start=2, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket at caret position'),  # noqa: E501
    test(content='a\\{bc', start=3, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket'),
)

TESTS_NEXT_BRACKET = (
    test(content='a\\}bc', start=2, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket at caret position'),  # noqa: E501
    test(content='a\\}bc', start=0, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket'),
    test(content='foo {bar foo bar}', start=16, brackets=('\\{', '\\}'), expected=unittest.Region(16, 17), msg='should find next bracket at caret position'),  # noqa: E501
)


class Test_previous_bracket(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.content)
            self.view.sel().clear()

            actual = find_prev_lone_bracket(self.view, data.start, data.brackets)

            self.assertEqual(data.expected, actual, "failed at test index {0}: {1}".format(i, data.msg))


class Test_next_bracket(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS_NEXT_BRACKET):
            self.write(data.content)
            self.view.sel().clear()

            actual = find_next_lone_bracket(self.view, data.start, data.brackets)

            self.assertEqual(data.expected, actual, "failed at test index {0}: {1}".format(i, data.msg))


class TestIsAtSpace(unittest.ViewTestCase):

    def test_basic(self):
        self.write('a bc .,: d')
        self.assertFalse(is_at_space(self.view, 0))
        self.assertTrue(is_at_space(self.view, 1))
        self.assertFalse(is_at_space(self.view, 2))
        self.assertFalse(is_at_space(self.view, 3))
        self.assertTrue(is_at_space(self.view, 4))
        self.assertFalse(is_at_space(self.view, 5))
        self.assertFalse(is_at_space(self.view, 6))
        self.assertFalse(is_at_space(self.view, 7))
        self.assertTrue(is_at_space(self.view, 8))
        self.assertFalse(is_at_space(self.view, 9))


class TestIsAtPunctuation(unittest.ViewTestCase):

    def test_is_at_punctuation(self):
        self.write('a bc .,: d\nx\ty')
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertFalse(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertFalse(is_at_punctuation(self.view, 3))
        self.assertFalse(is_at_punctuation(self.view, 4))
        self.assertTrue(is_at_punctuation(self.view, 5))
        self.assertTrue(is_at_punctuation(self.view, 6))
        self.assertTrue(is_at_punctuation(self.view, 7))
        self.assertFalse(is_at_punctuation(self.view, 8))
        self.assertFalse(is_at_punctuation(self.view, 9))
        self.assertFalse(is_at_punctuation(self.view, 10))
        self.assertFalse(is_at_punctuation(self.view, 11))
        self.assertFalse(is_at_punctuation(self.view, 12))
        self.assertFalse(is_at_punctuation(self.view, 13))
        self.assertFalse(is_at_punctuation(self.view, 14))
        self.assertFalse(is_at_punctuation(self.view, 15))
        self.assertFalse(is_at_punctuation(self.view, 16))

    def test_is_at_punctuation_newline_issue_a(self):
        self.write('a\nb\\nc')
        self.assertSize(6)
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertFalse(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertTrue(is_at_punctuation(self.view, 3))
        self.assertFalse(is_at_punctuation(self.view, 4))
        self.assertFalse(is_at_punctuation(self.view, 5))
        self.assertFalse(is_at_punctuation(self.view, 6))

    def test_is_at_punctuation_tab_char_issue_a(self):
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('translate_tabs_to_spaces', True)
        self.write('a\tb')
        self.assertContent('a   b')
        self.assertSize(5)
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertFalse(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertFalse(is_at_punctuation(self.view, 3))
        self.assertFalse(is_at_punctuation(self.view, 4))
        self.assertFalse(is_at_punctuation(self.view, 5))

    def test_is_at_punctuation_tab_char_issue_b(self):
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('translate_tabs_to_spaces', False)
        self.write('a\tb')
        self.assertContent('a\tb')
        self.assertSize(3)
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertFalse(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertFalse(is_at_punctuation(self.view, 3))

    def test_is_at_punctuation_tab_char_issue_c(self):
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('translate_tabs_to_spaces', False)
        self.write('a\\tb')
        self.assertContent('a\\tb')
        self.assertSize(4)
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertTrue(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertFalse(is_at_punctuation(self.view, 3))
        self.assertFalse(is_at_punctuation(self.view, 4))

    def test_is_at_punctuation_tab_char_issue_d(self):
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('translate_tabs_to_spaces', True)
        self.write('a\\tb')
        self.assertContent('a\\tb')
        self.assertSize(4)
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertTrue(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertFalse(is_at_punctuation(self.view, 3))
        self.assertFalse(is_at_punctuation(self.view, 4))


class TestAWord(unittest.ViewTestCase):

    def test_returns_full_word(self):
        self.write('foo bar baz\n')
        self.assertRegion(a_word(self.view, 5), 'bar ')

    def test_returns_word_and_preceding_white_space(self):
        self.write('(foo bar) baz\n')
        self.assertRegion(a_word(self.view, 5), ' bar')

    def test_returns_word_and_all_preceding_white_space(self):
        self.write('(foo   bar) baz\n')
        self.assertRegion(a_word(self.view, 8), '   bar')

    # XXX when the cursor starts at space character
    # it should probably include the following
    # word too to match Vim behaviour e.g
    # `a| b c` -> daw should delete ` b`
    def test_letters_digits_and_underscores(self):
        self.write('a ab _a _a1 x')
        self.assertRegion(a_word(self.view, 0), 'a ')
        self.assertRegion(a_word(self.view, 1), ' ')
        self.assertRegion(a_word(self.view, 2), 'ab ')
        self.assertRegion(a_word(self.view, 3), 'ab ')
        self.assertRegion(a_word(self.view, 4), ' ')
        self.assertRegion(a_word(self.view, 5), '_a ')
        self.assertRegion(a_word(self.view, 6), '_a ')
        self.assertRegion(a_word(self.view, 7), ' ')
        self.assertRegion(a_word(self.view, 8), '_a1 ')
        self.assertRegion(a_word(self.view, 9), '_a1 ')
        self.assertRegion(a_word(self.view, 10), '_a1 ')
        self.assertRegion(a_word(self.view, 11), ' ')
        self.assertRegion(a_word(self.view, 12), ' x')

    def test_letters_digits_and_underscores_eol_includes_preceding_space(self):
        self.write('x   e12_x')
        self.assertRegion(a_word(self.view, 4), '   e12_x')

    # XXX when the cursor starts at space character
    # it should probably include the following
    # word too to match Vim behaviour e.g
    # `a| b c` -> daw should delete ` b`
    def test_non_blank_characters(self):
        self.write('.. .,-= .%.$ .')
        self.assertRegion(a_word(self.view, 0), '.. ')
        self.assertRegion(a_word(self.view, 1), '.. ')
        self.assertRegion(a_word(self.view, 2), ' ')
        self.assertRegion(a_word(self.view, 3), '.,-= ')
        self.assertRegion(a_word(self.view, 4), '.,-= ')
        self.assertRegion(a_word(self.view, 5), '.,-= ')
        self.assertRegion(a_word(self.view, 6), '.,-= ')
        self.assertRegion(a_word(self.view, 7), ' ')
        self.assertRegion(a_word(self.view, 8), '.%.$ ')
        self.assertRegion(a_word(self.view, 9), '.%.$ ')
        self.assertRegion(a_word(self.view, 10), '.%.$ ')
        self.assertRegion(a_word(self.view, 11), '.%.$ ')
        self.assertRegion(a_word(self.view, 12), ' ')
        self.assertRegion(a_word(self.view, 13), ' .')

    def test_non_blank_characters_eol_includes_preceding_space(self):
        self.write('x    .=-,')
        self.assertRegion(a_word(self.view, 5), '    .=-,')

    # XXX when the cursor starts at space character
    # it should probably include the following
    # word too to match Vim behaviour e.g
    # `a| b c` -> daw should delete ` b`
    def test_letters_digits_underscores_and_non_blank_characters(self):
        self.write('ab.. _a_,=-12.34 .')
        self.assertRegion(a_word(self.view, 0), 'ab')
        self.assertRegion(a_word(self.view, 1), 'ab')
        self.assertRegion(a_word(self.view, 2), '.. ')
        self.assertRegion(a_word(self.view, 3), '.. ')
        self.assertRegion(a_word(self.view, 4), ' ')
        self.assertRegion(a_word(self.view, 5), ' _a_')
        self.assertRegion(a_word(self.view, 8), ',=-')
        self.assertRegion(a_word(self.view, 11), '12')
        self.assertRegion(a_word(self.view, 13), '.')
        self.assertRegion(a_word(self.view, 14), '34 ')


class TestABigWordStart(unittest.ViewTestCase):

    def test_basic(self):
        self.write('xyz x._a1     xx')

        self.assertEqual(0, big_word_start(self.view, 0))
        self.assertEqual(0, big_word_start(self.view, 1))
        self.assertEqual(0, big_word_start(self.view, 2))

        self.assertEqual(4, big_word_start(self.view, 3))
        self.assertEqual(4, big_word_start(self.view, 4))
        self.assertEqual(4, big_word_start(self.view, 5))
        self.assertEqual(4, big_word_start(self.view, 6))
        self.assertEqual(4, big_word_start(self.view, 7))
        self.assertEqual(4, big_word_start(self.view, 8))

        self.assertEqual(10, big_word_start(self.view, 9))
        self.assertEqual(11, big_word_start(self.view, 10))
        self.assertEqual(12, big_word_start(self.view, 11))
        self.assertEqual(13, big_word_start(self.view, 12))

        self.assertEqual(14, big_word_start(self.view, 13))
        self.assertEqual(14, big_word_start(self.view, 14))
        self.assertEqual(14, big_word_start(self.view, 15))


class TestABigWordEnd(unittest.ViewTestCase):

    def test_basic(self):
        self.write('xyz x._a1     xx')

        self.assertEqual(3, big_word_end(self.view, 0))
        self.assertEqual(3, big_word_end(self.view, 1))
        self.assertEqual(3, big_word_end(self.view, 2))
        self.assertEqual(3, big_word_end(self.view, 3))

        self.assertEqual(9, big_word_end(self.view, 4))
        self.assertEqual(9, big_word_end(self.view, 5))
        self.assertEqual(9, big_word_end(self.view, 6))
        self.assertEqual(9, big_word_end(self.view, 7))
        self.assertEqual(9, big_word_end(self.view, 8))
        self.assertEqual(9, big_word_end(self.view, 9))

        self.assertEqual(10, big_word_end(self.view, 10))
        self.assertEqual(11, big_word_end(self.view, 11))
        self.assertEqual(12, big_word_end(self.view, 12))
        self.assertEqual(13, big_word_end(self.view, 13))

        self.assertEqual(16, big_word_end(self.view, 14))
        self.assertEqual(16, big_word_end(self.view, 15))


class TestABigWord(unittest.ViewTestCase):

    def test_returns_full_words(self):
        self.write('a baz bA.__ eol')
        self.assertRegion(a_big_word(self.view, 0), 'a')
        self.assertRegion(a_big_word(self.view, 1), ' baz')
        self.assertRegion(a_big_word(self.view, 2), 'baz')
        self.assertRegion(a_big_word(self.view, 3), 'baz')
        self.assertRegion(a_big_word(self.view, 4), 'baz')
        self.assertRegion(a_big_word(self.view, 5), ' bA.__')
        self.assertRegion(a_big_word(self.view, 6), 'bA.__')
        self.assertRegion(a_big_word(self.view, 7), 'bA.__')
        self.assertRegion(a_big_word(self.view, 8), 'bA.__')
        self.assertRegion(a_big_word(self.view, 9), 'bA.__')
        self.assertRegion(a_big_word(self.view, 10), 'bA.__')
        self.assertRegion(a_big_word(self.view, 11), ' eol')
        self.assertRegion(a_big_word(self.view, 12), 'eol')
        self.assertRegion(a_big_word(self.view, 13), 'eol')
        self.assertRegion(a_big_word(self.view, 14), 'eol')

    def test_should_not_error_when_cursor_starts_on_whitespace(self):
        self.write('a   b')
        self.assertRegion(a_big_word(self.view, 0), 'a')
        self.assertRegion(a_big_word(self.view, 1), '   b')
        self.assertRegion(a_big_word(self.view, 2), '   b')
        self.assertRegion(a_big_word(self.view, 3), '   b')
        self.assertRegion(a_big_word(self.view, 4), 'b')


class TestGetTextObjectRegion(unittest.ViewTestCase):

    def test_text_object_does_nothing_and_returns_selection(self):
        self.assertEqual(get_text_object_region(self.view, '__expected__', 'foobar'), '__expected__')
