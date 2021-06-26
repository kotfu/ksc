# ksc

A command line tool to create standardized and properly formatted keyboard shortcuts.

The name of this program is a shorthand for (k)eyboard (s)hort(c)ut.

Inspired by and adapted from Brett Terpstra's
[kbd plugin for Jekyll](https://github.com/ttscoff/JekyllPlugins/tree/master/KBDTag).

Here's a few examples:

```
$ ksc command shift 5
Shift-Command-5
$ ksc -y hyper t
Hyper-T
$ ksc control +
Control-Shift-+
$ ksc ⌘⇧F
Shift-Command-F
```


## Installation

You'll need Python 3 on your system. Download `ksc` and put it in your path.


## Commmand Line Usage

Sequences of multiple keystrokes can be entered by separating them
with a " / " (yes the spaces are required around the /). This syntax
was chosen because it's more likely and easier to enter "command shift F"
than command-shift-f

When output in plain text, keys in a sequence are separated by a space
When output in html, each key in a sequence is in its own span


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

    For example, the keyboard shortcut for Help is
    Command-Question mark (?), not Shift-Command-Slash.

According to the style guide, it should be Command-Shift-Question mark

This program implements the style guide plus the unwritten rule, and ignores the conflict in the HIG.
