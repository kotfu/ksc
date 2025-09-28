#
# -*- coding: utf-8 -*-
"""Development related tasks to be run with 'invoke'"""

import os
import shutil

import invoke


# shared function
def rmrf(items, verbose=True):
    "Silently remove a list of directories or files"
    if isinstance(items, str):
        items = [items]

    for item in items:
        if verbose:
            print(f"Removing {item}")
        shutil.rmtree(item, ignore_errors=True)
        # rmtree doesn't remove bare files
        try:
            os.remove(item)
        except FileNotFoundError:
            pass


# create namespaces
namespace = invoke.Collection()
namespace_clean = invoke.Collection("clean")
namespace.add_collection(namespace_clean, "clean")

namespace_check = invoke.Collection("check")
namespace.add_collection(namespace_check, "check")

namespace_publish = invoke.Collection("publish")
namespace.add_collection(namespace_publish, "publish")


#####
#
# testing, coverage, and quality
#
#####
@invoke.task
def test(context):
    "Run tests and code coverage using pytest"
    context.run("pytest", echo=True, pty=True)


# in the main namespace, the words are verbs, so we use test here
namespace.add_task(test)
# in the check namespace, check is the verb, tests are the noun
namespace_check.add_task(test, name="tests")


@invoke.task
def pytest_clean(_):
    "Remove pytest cache and code coverage files and directories"
    dirs = [".pytest_cache", ".cache", ".coverage"]
    rmrf(dirs)


namespace_clean.add_task(pytest_clean, name="tests")


@invoke.task
def quality(context):
    "Inspect code quality using ruff"
    context.run("ruff check *.py src/ksc tests", echo=True)


namespace.add_task(quality, name="inspect")
namespace_check.add_task(quality)


@invoke.task
def format_check(context):
    """Check if code is properly formatted using ruff"""
    context.run("ruff format --check *.py tests src", echo=True)


namespace_check.add_task(format_check, name="format")


@invoke.task
def formatt(context):
    """Format code using ruff"""
    context.run("ruff format *.py tests src", echo=True)


namespace.add_task(formatt, name="format")


#####
#
# build and publish
#
#####
DISTDIR = "dist"


@invoke.task
def dist_clean(_):
    "Remove the dist directory"
    rmrf(DISTDIR)


namespace_clean.add_task(dist_clean, "dist")


@invoke.task
def eggs_clean(_):
    "Remove egg directories"
    dirs = set()
    dirs.add(".eggs")
    for name in os.listdir(os.curdir):
        if name.endswith(".egg-info"):
            dirs.add(name)
        if name.endswith(".egg"):
            dirs.add(name)
    rmrf(dirs)


namespace_clean.add_task(eggs_clean, "eggs")


@invoke.task
def bytecode_clean(_):
    "Remove __pycache__ directories and *.pyc files"
    dirs = set()
    for root, dirnames, files in os.walk(os.curdir):
        if "__pycache__" in dirnames:
            dirs.add(os.path.join(root, "__pycache__"))
        for file in files:
            if file.endswith(".pyc"):
                dirs.add(os.path.join(root, file))
    print("Removing __pycache__ directories and .pyc files")
    rmrf(dirs, verbose=False)


namespace_clean.add_task(bytecode_clean, "bytecode")


@invoke.task(pre=list(namespace_check.tasks.values()), default=True)
def check_all(_):
    "Run this before you commit or submit a pull request"


namespace_check.add_task(check_all, "all")


@invoke.task(pre=list(namespace_clean.tasks.values()), default=True)
def clean_all(_):
    "Clean everything"


namespace_clean.add_task(clean_all, "all")


@invoke.task(pre=[clean_all])
def build(context):
    "Create a distribution"
    context.run("uv build")


namespace.add_task(build)


@invoke.task(pre=[build])
def pypi(context):
    "Build and upload a distribution to pypi"
    context.run("uv publish")


namespace_publish.add_task(pypi)


@invoke.task(pre=[build])
def test_pypi(context):
    "Build and upload a distribution to https://test.pypi.org"
    context.run("uv publish --index test-pypi")


namespace_publish.add_task(test_pypi)
