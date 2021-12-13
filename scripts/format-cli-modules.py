#!/usr/bin/env python3

"""format-cli-modules.py - This program formats the rhoas CLI command files to be reference modules as defined by the CCS mod docs standards.

Usage: ./format-cli-modules.py [path]"""


import sys
import os
import re
from pathlib import Path


# Modular documentation constants
ABSTRACT = '[role="_abstract"]'
DEV_PREVIEW_NOTE = """[IMPORTANT]
====
The `rhoas` command-line interface (CLI) is currently available for Development Preview. Development Preview releases provide early access to a limited set of features that might not be fully tested and that might change in the final GA version. Users should not use Development Preview software in production or for business-critical workloads. Limited documentation is available for Development Preview releases and is typically focused on fundamental user goals.
===="""


def format_command_file(cli_file):
    """Formats a rhoas CLI command reference module file to meet the modular documentation guidelines. This function formats the title, headings, and option descriptions, and converts the links to valid xrefs."""

    with cli_file.open(mode="r") as file:
        content = file.read()

    # Make the title H1 and add module type and abstract metadata.
    title_regex = re.compile(r"(^={2}\srhoas\s?.*)(\n+)(.+)")
    doc_title = title_regex.search(content)
    if doc_title:
        new_doc_title = (
            f"{doc_title.groups()[0][1:]}\n\n{ABSTRACT}\n{doc_title.groups()[2]}"
        )
        content = content.replace(doc_title.group(), new_doc_title)

    # Make subsections H2 and add discrete tag.
    heading_regex = re.compile(r"(={3,}\s)(.+)")
    heading_results = heading_regex.findall(content)
    for h in heading_results:
        new_heading = f"[discrete]\n{h[0][1:]}{h[1].capitalize()}"
        content = content.replace("".join(h), new_heading)

    # Convert links to valid xrefs.
    link_regex = re.compile(
        r"""
        (\*\slink:)  # link tag
        ([\w-]+)  # anchor ID for the xref
        (\{\w+\})  # relfilesuffix attribute
        (\[.+\])  # text for the xref
        (.+)  # xref description
        """,
        re.VERBOSE | re.MULTILINE,
    )
    link_results = link_regex.findall(content)
    for l in link_results:
        new_link = f"* xref:_{l[1].replace('-', '_')}{l[3]} {l[4].lstrip()}"
        content = content.replace("".join(l), new_link)

    # Convert options to def lists.
    option_regex = re.compile(
        r"""
        (^\.{4}\n)?  # select opening code block if present
        (^\s{2,})  # beginning spaces
        (-\w,\s--[a-z]+|--[a-z-]+|(?<=\s{5}).+(?=\s{5}))  # option name
        (\s\w+)?  # option data type (optional)
        (.*)  # option description
        (\n\.{4})?  # select closing code block if present
        """,
        re.VERBOSE | re.MULTILINE,
    )
    command_option_results = option_regex.findall(content)
    for op in command_option_results:
        # If the line has an option, format it
        if op[2].startswith("-"):
            # Format for an option with no data type
            if op[3] == (""):
                op_name = f"`{op[2]}`::\n{op[4].strip()}"
            # Format for an option with a data type
            else:
                op_name = f"`{op[2]} _{op[3].strip()}_`::\n{op[4].strip()}"
        # If the line is blank, remove it
        elif op[2].startswith(" "):
            op_name = "\n"
        # If the line has text but no option, append the description to the previous line
        else:
            op_name = f"+\n{op[2].strip()}"

        content = content.replace("".join(op), op_name)

    with cli_file.open(mode="w") as file:
        file.write(content)


def add_dev_preview_note(cli_assembly_file):
    """Adds the dev preview admonition to the rhoas CLI command reference assembly file."""

    with cli_assembly_file.open(mode="r") as file:
        content = file.read()

    if DEV_PREVIEW_NOTE in content:
        return
    else:
        content = content.replace(ABSTRACT, f"{DEV_PREVIEW_NOTE}\n\n{ABSTRACT}")
        with cli_assembly_file.open(mode="w") as file:
            file.write(content)


def main():
    if len(sys.argv) == 1:
        input_dir = Path.cwd().parent / "modules"
        assembly_file = (
            Path.cwd().parent / "assemblies" / "assembly-cli-command-reference.adoc"
        )
    else:
        input_dir = Path(sys.argv[1])
        input_dir = input_dir.resolve()
        assembly_file = (
            input_dir.parent / "assemblies" / "assembly-cli-command-reference.adoc"
        )

    print(f"Formatting CLI command reference modules in {input_dir}")
    for f in input_dir.iterdir():
        if f.stem.startswith("ref-cli") and f.suffix == ".adoc":
            format_command_file(f)

    print(f"Adding dev preview note to {assembly_file.name}")
    add_dev_preview_note(assembly_file)


if __name__ == "__main__":
    main()
