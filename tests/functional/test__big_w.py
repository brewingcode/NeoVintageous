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


class Test_W(unittest.FunctionalTestCase):

    def test_W(self):
        self.eq('x one |two. three', 'n_W', 'x one two. |three')
        self.eq('x |one, t.- three', 'n_2W', 'x one, t.- |three')
        self.eq('x |on.e t.wo', 'n_2W', 'x on.e t.w|o')
        self.eq('x |one, t.- a&^$x four x', 'n_3W', 'x one, t.- a&^$x |four x')
        self.eq('|one, t.- three', 'n_2W', 'one, t.- |three')
        self.eq('|on.e t.wo', 'n_2W', 'on.e t.w|o')
        self.eq('|one, t.- a&^$x four x', 'n_3W', 'one, t.- a&^$x |four x')

    def test_v_w(self):
        self.eq('one |t=- three', 'v_W', 'one |t=- t|hree')
        self.eq('x |one two x', 'v_W', 'x |one t|wo x')
        self.eq('x |one_ two$ three x', 'v_2W', 'x |one_ two$ t|hree x')
        self.eq('x |one_ two$ a,b.c four x', 'v_3W', 'x |one_ two$ a,b.c f|our x')
        self.eq('|one two x', 'v_W', '|one t|wo x')
        self.eq('|one_ two$ three x', 'v_2W', '|one_ two$ t|hree x')
        self.eq('|one_ two$ a,b.c four x', 'v_3W', '|one_ two$ a,b.c f|our x')
        self.eq('r_|on|e two three four x', 'v_W', 'o|ne t|wo three four x')
        self.eq('r_|on|e_ $two .!"£$%^&*(){}:@,./\\_ four x', 'v_3W', 'o|ne_ $two .!"£$%^&*(){}:@,./\\_ f|our x')
