import re

import typer
from typing import List, Tuple
from stdin_processor.processor import STDIN
from stdin_processor import global_args
from stdin_processor.processor import backslashed
from pathlib import Path

def _remove(line, **kwargs):
    charset = kwargs.get('charset', None)
    strings = kwargs.get('strings', None)
    reg_expressions = kwargs.get('reg_expressions', None)
    ignore_case = kwargs.get('ignore_case', False)

    s = line

    if reg_expressions:
        for regex in reg_expressions:
            matches = re.compile(regex, re.IGNORECASE) if ignore_case else re.compile(regex)
            s = matches.sub('', s)

    if strings:
        for string in strings:
            matches = re.compile(re.escape(backslashed(string)), re.IGNORECASE) if ignore_case else re.compile(re.escape(backslashed(string)))
            s = matches.sub('', s)

    if charset:
        bs_charset = backslashed(charset)
        for char in bs_charset:
            s = s.replace(backslashed(char), '')

    return s



def remove(regex: List[Path,] = typer.Option(None, '--regex', '-r', metavar='REGEX', help='The regexes to remove from stdin. Can be used multiple times'),
           strings: List[Path] = typer.Option(None, '--string', '-s', metavar='STRING', help='Remove string from stdin. Can be used multiple times'),
           charset: str = typer.Option(None, '--charset', '-c', metavar='STRING', help='The charset to remove from stdin'),
           remove_ignore_case: bool = typer.Option(False, '--ic', '--rI', help='Ignore case for targets to remove, do not confuse with -I that is used with global option --where'),
           clean: bool = typer.Option(True, '--clean/--no-clean', '-c/--nc', help='Don\'t print lines that are empty after removal'),
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
    stdin.process(lambda x: _remove(x, reg_expressions=map(lambda posisxp: posisxp.name, regex), strings=map(lambda posisxp: posisxp.name, strings), charset=charset, ignore_case=remove_ignore_case),
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

    if clean:
        cleaned = join.join([x for x in stdin.value.split(join) if x != ''])
        print(cleaned)
    else:
        print(stdin.value, end='\n' if '\n' in separators else '')
