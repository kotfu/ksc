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

import re


class Key:
    """store the name of a key, input names, ane render names for that key"""

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
        Key("*", "Fn", ["func", "function", "fn"], ascii_key="*", modifier=True),
        Key(
            "⌃",  # this is not a caret, it's another unicode character
            "Control",
            ["control", "cont", "ctrl", "ctl"],
            ascii_key="^",  # this one is a caret
            modifier=True,
        ),
        Key("⌥", "Option", ["option", "opt", "alt"], ascii_key="~", modifier=True),
        Key("⇧", "Shift", ["shift", "shft"], ascii_key="$", modifier=True),
        Key("⌘", "Command", ["command", "cmd", "clover"], ascii_key="@", modifier=True),
        Key("⎋", "Escape", ["escape", "esc"]),
        Key("⇥", "Tab", ["tab"]),
        Key("⇪", "Caps Lock", ["capslock", "caps"]),
        Key("␣", "Space", ["space"]),
        Key("⏏", "Eject", ["eject"]),
        Key("⌫", "Delete", ["delete", "del"]),
        Key(
            "⌦",
            "Forward Delete",
            ["forwarddelete", "fwddelete", "forwarddel", "fwddel"],
        ),
        Key("⌧", "Clear", ["clear"], clarified_name="Clear (⌧)"),
        Key("↩", "Return", ["return", "rtn"]),
        Key("⌅", "Enter", ["enter", "ent"]),
        Key("⇞", "Page Up", ["pageup", "pgup"]),
        Key("⇟", "Page Down", ["pagedown", "pgdown"]),
        Key("↖", "Home", ["home"]),
        Key("↘", "End", ["end"]),
        Key("←", "Left Arrow", ["leftarrow", "left"]),
        Key("→", "Right Arrow", ["rightarrow", "right"]),
        Key("↑", "Up Arrow", ["uparrow", "up"]),
        Key("↓", "Down Arrow", ["downarrow", "down"]),
        Key("leftclick", "click", ["leftclick", "click"]),
        Key("rightclick", "right click", ["rightclick", "rclick"]),
        Key(
            "`",
            "`",
            ["grave", "backtick", "backquote"],
            shifted_key="~",
            clarified_name="Grave (`)",
        ),
        Key("~", "~", ["tilde"], clarified_name="Tilde (~)"),
        Key("1", "1", shifted_key="!"),
        Key("2", "2", shifted_key="@"),
        Key("3", "3", shifted_key="#"),
        Key("4", "4", shifted_key="$"),
        Key("5", "5", shifted_key="%"),
        Key("6", "6", shifted_key="^"),
        Key("7", "7", shifted_key="&"),
        Key("8", "8", shifted_key="*"),
        Key("9", "9", shifted_key="("),
        Key("0", "0", shifted_key=")"),
        Key("-", "-", ["minus"], shifted_key="_", clarified_name="Minus Sign (-)"),
        Key("_", "_", ["underscore"], clarified_name="Underscore (_)"),
        Key("=", "=", ["equals", "equal"], shifted_key="+"),
        Key("+", "+", ["plus"], clarified_name="Plus Sign (+)"),
        Key("[", "[", shifted_key="{"),
        Key("]", "]", shifted_key="}"),
        Key("\\", "\\", ["backslash"], shifted_key="|"),
        Key("|", "|", ["pipe"]),
        Key(
            ";",
            ";",
            ["semicolon", "semi"],
            shifted_key=":",
            clarified_name="Semicolon (;)",
        ),
        Key(
            "'",
            "'",
            ["singlequote", "sq"],
            shifted_key='"',
            clarified_name="Single Quote (')",
        ),
        Key('"', '"', ["doublequote", "dq"], clarified_name='Double Quote (")'),
        Key(",", ",", ["comma"], shifted_key="<", clarified_name="Comma (,)"),
        Key(".", ".", ["period"], shifted_key=">", clarified_name="Period (.)"),
        Key("/", "/", ["slash"], shifted_key="?", clarified_name="Slash (.)"),
        Key("?", "?", ["questionmark", "question"]),
    ]
    # programatically create 35 function keys
    # we choose 35 because that's how many are defined in NSEvent()
    # see https://developer.apple.com/documentation/appkit/1535851-function-key_unicodes?preferredLanguage=occ
    for _num in range(1, 36):
        _fkey = "F{}".format(_num)
        keys.append(Key(_fkey, _fkey, [_fkey.lower()]))

    #
    # construct various data structures from keys, which are the authoritative
    # source
    hyper_mods = "^~$@"
    hyper_name = "Hyper"
    hyper_regex = r"\b" + hyper_name.lower() + r"\b"

    mods_names = []
    mods_plaintext = []
    mods_unicode = []
    unshifted_keys = ""
    shifted_keys = ""
    mods_regex_map = []
    for _key in keys:
        if _key.modifier:
            mods_names.append(_key.name)
            mods_plaintext.append(_key.ascii_key)
            mods_unicode.append(_key.key)
            _regex = r"\b(" + "|".join(_key.input_names) + r")\b"
            mods_regex_map.append((_key.ascii_key, _regex))
        if _key.shifted_key:
            unshifted_keys += _key.key
            shifted_keys += _key.shifted_key

    # make some translation tables
    unicode_plaintext_mods_trans = str.maketrans(
        "".join(mods_unicode), "".join(mods_plaintext)
    )
    to_shifted_trans = str.maketrans(unshifted_keys, shifted_keys)
    to_unshifted_trans = str.maketrans(shifted_keys, unshifted_keys)
    # and a keyname dictionary lookup
    keyname_map = {}
    for _key in keys:
        if _key.input_names:
            for _name in _key.input_names:
                keyname_map[_name] = _key

    @classmethod
    def named_keys(cls, args):
        """Return a string containing a formatted list of all known keys"""
        # start with the modifiers
        output = []
        fmt = "{:12} {:18} {}"
        output.append(fmt.format("Key", "Name", "Inputs"))
        output.append(fmt.format("-" * 12, "-" * 18, "-" * 50))
        keyflag = True
        for key in cls.keys:
            if key.modifier is False and keyflag is True:
                if args.hyper:
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
    def parse_shortcuts(cls, shortcuts):
        """parse a string or array of text into a standard representation of the shortcut

        shortcuts = a string of text to be parsed

        uses args from the command line to influence parsing behavior

        returns an array of shortcut combinations
        """
        combos = []
        for combo in re.split(r" [/|] ", shortcuts):
            combos.append(cls.parse_shortcut(combo))
        return combos

    @classmethod
    def parse_shortcut(cls, text):
        """parse a string and return a MacOSKeyboardShortcut object

        Raises ValueError if string can't be parsed

        """

        # save the original text for an error message
        orig_text = text
        mods = []
        key = ""
        # Only remove hyphens preceeded and followed by non-space character
        # to avoid removing the last hyphen from 'option-shift--' or 'command -'
        text = re.sub(r"(?<=\S)-(?=\S)", " ", text)
        # remove words that represent modifiers from the text, and add them
        # to the 'mods' array
        for (modkey, regex) in cls.mods_regex_map:
            (text, cnt) = re.subn(regex, "", text, re.IGNORECASE)
            if cnt:
                mods.append(modkey)
        # look for the hyper key
        (text, cnt) = re.subn(cls.hyper_regex, "", text, re.IGNORECASE)
        if cnt:
            for modkey in cls.hyper_mods:
                mods.append(modkey)

        # process the remainder of the text
        for char in text.strip():
            if char == " ":
                continue
            elif char in cls.mods_unicode:
                # translate unicode modifier symbols to their plaintext equivilents
                mods.append(char.translate(cls.unicode_plaintext_mods_trans))
            elif char in cls.mods_plaintext and char not in mods:
                # but since plaintext modifiers could also be a key, aka
                # @$@ really means command-shift-2, we only treat the first
                # occurance of a plaintext modifier as a modifier, subsequent
                # occurances are the key
                mods.append(char)
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
                mods.append("$")  # duplicates will get removed later
                # the unwritten apple rule that shifted numbers are
                # written as numbers not their symbols
                if key in "!@#$%^&*()":
                    key = key.translate(cls.to_unshifted_trans)
            else:
                if "$" in mods:
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
        mods.sort(key=lambda x: cls.mods_plaintext.index(x))

        return MacOSKeyboardShortcut("".join(mods), key)


