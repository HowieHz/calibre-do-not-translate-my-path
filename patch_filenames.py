# -*- coding: utf-8 -*-

import ast
import sys
import subprocess
import glob
import os
import shutil

import click

PATCH_ANCHOR="""\
def ascii_filename(orig, substitute='_'):
    if isinstance(substitute, bytes):
        substitute = substitute.decode(filesystem_encoding)
    orig = ascii_text(orig).replace('?', '_')
    ans = ''.join(x if ord(x) >= 32 else substitute for x in orig)
    return sanitize_file_name(ans, substitute=substitute)"""

PATCH_CODE = r"""def ascii_filename(orig, substitute='_'):
    import re
    return re.sub(r"[\/\\\:\*\?\"\<\>\|]", substitute, orig)
"""

def patch(input: str, output: str | None, os: str):
    if output is None:
        output = input

    with open(input, "r", encoding="utf8") as f:
        old = f.read()

    code = PATCH_CODE
    new = old.replace(PATCH_ANCHOR, code, 1)

    with open(output, "w", encoding="utf8") as f:
        f.write(new)

@click.command()
@click.argument("input", required=True, type=click.Path(exists=True))
@click.argument("output", required=False, type=click.Path(exists=False))
@click.option(
    "os",
    "-o",
    "--os",
    type=click.Choice(["win", "unix"]),
    default="win",
)
def cli_patch(input, output, os):
    patch(input, output, os)

if __name__ == "__main__":
    cli_patch()