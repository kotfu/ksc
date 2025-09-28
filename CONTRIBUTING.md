# Contributing

This project uses [uv](https://docs.astral.sh/uv/) as package and project manager.
You don't have to use `uv` if you don't want to, but this document assumes
you are using `uv`.


## Get Source Code

Clone the repo from github:
```
$ git clone git@github.com:kotfu/ksc.git
```


## Python Environment

Use [uv](https://docs.astral.sh/uv/) to select a python version and save it in
`.python-version`:
```
$ uv python pin 3.13
```

Then create a virutal environment and activate it:
```
$ uv venv
$ source .venv/bin/activate
```


## Dependencies

Install all the development dependencies with:
```
$ uv sync
```

Upgrade all dependent packages to latest compatible versions:
```
$ uv lock --upgrade
```


## Development Tasks (Format, Lint, etc)

Every python project has some scripts/commands/stuff that you run frequently
while developing. These commands could format the code, or run the linter, or
whatever.

uv doesn't do this yet. Makefiles are terrible. There are many tools and utilities
to solve this problem, we use [invoke](https://www.pyinvoke.org). Tasks are code
in `tasks.py`. See the list of all available tasks with:
```
$ invoke -l
```

## Building a Distribution

Build the distribution for this project with:
```
$ invoke build
```
or:
```
$ uv build
```


## Publishing to PyPI

You'll need tokens created and configured in your environment to publish to PyPI.
```
$ uv publish
```