class MacOSKeyboardShortcut:
    """Store and render a keyboard shortcut in the macos flavor

    When this object is created, it expects the modifiers, if present, are in the
    correct order as specified by the Apple Style Guidelines. This occurs in
    MacOS.parse_shortcut().

    """

    def __init__(self, mods, key):
        """
        mods is a list of ascii symbols representing key modifiers
        key is the keyname (i.e L, ←, 5 or F12)
        options are the rendering options to use for this key
        """
        self.mods = mods
        self.key = key
        self.canonical = self.mods + self.key

    def __repr__(self):
        return "KeyboardShortcut({})".format(self.canonical)

    def __str__(self):
        return self.canonical

    def render(self, options):
        """render this key as a string for human consumption"""
        tokens = []
        joiner = ""
        if options.modifier_symbols:
            if options.plus_sign:
                joiner = "+"
            tokens.extend(self.mod_symbols())
        elif options.modifier_ascii:
            joiner = ""
            tokens.extend(self.mods)
        else:
            joiner = "-"
            tokens.extend(self.mod_names(options))
        if options.key_symbols:
            tokens.extend(self.key)
        else:
            tokens.append(self.key_name(options))
        return joiner.join(tokens)

    def mod_names(self, options):
        """return a list of modifier names for this shortcut"""
        output = []
        if options.hyper and self.mods == MacOS.hyper_mods:
            output.append(MacOS.hyper_name)
        else:
            for mod in self.mods:
                output.append(MacOS.mods_names[MacOS.mods_plaintext.index(mod)])
        return output

    def mod_symbols(self):
        """return a list of unicode symbols for this shortcut"""
        output = []
        for mod in self.mods:
            output.append(MacOS.mods_unicode[MacOS.mods_plaintext.index(mod)])
        return output

    def key_name(self, options):
        """return either the key, or if it has a name return that"""
        # find the key object, if it exists
        keyobj = None
        for keytest in MacOS.keys:
            if self.key == keytest.key:
                keyobj = keytest
                break
        # if we have a key object, then use it's name and clarified name
        if keyobj:
            if options.clarify_keys and keyobj.clarified_name:
                return keyobj.clarified_name
            return keyobj.name
        # otherwise
        return self.key
