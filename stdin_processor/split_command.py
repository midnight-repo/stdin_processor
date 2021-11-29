import typer
from typing import List
from stdin_processor.processor import STDIN, backslashed, parse_index_pattern
from stdin_processor import global_args
import re
from pathlib import Path

def _split(string, **kwargs):
    index_pattern = kwargs.get('index_pattern', None)
    split_separators = kwargs.get('split_separators', [' '])
    split_joiner = kwargs.get('split_joiner', ' ')

    s = string
    backslashed_separators = map(backslashed, split_separators)
    regex_pattern = '|'.join(backslashed_separators)
    split_string = re.split(regex_pattern, s)

    while '' in split_string: split_string.remove('')

    if index_pattern:
        targets = parse_index_pattern(split_string, index_pattern)
        matched = [split_string[i] for i in range(len(split_string)) if i in targets]
        return split_joiner.join(matched)
    else:
        return split_joiner.join(split_string)




def split(split_separators: List[Path] = typer.Argument(..., help='Separators to split each element of stdin with'),
split_joiner: str = typer.Option(' ', '--split-join', '--sj', metavar='JOINER', help='Joiner to join the splitted element of stdin with'),
position: str = typer.Option(None, '--position', '-p', help='Index patterns'),

           ____________________________: str = global_args.args_separator,
           separators: List[str] = global_args.separators,
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
    stdin.process(lambda x: _split(x, split_separators=[x.name for x in split_separators], split_joiner=split_joiner, index_pattern=position),
                  separators=separators,
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
