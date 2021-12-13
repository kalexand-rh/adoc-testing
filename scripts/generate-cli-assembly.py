#!/usr/bin/env python3

# generate-cli-assembly.py - This program generates an assembly file for the
# command reference.
#
# Usage: ./generate-cli-assembly.py


from pathlib import Path


# Modular documentation constants
ABSTRACT = '[role="_abstract"]'
MODULE_TYPE = ":_module-type: REFERENCE"
ASSEMBLY_ID = '[id="cli-command-reference_{context}"]'
ASSEMBLY_TITLE = "= CLI command reference"
ASSEMBLY_ABSTRACT_TEXT = (
    "You use the `rhoas` CLI to manage your application services from the command line."
)
ASSEMBLY_INCLUDE_DIRECTIVE = "include::../{rhoas-module}/"
LEVELOFFSET = "[leveloffset=+1]"


def generate_command_ref_assembly(module_path, assembly_path):
    """Generates the command reference assembly file."""

    with assembly_path.open(mode="w") as file:
        file.write(f"{ASSEMBLY_ID}\n")
        file.write(f"{ASSEMBLY_TITLE}\n\n")
        file.write(f"{ABSTRACT}\n{ASSEMBLY_ABSTRACT_TEXT}\n\n")
        for command in sorted(module_path.iterdir()):
            if command.suffix == ".adoc":
                file.write(f"{ASSEMBLY_INCLUDE_DIRECTIVE}{command.name}{LEVELOFFSET}\n")


def main():
    cli_command_dir = Path.cwd() / "modules"
    cli_assembly_path = (
        Path.cwd() / "assemblies" / "assembly-cli-command-reference.adoc"
    )
    print("Generating CLI command ref assembly")
    generate_command_ref_assembly(cli_command_dir, cli_assembly_path)


if __name__ == "__main__":
    main()