# ksc

A command line tool to create standardized and properly formatted keyboard shortcuts.

The name of this program is a shorthand for (k)eyboard (s)hort(c)ut.

Inspired by and adapted from Brett Terpstra's
[kbd plugin for Jekyll](https://github.com/ttscoff/JekyllPlugins/tree/master/KBDTag).

Here's a few examples:

    $ ksc command shift 5
    Shift-Command-5
    $ ksc -y hyper t
    Hyper-T
    $ ksc control +
    Control-Shift-+
    $ ksc ⌘⇧F
    Shift-Command-F


## Installation

You'll need Python 3 on your system. Download `ksc` and put it in your path.


## Commmand Line Usage

The simplest invocation of this program has some description of the keyboard shortcut
as the arguments. Many variations of input are accepted. Capitalization is not
important. You can use modifier key names and abbreviations, like `Command` and `opt`.
You can use modifier key symbols such as `⇧` and `⌃`. You can use the ASCII symbols
for modifiers that are used in the [Cocoa Text System Key
Bindings](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/EventOverview/TextDefaultsBindings/TextDefaultsBindings.html).

Keys can be any letter or symbol on the keyboard. In addition, you can type the name
of a key, like `esc`, `return`, `home`, `pageup`, and `rightarrow`, `F5`, and `eject`.
Most everything you try should just work. If it doesn't, open an issue and I'll add
it. Here's some examples:

    $ ksc command b
    Command-B
    $ ksc shift F2
    Shift-F2
    $ ksc command-option-rightarrow
    Option-Command-Right Arrow
    $ ksc command shift %
    Shift-Command-5
    $ ksc $~r
    Option-Shift-R
    $ ksc ⇧⌘P
    Shift-Command-P

Note that the output is standardized according to Apple's Style Guidelines (see
below), including names of modifiers, keys, capitalization, interpretation of shifted
symbols and characters, and sequence of modifiers if there are more than one.

Sequences of multiple keystrokes can be entered by separating them with a " / " or " |
" (yes the surrounding spaces are required). This syntax was chosen because it's
faster to enter `command shift F` than `command-shift-F`, and sequences of multiple
shortcuts are pretty rare.

    $ ksc control x / control c
    Control-X Control-C

There are several command line options available. You can see a brief summary by using
the help command line option:

    $ ksc -h


## Apple Style

This program implements the rules given in [Apple's Style Guide](https://help.apple.com/applestyleguide)
under definition "key, keys". Their deep links are not semantic and seem liable to change, so you'll
just have to search for it.

If you strictly followed the Style Guide, the keyboard shortcut to take a screenshot
would be Command-Shift-%. However, Apple never refers to it this way, they use
Command-Shift-5. See
[Take screenshots or screen recordings on Mac](https://support.apple.com/guide/mac-help/take-a-screenshot-or-screen-recording-mh26782/mac).
It appears the unwritten rule is that if the keyboard shortcut includes one of the
number keys and shift, instead of showing the symbol you show the number.

Apple's [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/macos/user-interaction/keyboard/)
conflict with the style guide:

> For example, the keyboard shortcut for Help is
> Command-Question mark (?), not Shift-Command-Slash.

According to the style guide, it should be Command-Shift-Question mark

This program implements the style guide plus the unwritten rule, and ignores the conflict in the HIG.
