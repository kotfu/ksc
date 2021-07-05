#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Jared Crapo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


from ksc.__main__ import (
    main,
    EXIT_ERROR,
    EXIT_USAGE,
)


def test_mac_list(capsys):
    argv = []
    exit_code = main(argv)
    out, err = capsys.readouterr()
    assert err
    assert not out
    assert exit_code == EXIT_USAGE


def test_mac_parse_err(capsys):
    argv = "command //".split(" ")
    exit_code = main(argv)
    out, err = capsys.readouterr()
    assert err
    assert not out
    assert exit_code == EXIT_ERROR
