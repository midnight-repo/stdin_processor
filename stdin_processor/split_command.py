import typer
from typing import List
from stdin_processor.processor import STDIN, backslashed, parse_index_pattern
from stdin_processor import global_args
import re
import sys

def _split(string, **kwargs):
    index_pattern = kwargs.get('index_pattern', None)
    split_separators = kwargs.get('split_separators', [' '])
    split_keep = kwargs.get('split_keep', True)
    split_joiner = kwargs.get('split_joiner', ' ')

    s = string
    backslashed_separators = map(backslashed, split_separators)
    regex_pattern = '|'.join(backslashed_separators)
    split_string = re.split(regex_pattern, s)
    if not split_keep:
        while '' in split_string: split_string.remove('')

    if index_pattern:
        targets = parse_index_pattern(split_string, index_pattern)
        matched = [split_string[i] for i in range(len(split_string)) if i in targets]
        return split_joiner.join(matched)
    else:
        return split_joiner.join(split_string)


def split(split_separators: List[str] = typer.Argument(..., help='Separators to split each element of stdin with'),
          split_joiner: str = typer.Option(' ', '--split-join', '--sj', metavar='JOINER', help='Joiner to join the splitted element of stdin with'),
          position: str = typer.Option(None, '--position', '-p', help='Index patterns'),
          split_keep: bool = typer.Option(True, '--split-keep/--no-split-keep', '--sk/--nsk', show_default=False, help='Keep empty values when splitting each element [default: keep]'),
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
          indexes: str = global_args.index,
          _not: bool = global_args._not,
          rotation: int = global_args.rotation,
          ignore_case: bool = global_args.ignore_case
          ):
    stdin = STDIN(sys.stdin.read())
    stdin.process(lambda x: _split(x, split_separators=split_separators, split_joiner=split_joiner,
                                   index_pattern=position, split_keep=split_keep),
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
                  _not=_not,
                  ignore_case=ignore_case,
                  indexes=indexes,
                  rotation=rotation,
                  joiner=join)

    print(stdin.value, end='' if stdin.value.endswith('\n') else '\n')
