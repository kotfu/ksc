# ksc

A command line tool to create standardized and properly formatted keyboard shortcuts.

The name of this program is a shorthand for (k)eyboard (s)hort(c)ut.

Inspired by and adapted from Brett Terpstra's
[kbd plugin for Jekyll](https://github.com/ttscoff/JekyllPlugins/tree/master/KBDTag).

Here's a few examples:

    $ ksc -ms -p command shift 5
    ⇧+⌘+5
    $ ksc -y hyper t
    Hyper-T
    $ ksc control +
    Control-Shift-+
    $ ksc ⌘⇧F
    Shift-Command-F


## Installation

You'll need Python 3 on your system. Download
[ksc](https://github.com/kotfu/ksc/blob/main/ksc) and put it in your path.


## Specifying Keyboard Shortcuts

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
    $ ksc fn f10
    Fn-F10
    $ ksc command-option-rightarrow
    Option-Command-Right Arrow
    $ ksc command shift %
    Shift-Command-5
    $ ksc $~r
    Option-Shift-R
    $ ksc ⇧⌘P
    Shift-Command-P


Sequences of multiple keyboard shortcuts can be entered by separating them with a ` / `
or ` | ` (the spaces surrounding the slash or the pipe are required).

    $ ksc control x / control c
    Control-X Control-C

If you have a sequence of multiple keyboard shortcuts and the first one has a slash,
you can clarify the shortcut by joining the elements of the shortcut with a `-`:

    $ ksc command-/ / control-f
    Command-/ Control-F

In addition to friendly modifier names, you can also enter keyboard shortcuts using
unicode symbols or ASCII symbols representing the modifiers. The ASCII symbols are
the same as those used by Apple in the
[Cocoa Text System Key Bindings](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/EventOverview/TextDefaultsBindings/TextDefaultsBindings.html).

| Modifier   | Unicode | ASCII |
|------------|:-------:|:-----:|
| Control    |   `⌃`   |  `^`  |
| Option     |   `⌥`   |  `~`  |
| Shift      |   `⇧`   |  `$`  |
| Command    |   `⌘`   |  `@`  |


## Getting Help

You are currently reading the help for this program. You can see a brief summary by
using the help command line option:

    $ ksc -h


## Customizing Output

The output is standardized according to Apple's Style Guidelines (see
below), including names of modifiers, keys, capitalization, interpretation of shifted
symbols and characters, and sequence of modifiers if there are more than one.

There are several command line options to modify the output. The `-ms` or
`--modifier-symbols` options output the modifers as unicode symbols:

    $ ksc -ms shift command u
    ⇧⌘U

Apple says you should include a plus sign between symbols, but I think that it looks
ugly, so that's not the default. If you want it, add the `-p` or `--plus-sign` when
using `-ms`:

    $ ksc -ms -p shift command u
    ⇧+⌘+U

You can also have the modifier symbols output as their ASCII representation by using
the `-ma` or `--modifier-ascii` options:

    $ ksc -ma shift command u
    $@U

The `-k` or `--key-symbols` argument causes all keys to be output as their symbol,
instead of their name. Makes most sense when used with `-ms`:

    $ ksc -ms -k control option pageup
    ⌃⌥⇞

The `-c` or `--clarify-keys` outputs some less-readable keys as names and symbols,
instead of just symbols. This setting is ignored if you use `-k`. Here's you can see
the difference when you use `-c`:

    $ ksc command .
    Command-.
    $ ksc -c command .
    Command-Period (.)


## Show Me The Keys

The alpha-numeric keys like `T` and `8` are easily known and understood. However, you may
not know all the names and symbols for the other keys. You can get a list with:

    $ ksc -l


## Keyboard Maestro

I have created a simple [Keyboard Maestro](https://www.keyboardmaestro.com/) macro
which allows you to use `ksc` anywhere you can type on your Mac. I set a typed input trigger
so when I type `;ksc`, Keyboard Maestro prompts me for input. I type in the keyboard shortcut
I want, and Keyboard Maestro runs the script, captures the output, and then types the output
where my cursor is.

[![Keyboard Maestro Macro for Keyboard Shortcut](/keyboard-maestro-macro.jpg)](/Keyboard%20Shortcut.kmmacros)

Download the [Keyboard Shortcut macro](/Keyboard%20Shortcut.kmmacros) for Keyboard Maestro.


## The Hyper Key

Using [Karabiner Elements](https://karabiner-elements.pqrs.org/) or
[BetterTouchTool](https://folivora.ai/), you can make `Caps Lock-T` be the same as
pressing `Control-Option-Shift-Command-T`. Mac nerds call this the [Hyper
key](https://statusq.org/archives/2016/09/25/7857/). You can always
use `hyper` as a modifier key when entering a keyboard shortcut:

    $ ksc hyper-t
    Control-Option-Shift-Command-T

If you give the `-y` or `--hyper` command line option, you will get a `Hyper` key in
your output when it's appropriate:

    $ ksc -y control option shift command t
    Hyper-T
    # ksc -y hyper t
    Hyper-T


## Tips and Tricks

* You can easily get the unicode symbol for a key and put it on your clipboard (on MacOS) with:

      $ ksc -k home | pbcopy

* Because the tilde character `~` can mean both the `Option` key as well as `Shift-Grave`, the
  following input is ambiguous:

      $ ksc '$@~'

  Note the single quotes to protect all those special characters from being
  interpreted by your shell. This could either mean `Shift-Command-~`, which is valid,
  or `Shift-Command-Option`, which is not, therefore this input causes a parsing
  error. You can clarify by using:

      $ ksc command tilde
      Shift-Command-~

  or:

      $ ksc -c shift command grave
      Shift-Command-Tilde (~)


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
