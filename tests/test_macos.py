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

import pytest

import ksc
from ksc.__main__ import (
    main,
    EXIT_SUCCESS,
    EXIT_ERROR,
    EXIT_USAGE,
)


def test_mac_parse():
    parsemap = [
        ("command 2", "@2"),
        ("@2", "@2"),
        ("command shift 2", "$@2"),
        ("command %", "$@5"),
        ("command shift %", "$@5"),
        ("command shift 5", "$@5"),
        ("shift control 6", "^$6"),
        ("^$6", "^$6"),
        ("shift-command-/", "$@?"),
        ("command shift /", "$@?"),
        ("shift control \\", "^$|"),
        ("control \\", "^\\"),
        ("control shift `", "^$~"),
        ("^$`", "^$~"),
        ("command ?", "$@?"),
        ("command f", "@F"),
        ("command option r", "~@R"),
        ("⌘⌥⇧⌃r", "^~$@R"),
        ("command-shift-f", "$@F"),
        ("func f2", "*F2"),
        ("fn F13", "*F13"),
        ("F7", "F7"),
        ("control command  shift control H", "^$@H"),
        ("  command -", "@-"),
        ("command command q", "@Q"),
        ("H", "H"),
        ("shift h", "$H"),
        ("command control R", "^@R"),
        ("shift p", "$P"),
        ("shift 4", "$4"),
        ("ctrl 6", "^6"),
        ("command right", "@→"),
        ("control command del", "^@⌫"),
        ("shift ESCAPE", "$⎋"),
        ("control click", "^leftclick"),
        ("option rightclick", "~rightclick"),
        ("hyper 5", "^~$@5"),
        ("command dq", '$@"'),
        ("command tilde", "$@~"),
    ]
    for (inp, parsed) in parsemap:
        shortcut = ksc.MacOS.parse_shortcut(inp)
        assert parsed == shortcut.canonical


@pytest.mark.parametrize(
    "inp",
    [
        "Q99",
        "F0",
        "F100",
        "fred",
        "command - shift 5",
        "control ^F",
        "^$~",
    ],
)
def test_mac_parse_error(inp):
    with pytest.raises(ValueError):
        _ = ksc.MacOS.parse_shortcuts(inp)


@pytest.mark.parametrize(
    "inp, count",
    [
        ("F10 / shift-escape / control-option-right", 3),
        ("control x | control c", 2),
    ],
)
def test_mac_parse_multiple(inp, count):
    combos = ksc.MacOS.parse_shortcuts(inp)
    assert len(combos) == count


@pytest.mark.parametrize(
    "cmdline, result",
    [
        ("$@5", "Shift-Command-5"),
        ("-ms $@5", "⇧⌘5"),
        ("-ms -p $@5", "⇧+⌘+5"),
        ("^~$@R", "Control-Option-Shift-Command-R"),
        ("-y ^~$@R", "Hyper-R"),
        ("-y hyper 5", "Hyper-5"),
        ("-yp -ms hyper 5", "⌃+⌥+⇧+⌘+5"),
        ("-ma hyper 5", "^~$@5"),
        ("-ms -k command esc", "⌘⎋"),
        ("^leftclick", "Control-click"),
        ("~rightclick", "Option-right click"),
        ("-c @.", "Command-Period (.)"),
        ("@⌫", "Command-Delete"),
    ],
)
def test_mac_render(cmdline, result, capsys):
    argv = cmdline.split(" ")
    exit_code = main(argv)
    out, _ = capsys.readouterr()
    out = out.rstrip()
    assert out == result
    assert exit_code == EXIT_SUCCESS


def test_mac_list(capsys):
    argv = "-l".split(" ")
    exit_code = main(argv)
    out, _ = capsys.readouterr()
    assert not ksc.MacOS.hyper_name in out
    assert "Command" in out
    assert exit_code == EXIT_SUCCESS


def test_mac_list_hyper(capsys):
    argv = "-ly".split(" ")
    exit_code = main(argv)
    out, _ = capsys.readouterr()
    assert ksc.MacOS.hyper_name in out
    assert exit_code == EXIT_SUCCESS

def test_keyboard_shortcut_dunders():
    combo = ksc.MacOS.parse_shortcut("opt command v")
    assert combo.__repr__() == "MacOSKeyboardShortcut('{}')".format("~@V")
    assert combo.__str__() == "~@V"
