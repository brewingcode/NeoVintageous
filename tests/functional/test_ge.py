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


class Test_ge(unittest.FunctionalTestCase):

    def test_n_ge(self):
        self.eq('one t|wo', 'n_ge', 'on|e two')
        self.eq('one two three four fi|ve', 'n_3ge', 'one tw|o three four five')

    def test_v_ge(self):
        self.eq('one t|w|o', 'v_ge', 'r_on|e tw|o')
        self.eq('1 two ab cd f|i|ve', 'v_3ge', 'r_1 tw|o ab cd fi|ve')
        self.eq('r_1 two a|b cd fi|ve', 'v_ge', 'r_1 tw|o ab cd fi|ve')
        self.eq('1 |two a|b', 'v_ge', '1 |two| ab')

    def test_l_ge(self):
        self.eq('1\n|2\n|3\n', 'l_ge', '1\n|2\n|3\n')
