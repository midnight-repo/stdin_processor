import re
import sys
import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args
from stdin_processor.processor import backslashed

def _remove(line, **kwargs):
    charset = kwargs.get('charset', None)
    # strings = kwargs.get('strings', None)
    regular_expressions = kwargs.get('reg_expressions', None)
    ignore_case = kwargs.get('ignore_case', False)

    s = line

    if regular_expressions:
        for regex in regular_expressions:
            matches = re.compile(regex, re.IGNORECASE) if ignore_case else re.compile(regex)
            s = matches.sub('', s)

    # if strings:
    #     for string in strings:
    #         matches = re.compile(re.escape(backslashed(string)), re.IGNORECASE) if ignore_case else re.compile(re.escape(backslashed(string)))
    #         s = matches.sub('', s)

    if charset:
        bs_charset = backslashed(charset)
        for char in bs_charset:
            s = s.replace(backslashed(char), '')

    return s



def remove(regex: List[str] = typer.Option(None, '--regex', '-e', metavar='REGEX', help='The regexes to remove from stdin. Can be used multiple times'),
           # strings: List[Path] = typer.Option(None, '--string', '-s', metavar='STRING', help='Remove string from stdin. Can be used multiple times'),
           charset: str = typer.Option(None, '--charset', '-c', metavar='STRING', help='The charset to remove from stdin'),
           remove_ignore_case: bool = typer.Option(False, '--ic', '--rI', help='Ignore case for targets to remove, do not confuse with -I that is used with global option --where'),
           remove_clean: bool = typer.Option(True, '--remove-clean/--no-remove-clean', '--rc/--nrc', help='Don\'t print lines that are empty after removal'),
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
    # add this and uncomment in _remove() function to add support for strings
    # strings = map(lambda posisxp: posisxp.name, strings)
    stdin.process(lambda x: _remove(x, reg_expressions=regex, charset=charset, ignore_case=remove_ignore_case),
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

    if remove_clean:
        cleaned = join.join([x for x in stdin.value.split(join) if x != ''])
        print(cleaned)
    else:
        print(stdin.value, end='' if stdin.value.endswith('\n') else '\n')
