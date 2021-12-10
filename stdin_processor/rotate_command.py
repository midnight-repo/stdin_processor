import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args
import sys
from collections import deque

def _rotate(x, i, **kwargs):
    left = kwargs.get('left')
    right = kwargs.get('right')

    if left and right:
        return x

    rotation = -1*i if left else i
    s = deque(list(x))
    s.rotate(rotation)

    return ''.join(list(s))

def rotate(value:int = typer.Argument(0, metavar='INT'),
           left: bool = typer.Option(False, '--left', '-l'),
           right: bool = typer.Option(False, '--right', '-r'),

           ____________________________: str = global_args.args_separator,
           separators: List[str] = global_args.separators,
           clean: bool = global_args.clean,
           group_by: int = global_args.group_by,
           group_join: str = global_args.group_join,
           join: str = global_args.join,
           unique: bool = global_args.unique,
           sort: str = global_args.sort,
           sort_key: str = global_args.sort_key,
           shuffle: bool = global_args.shuffle,
           keep: bool = global_args.keep,
           where: List[str] = global_args.where,
           start_where: str = global_args.start_where,
           stop_where: str = global_args.stop_where,
           indexes: str = global_args.index,
           _not: bool = global_args._not,
           rotation: int = global_args.rotation,
           reverse: bool = global_args.reverse,
           ignore_case: bool = global_args.ignore_case
           ):


    stdin = STDIN(sys.stdin.read())
    stdin.process(lambda x: _rotate(x, value, left=left, right=right),
                  separators=separators,
                  clean=clean,
                  group_by=group_by,
                  group_join=group_join,
                  unique=unique,
                  sort=sort,
                  sort_key=sort_key,
                  shuffle=shuffle,
                  keep=keep,
                  where=where,
                  start_where=start_where,
                  stop_where=stop_where,
                  _not=_not,
                  ignore_case=ignore_case,
                  indexes=indexes,
                  rotation=rotation,
                  reverse=reverse,
                  joiner=join)

    print(stdin.value, end='' if stdin.value.endswith('\n') else '\n')
