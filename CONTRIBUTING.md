
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

For example, to format the code with ruff do:
```
$ invoke format
```

This project uses setuptools-scm to get the version number in code from the git
tags. While developing, if you want to to re-calculate the version number, you
need to reinstall in place with:
```
$ uv pip install -e .
```

You'd think that `uv sync` would do this, but if `uv` doesn't think anything has
changed, it won't call down into `setuptools-scm`. Using the `uv pip` command
forces a call to `setuptools-scm`.

Now you'll have a newly calculated version to show when you do:
```
$ ksc --version
```


## Building a Distribution

Build the distribution for this project with:
```
$ invoke build
```
which just invokes:
```
$ uv build
```


## Publishing to PyPI

You'll need tokens to publish to PyPI. Once you have the tokens, set them up
in uv. These commands are set up to accept the token on standard input, so
you'll probably want to have them on the clipboard so you can paste them in.

For test PyPi:
```
$ uv auth login test.pypi.org --token -
```
and for real PyPi:
```
$ uv auth login upload.pypi.org --token -
```

With the credentials available to uv, publish to https://test.pypi.org
```
$ invoke publish.test-pypi
```

and then publish to https://www.pypi.org
```
$ invoke publish.pypi
```
