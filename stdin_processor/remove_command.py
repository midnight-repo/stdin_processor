import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args
from stdin_processor.processor import backslashed

def _remove(line, *strings, **kwargs):
    charset = kwargs.get('charset', None)

    s = line

    if len(strings) == 0:
        pass
    else:
        for string in strings:
            s = s.replace(backslashed(string), '')

    if charset:
        bs_charset = backslashed(charset)
        for char in bs_charset:
            s = s.replace(backslashed(char), '')

    return s



def remove(charset: str = typer.Option(None, '--charset', '-c', metavar='STRING', help='The charset to remove from stdin'),
           strings: List[str] = typer.Option([], '--string', '-s', metavar='STRING', help='Remove string from stdin'),

           ____________________________: str = global_args.args_separator,
           separators: List[str] = global_args.separators,
           group_by: int = global_args.group_by,
           group_join: str = global_args.group_join,
           join: str = global_args.join,
           unique: bool = global_args.unique,
           sort: str = global_args.sort,
           keep: bool = global_args.keep,
           where: str = global_args.where,
           indexes: str = global_args.index,
           _not: bool = global_args._not,
           ignore_case: bool = global_args.ignore_case
           ):


    stdin = STDIN()
    stdin.process(lambda x: _remove(x, *strings, charset=charset),
                  separators=separators,
                  group_by=group_by,
                  group_join=group_join,
                  unique=unique,
                  sort=sort,
                  keep=keep,
                  where=where,
                  _not=_not,
                  ignore_case=ignore_case,
                  indexes=indexes,
                  joiner=join)

    print(stdin.value, end='\n' if '\n' in separators else '')
