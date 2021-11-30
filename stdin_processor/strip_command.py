import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args


def _strip(line, **kwargs):
    left = kwargs.get('left', True)
    right = kwargs.get('right', True)

    l = line
    if left: l = l.lstrip()
    if right: l = l.rstrip()

    return l


def strip(left: bool = typer.Option(True, '--left/--no-left', '-l/--nl', help='Strip left'),
          right: bool = typer.Option(True, '--right/--no-right', '-r/--nr', help='Strip right'),

          ____________________________: str = global_args.args_separator,
          separators: List[str] = global_args.separators,
          clean: bool = global_args.clean,
          group_by: int = global_args.group_by,
          group_join: str = global_args.group_join,
          join: str = global_args.join,
          unique: bool = global_args.unique,
          sort: str = global_args.sort,
          sort_key: str = global_args.sort_key,
          keep: bool = global_args.keep,
          where: List[str] = global_args.where,
          indexes: str = global_args.index,
          _not: bool = global_args._not,
          ignore_case: bool = global_args.ignore_case
          ):
    stdin = STDIN()
    stdin.process(lambda x: _strip(x, left=left, right=right),
                  separators=separators,
                  clean=clean,
                  group_by=group_by,
                  group_join=group_join,
                  unique=unique,
                  sort=sort,
                  sort_key=sort_key,
                  keep=keep,
                  where=where,
                  _not=_not,
                  ignore_case=ignore_case,
                  indexes=indexes,
                  joiner=join)

    print(stdin.value, end='\n' if '\n' in separators else '')
