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
# pylint: disable=protected-access, missing-function-docstring
# pylint: disable=missing-module-docstring, unused-variable

import pytest

import ksc
from ksc.__main__ import (
    main,
    EXIT_SUCCESS,
)


@pytest.mark.parametrize(
    "inp, parsed",
    [
        ("command 2", "Command-2"),
        ("@2", "Command-2"),
        ("command shift 2", "Shift-Command-2"),
        ("command %", "Shift-Command-5"),
        ("command shift %", "Shift-Command-5"),
        ("command shift 5", "Shift-Command-5"),
        ("shift control 6", "Control-Shift-6"),
        ("^$6", "Control-Shift-6"),
        ("shift-command-/", "Shift-Command-?"),
        ("command shift /", "Shift-Command-?"),
        ("command ?", "Shift-Command-?"),
        ("shift control \\", "Control-Shift-|"),
        ("control \\", "Control-\\"),
        ("control shift `", "Control-Shift-~"),
        ("command tilde", "Shift-Command-~"),
        ("^$`", "Control-Shift-~"),
        ("command f", "Command-F"),
        ("command-shift-f", "Shift-Command-F"),
        ("command option r", "Option-Command-R"),
        ("command control R", "Control-Command-R"),
        ("⌘⌥⇧⌃r", "Control-Option-Shift-Command-R"),
        ("control command  shift control H", "Control-Shift-Command-H"),
        ("func f2", "Fn-F2"),
        ("fn F13", "Fn-F13"),
        ("F7", "F7"),
        ("  command -", "Command--"),
        ("command command q", "Command-Q"),
        ("H", "H"),
        ("shift h", "Shift-H"),
        ("shift p", "Shift-P"),
        ("shift 4", "Shift-4"),
        ("ctrl 6", "Control-6"),
        ("command right", "Command-Right Arrow"),
        ("control command del", "Control-Command-Delete"),
        ("shift ESCAPE", "Shift-Escape"),
        ("control click", "Control-click"),
        ("control leftclick", "Control-click"),
        ("option rightclick", "Option-right click"),
        ("hyper 5", "Control-Option-Shift-Command-5"),
        ("command dq", 'Shift-Command-"'),
    ],
)
def test_mac_parse(inp, parsed):
    shortcut = ksc.MacOS.parse_shortcut(inp)
    assert parsed == str(shortcut)


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
    assert repr(combo) == "MacOSKeyboardShortcut('Option-Command-V')"
    assert str(combo) == "Option-Command-V"
