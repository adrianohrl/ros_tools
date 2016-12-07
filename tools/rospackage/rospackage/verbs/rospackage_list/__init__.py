from .cli import main
from .cli import prepare_arguments
from .cli import argument_preprocessor

# This describes this command to the loader
entry_point_data = dict(
    verb='list',
    description="Lists ...",
    # Called for execution, given parsed arguments 
    main=main,
    # Called first to setup argparse, given argparse parser
    prepare_arguments=prepare_arguments,
    # Called after prepare_arguments, but before argparse.parse_args
    argument_preprocessor=argument_preprocessor,
)
