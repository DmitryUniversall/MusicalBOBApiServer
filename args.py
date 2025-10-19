import argparse

from execution_mode import ExecutionMode

# Parser instance
_parser = argparse.ArgumentParser(description='Fastapi application')

# Add arguments
_parser.add_argument(
    '--mode',
    type=ExecutionMode,
    choices=list(ExecutionMode),
    help='Specify the execution mode (choose from {})'.format('/'.join([mode.value for mode in ExecutionMode])),
    default=ExecutionMode.DEBUG
)

# Parse
cmd_args = _parser.parse_args()
