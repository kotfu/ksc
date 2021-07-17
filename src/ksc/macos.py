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
Classes to represent MacOS keys and shortcuts
"""

import collections
import re


class MacOSKey:
    """store the name of a key, input names, ane render names for that key"""

    # pylint: disable=too-many-instance-attributes, too-few-public-methods

    def __init__(
        self,
        key,
        name,
        input_names=None,
        shifted_key=None,
        html_entity=None,
        clarified_name=None,
        ascii_key=None,
        modifier=False,
    ):
        # pylint: disable=too-many-arguments)
        self.key = key
        """The (usually) single character representation of the key. For modifiers and
        most other named keys, we use the unicode representation, i.e. ⌘ for command,
        → for Right Arrow, etc."""

        self.name = name
        """The name of this key spelled out, ie the ← key is Left Arrow. If
        the key is F, the name is F."""

        self.input_names = input_names
        """A list of names which a user can input to reference this key"""

        self.shifted_key = shifted_key
        """If the key has a different output when the shift key is pressed, put
        the shifted value here"""

        self.clarified_name = clarified_name
        """Some keys can benefit from a clarified name, like Period (.) instead of ."""

        self.html_entity = html_entity
        """If this key has an HTML entity, store it here"""

        self.modifier = modifier
        """True if this key is a modifier key, like Fn, Shift, etc."""

        self.ascii_key = ascii_key
        """If the key is a modifier, it also has an ASCII representation, like ~ for Option"""


# make a list of keys, if the key isn't in this list (like F or R), then
# it's just a single character key with nothing special about it
class MacOS:
    """The keys and their properties for MacOS

    Includes methods to parse user input into shortcuts
    """

    keys = [
        # '*' is not unicode for Fn, but their isn't one, and we need something
        # that is a single character
        # order matters for the modifier keys, they need to be in the apple
        # recommended order for displaying modifier keys
        MacOSKey("Fn", "Fn", ["func", "function", "fn"], ascii_key="*", modifier=True),
        MacOSKey(
            "⌃",  # this is not a caret, it's another unicode character
            "Control",
            ["control", "cont", "ctrl", "ctl"],
            ascii_key="^",  # this one is a caret
            modifier=True,
        ),
        MacOSKey("⌥", "Option", ["option", "opt", "alt"], ascii_key="~", modifier=True),
        MacOSKey("⇧", "Shift", ["shift", "shft"], ascii_key="$", modifier=True),
        MacOSKey(
            "⌘", "Command", ["command", "cmd", "clover"], ascii_key="@", modifier=True
        ),
        MacOSKey("⎋", "Escape", ["escape", "esc"]),
        MacOSKey("⇥", "Tab", ["tab"]),
        MacOSKey("⇪", "Caps Lock", ["capslock", "caps"]),
        MacOSKey("␣", "Space", ["space"]),
        MacOSKey("⏏", "Eject", ["eject"]),
        MacOSKey("⌫", "Delete", ["delete", "del"]),
        MacOSKey(
            "⌦",
            "Forward Delete",
            ["forwarddelete", "fwddelete", "forwarddel", "fwddel"],
        ),
        MacOSKey("⌧", "Clear", ["clear"], clarified_name="Clear (⌧)"),
        MacOSKey("↩", "Return", ["return", "rtn"]),
        MacOSKey("⌅", "Enter", ["enter", "ent"]),
        MacOSKey("⇞", "Page Up", ["pageup", "pgup"]),
        MacOSKey("⇟", "Page Down", ["pagedown", "pgdown"]),
        MacOSKey("↖", "Home", ["home"]),
        MacOSKey("↘", "End", ["end"]),
        MacOSKey("←", "Left Arrow", ["leftarrow", "left"]),
        MacOSKey("→", "Right Arrow", ["rightarrow", "right"]),
        MacOSKey("↑", "Up Arrow", ["uparrow", "up"]),
        MacOSKey("↓", "Down Arrow", ["downarrow", "down"]),
        MacOSKey("leftclick", "click", ["leftclick", "click"]),
        MacOSKey("rightclick", "right click", ["rightclick", "rclick"]),
        MacOSKey(
            "`",
            "`",
            ["grave", "backtick", "backquote"],
            shifted_key="~",
            clarified_name="Grave (`)",
        ),
        MacOSKey("~", "~", ["tilde"], clarified_name="Tilde (~)"),
        MacOSKey("1", "1", shifted_key="!"),
        MacOSKey("2", "2", shifted_key="@"),
        MacOSKey("3", "3", shifted_key="#"),
        MacOSKey("4", "4", shifted_key="$"),
        MacOSKey("5", "5", shifted_key="%"),
        MacOSKey("6", "6", shifted_key="^"),
        MacOSKey("7", "7", shifted_key="&"),
        MacOSKey("8", "8", shifted_key="*"),
        MacOSKey("9", "9", shifted_key="("),
        MacOSKey("0", "0", shifted_key=")"),
        MacOSKey("-", "-", ["minus"], shifted_key="_", clarified_name="Minus Sign (-)"),
        MacOSKey("_", "_", ["underscore"], clarified_name="Underscore (_)"),
        MacOSKey("=", "=", ["equals", "equal"], shifted_key="+"),
        MacOSKey("+", "+", ["plus"], clarified_name="Plus Sign (+)"),
        MacOSKey("[", "[", shifted_key="{"),
        MacOSKey("]", "]", shifted_key="}"),
        MacOSKey("\\", "\\", ["backslash"], shifted_key="|"),
        MacOSKey("|", "|", ["pipe"]),
        MacOSKey(
            ";",
            ";",
            ["semicolon", "semi"],
            shifted_key=":",
            clarified_name="Semicolon (;)",
        ),
        MacOSKey(
            "'",
            "'",
            ["singlequote", "sq"],
            shifted_key='"',
            clarified_name="Single Quote (')",
        ),
        MacOSKey('"', '"', ["doublequote", "dq"], clarified_name='Double Quote (")'),
        MacOSKey(",", ",", ["comma"], shifted_key="<", clarified_name="Comma (,)"),
        MacOSKey(".", ".", ["period"], shifted_key=">", clarified_name="Period (.)"),
        MacOSKey("/", "/", ["slash"], shifted_key="?", clarified_name="Slash (.)"),
        MacOSKey("?", "?", ["questionmark", "question"]),
    ]
    # programatically create 35 function keys
    # we choose 35 because that's how many are defined in NSEvent()
    # see https://developer.apple.com/documentation/appkit/1535851-function-key_unicodes
    for _num in range(1, 36):
        _fkey = "F{}".format(_num)
        keys.append(MacOSKey(_fkey, _fkey, [_fkey.lower()]))

    # modifiers is a subset of keys
    modifiers = []
    for _key in keys:
        if _key.modifier:
            modifiers.append(_key)

    # build a keyname dictionary lookup
    keyname_map = {}
    for _key in keys:
        if _key.input_names:
            for _name in _key.input_names:
                keyname_map[_name] = _key

    #
    # construct various data structures from keys, which are the authoritative
    # source

    # the hyper key is a wierd because its a combination of other keys, so we have to
    # handle it separately
    hyper_mods = []
    hyper_mods.append(keyname_map["control"])
    hyper_mods.append(keyname_map["option"])
    hyper_mods.append(keyname_map["shift"])
    hyper_mods.append(keyname_map["command"])
    hyper_name = "Hyper"
    hyper_regex = r"\b" + hyper_name.lower() + r"\b"

    # can't refactor mods_ascii and mods_unicode into a single
    # dictionary, see parse_shortcut() for why
    mods_ascii = collections.OrderedDict()
    mods_unicode = collections.OrderedDict()
    unshifted_keys = ""
    shifted_keys = ""
    mods_regexes = []
    for _key in keys:
        if _key.modifier:
            mods_ascii[_key.ascii_key] = _key
            mods_unicode[_key.key] = _key
            _regex = r"\b(" + "|".join(_key.input_names) + r")\b"
            mods_regexes.append((_key, _regex))
        if _key.shifted_key:
            unshifted_keys += _key.key
            shifted_keys += _key.shifted_key

    # make some translation tables
    to_shifted_trans = str.maketrans(unshifted_keys, shifted_keys)
    to_unshifted_trans = str.maketrans(shifted_keys, unshifted_keys)

    @classmethod
    def named_keys(cls, *, hyper=False, **_):
        """Return a string containing a formatted list of all known keys

        Designed to be called with the namespace from argparse:

            ksc.MacOS.named_keys(**vars(args)))

        If not using argparse, you can just pass the keyword only
        arguments as you typically would
        """
        # start with the modifiers
        output = []
        fmt = "{:12} {:18} {}"
        output.append(fmt.format("Key", "Name", "Inputs"))
        output.append(fmt.format("-" * 12, "-" * 18, "-" * 50))
        keyflag = True
        for key in cls.keys:
            if key.modifier is False and keyflag is True:
                if hyper:
                    output.append(
                        fmt.format(" ", cls.hyper_name, cls.hyper_name.lower())
                    )
                keyflag = False
            if key.key != key.name or key.clarified_name or key.input_names:
                output.append(
                    fmt.format(
                        key.key,
                        key.clarified_name or key.name,
                        ",".join(key.input_names if key.input_names else ""),
                    )
                )
        return "\n".join(output)

    @classmethod
    def parse_shortcuts(cls, text):
        """parse a string or array of text into a standard representation of the shortcut

        text = a string of text to be parsed

        returns an array of shortcut combinations
        """
        combos = []
        for combo in re.split(r" [/|] ", text):
            combos.append(cls.parse_shortcut(combo))
        return combos

    @classmethod
    def parse_shortcut(cls, text):
        """parse a string and return a MacOSKeyboardShortcut object

        Raises ValueError if string can't be parsed

        """
        # pylint: disable=too-many-branches

        # save the original text for an error message
        orig_text = text
        mods = []
        key = ""
        # Only remove hyphens preceeded and followed by non-space character
        # to avoid removing the last hyphen from 'option-shift--' or 'command -'
        text = re.sub(r"(?<=\S)-(?=\S)", " ", text)
        # remove words that represent modifiers from the text, and add them
        # to the 'mods' array
        for (mod, regex) in cls.mods_regexes:
            (text, howmany) = re.subn(regex, "", text, re.IGNORECASE)
            if howmany:
                mods.append(mod)
        # look for the hyper key
        (text, howmany) = re.subn(cls.hyper_regex, "", text, re.IGNORECASE)
        if howmany:
            for mod in cls.hyper_mods:
                mods.append(mod)

        # process the remainder of the text
        for char in text.strip():
            if char == " ":
                continue

            if char in cls.mods_unicode:
                # translate unicode modifier symbols to their plaintext equivilents
                mods.append(cls.mods_unicode[char])
            elif char in cls.mods_ascii and cls.mods_ascii[char] not in mods:
                # but since plaintext modifiers could also be a key, aka
                # @$@ really means command-shift-2, we only treat the first
                # occurance of a plaintext modifier as a modifier, subsequent
                # occurances are the key
                mods.append(cls.mods_ascii[char])
            else:
                key += char

        # map key names to key symbols
        if key.lower() in cls.keyname_map:
            # special key names, pgup, etc are in lowercase
            key = cls.keyname_map[key.lower()].key

        if len(key) == 1:
            if key in cls.shifted_keys:
                # command % should be command shift 5
                # and command ? should be command shift ?
                # these ↓ are the shifted number keys
                mods.append(cls.keyname_map["shift"])  # dups will get removed later
                # the unwritten apple rule that shifted numbers are
                # written as numbers not their symbols
                if key in "!@#$%^&*()":
                    key = key.translate(cls.to_unshifted_trans)
            else:
                if cls.keyname_map["shift"] in mods:
                    # shift is in the mods, and the key is unshifted
                    # we should have the shifted symbol unless it is
                    # a number or letter
                    # command shift 5 should remain command shift 5
                    # and command shift r should remain command shift r
                    if key not in "0123456789":
                        # but shift command / should be shift command ?
                        key = key.translate(cls.to_shifted_trans)

            # shortcuts always displayed with upper case letters
            key = key.upper()
        else:
            if key.lower() in cls.keyname_map:
                # these are the function keys because they are in the map
                # and the key name is longer than a single character
                # either way, if the key is in the map then it's valid
                pass
            else:
                raise ValueError("error parsing '{}'".format(orig_text))

        # remove duplicate modifiers
        mods = list(set(mods))
        # sort the mods to be in Apple's recommended order
        mods.sort(key=cls.keys.index)

        return MacOSKeyboardShortcut(mods, key)


class MacOSKeyboardShortcut:
    """Store and render a keyboard shortcut in the macos flavor

    When this object is created, it expects the modifiers, if present, are in the
    correct order as specified by the Apple Style Guidelines. This occurs in
    MacOS.parse_shortcut().

    """

    def __init__(self, mods, key):
        """
        mods is a list of MacOSKey objects which are modifiers

        key is the keyname (i.e L, ←, 5 or F12)
        """
        self.mods = mods
        self.key = key

    def __repr__(self):
        """custom repr"""
        return "MacOSKeyboardShortcut('{}')".format(self.render())

    def __str__(self):
        """custom string representation"""
        return self.render()

    def render(
        self,
        *,
        hyper=False,
        modifier_symbols=False,
        modifier_ascii=False,
        plus_sign=False,
        key_symbols=False,
        clarify_keys=False,
        **_
    ):
        """render this key as a string for human consumption

        Designed to be called with the namespace from argparse:

            combo.render(**vars(args))

        If not using argparse, you can just pass the keyword only
        arguments as you typically would
        """
        tokens = []
        joiner = ""
        if modifier_symbols:
            if plus_sign:
                joiner = "+"
            tokens.extend(self.mod_symbols())
        elif modifier_ascii:
            joiner = ""
            tokens.extend(self.mod_ascii())
        else:
            joiner = "-"
            tokens.extend(self.mod_names(hyper=hyper))
        if key_symbols:
            tokens.extend(self.key)
        else:
            tokens.append(self.key_name(clarify_keys=clarify_keys))
        return joiner.join(tokens)

    def mod_names(self, hyper=False):
        """return a list of modifier names for this shortcut"""
        output = []
        if hyper and self.mods == MacOS.hyper_mods:
            output.append(MacOS.hyper_name)
        else:
            for mod in self.mods:
                output.append(mod.name)
        return output

    def mod_symbols(self):
        """return a list of unicode symbols representing the modifier names"""
        output = []
        for mod in self.mods:
            output.append(mod.key)
        return output

    def mod_ascii(self):
        """return a list of ascii symbols representing the modifier names"""
        output = []
        for mod in self.mods:
            output.append(mod.ascii_key)
        return output

    def key_name(self, *, clarify_keys=False):
        """return either the key, or if it has a name return that"""
        # find the key object, if it exists
        keyobj = None
        for keytest in MacOS.keys:
            if self.key == keytest.key:
                keyobj = keytest
                break
        # if we have a key object, then use it's name and clarified name
        if keyobj:
            if clarify_keys and keyobj.clarified_name:
                return keyobj.clarified_name
            return keyobj.name
        # otherwise
        return self.key
