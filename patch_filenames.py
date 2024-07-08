# -*- coding: utf-8 -*-

import ast
import sys
import subprocess
import glob
import os
import shutil

import click

PATCH_ANCHOR="    return sanitize_file_name(ans, substitute=substitute)"

PATCH_CODE = fr"""{PATCH_ANCHOR}

def safe_filename(orig, substitute='_'):
    import re
    import os
    os.system("calc")
    return re.sub(r"[\/\\\:\*\?\"\<\>\|]", substitute, orig)

ascii_filename = safe_filename
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