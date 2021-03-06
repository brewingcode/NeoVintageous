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

from NeoVintageous.tests import unittest


class Test_right_paren(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|a b c. xy', 'n_)', 'a b c. |xy')
        self.eq('|a b c? xy', 'n_)', 'a b c? |xy')
        self.eq('|a b c! xy', 'n_)', 'a b c! |xy')
        self.eq('|a b c! x y. a b. xy.', 'n_3)', 'a b c! x y. a b. |xy.')

    def test_N(self):
        self.eq('|a b c. xy', ')', 'N_|a b c. |xy')
        self.eq('|a b c? xy', ')', 'N_|a b c? |xy')
        self.eq('|a b c! xy', ')', 'N_|a b c! |xy')

    def test_v(self):
        self.eq('|a b c. xyz', 'v_)', '|a b c. x|yz')
        self.eq('|a b c? xyz', 'v_)', '|a b c? x|yz')
        self.eq('|a b c! xyz', 'v_)', '|a b c! x|yz')
