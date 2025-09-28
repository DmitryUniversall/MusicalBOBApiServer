import argparse

from execution_mode import RunMode

# Parser instance
_parser = argparse.ArgumentParser(description='Fastapi application')

# Add arguments
_parser.add_argument(
    '--state',
    type=RunMode,
    choices=list(RunMode),
    help='Specify the run mode (choose from {})'.format('/'.join([e.value for e in RunMode])),
    default=RunMode.DEBUG
)

# Parse
cmd_args = _parser.parse_args()
