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
"""
Entry point for 'ksc' command line program.
"""
import argparse
import sys
import textwrap

import ksc


EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_USAGE = 2


def _build_parser():
    """build an arg parser with all the proper parameters"""
    desc = "Create a standardized representation of a MacOS keyboard shortcut."
    epilog = """\
        Keyboard shortcuts can be entered in many ways:

            command shift F
            option command h
            control option command space

        Separate multiple shortcuts with ' / ' or ' | ':

            control x / control c

        See https://github.com/kotfu/ksc for more info
        """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc,
        epilog=textwrap.dedent(epilog),
    )
    parser.add_argument("shortcuts", nargs="*", help="keyboard shortcuts")

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=ksc.VERSION_STRING,
        help="show the version information and exit",
    )
    mod_group = parser.add_mutually_exclusive_group()
    mod_group.add_argument(
        "-ma",
        "--modifier-ascii",
        action="store_true",
        help="output modifiers as ASCII characters instead of modifier names",
    )
    mod_group.add_argument(
        "-ms",
        "--modifier-symbols",
        action="store_true",
        help="output modifier symbols instead of modifier names",
    )
    parser.add_argument(
        "-p",
        "--plus-sign",
        action="store_true",
        help="output + between modifier symbols, only used if -ms",
    )
    parser.add_argument(
        "-y",
        "--hyper",
        action="store_true",
        help="output Hyper as a modifier name",
    )

    parser.add_argument(
        "-k",
        "--key-symbols",
        action="store_true",
        help="output key symbols instead of key names",
    )
    parser.add_argument(
        "-c",
        "--clarify-keys",
        action="store_true",
        help="clarify hard to read keys by spelling out their name, ignored if -k",
    )

    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="list all modifier and key names",
    )
    # potential future options, here for planning
    #
    # parser.add_argument(
    #     "-o",
    #     "--output",
    #     choices=["txt", "html", "json"],
    #     default="txt",
    #     help="output format",
    # )
    # parser.add_argument(
    #     "-s",
    #     "--style",
    #     choices=["mac", "win"],
    #     default="mac",
    #     help="style of shortcut based on operating system",
    # )
    # parser.add_argument(
    #     "-t",
    #     "--template",
    #     help="tempate to use for html output",
    # )
    return parser


def main(argv=None):
    """main function"""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.list:
        # list all available keys, don't parse any input
        print(ksc.MacOS.named_keys(args))
        return EXIT_SUCCESS

    try:
        combos = ksc.MacOS.parse_shortcuts(" ".join(args.shortcuts))
    except ValueError as err:
        print("{}: {}".format(parser.prog, err), file=sys.stderr)
        return EXIT_ERROR

    output = []
    for combo in combos:
        output.append(combo.render(args))
    print(" ".join(output))
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
