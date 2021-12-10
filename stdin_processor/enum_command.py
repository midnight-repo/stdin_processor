import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args
import sys

i = 0
enum_initialized = False
def _enum(line: str, start: int, bound: int, **kwargs):
    beginning = kwargs.get('beginning', True)
    ending = kwargs.get('ending', False)
    num_format = kwargs.get('num_format', ' ')

    l = line
    global i
    global enum_initialized


    if enum_initialized == False:
        i = start
        enum_initialized = True

        if beginning: l = str(i) + num_format + l
        if ending: l = l + num_format + str(i)
        i += bound

    else:
        if beginning: l = str(i) + num_format + l
        if ending: l = l + num_format + str(i)
        i += bound

    return l




def enum(start: int = typer.Option(0, metavar='START', help='Starts to enumerate from START'),
         beginning: bool = typer.Option(True, '--beginning/--no-beginning', '--beg/--nb', help='Adds the number at the begenning of the line'),
         ending: bool = typer.Option(False, '--ending/--no-ending', '-e/--ne', help='Adds the number at the end of the line'),
         bound: int = typer.Option(1, '--bound', '-b', metavar='BOUND', help='Increase by BOUND for each line'),
         format: str = typer.Option(' ', '--format', '-f', metavar='STR', show_default=False, help='String to add after number if --beginning or before number if --ending [default: " "]'),

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
    stdin.process(lambda x: _enum(x, start, bound, beginning=beginning, ending=ending, num_format=format),
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
