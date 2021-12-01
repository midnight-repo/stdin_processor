import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args


def _wrap(string, **kwargs):
    prefix = kwargs.get('prefix')
    suffix = kwargs.get('suffix')
    s = string

    wrapper = {
        'double_quote': lambda x: f'"{x}"',
        'quote': lambda x: f"'{x}'",
        'back_quote': lambda x: f"`{x}`",
        'parentheses': lambda x: f"({x})",
        'brackets': lambda x: f"[{x}]",
        'curly_brackets': lambda x: "{%s}" % x,
        'ltgt': lambda x: f"<{x}>",
        'tag': lambda x, tag: f"<{tag}>{x}</{tag}>"
    }

    for element in kwargs:
        if kwargs[element] != False:
            if type(kwargs[element]) == bool:
                s = wrapper[element](s)
            elif element == 'tag' and kwargs[element] != ('',):
                print(element, kwargs[element])
                for tag_name in kwargs[element]:
                    s = wrapper[element](s, tag_name)

    return prefix + s + suffix


def wrap(prefix: str = typer.Argument('', help='Prefix to add'),
         suffix: str = typer.Argument('', help='Suffix to add'),
         quote: bool = typer.Option(False, '--quote', '-q', help='Wraps element with quotes'),
         double_quote: bool = typer.Option(False, '--double-quote', '--dq', help='Wraps element with double quotes'),
         back_quote: bool = typer.Option(False, '--back-quote', '--bq', help='Wraps element with back quotes'),
         parentheses: bool = typer.Option(False, '--parentheses', '-p', help='Wraps element with parentheses'),
         brackets: bool = typer.Option(False, '--brackets', '-b', help='Wraps element with brackets'),
         curly_brackets: bool = typer.Option(False, '--curly-brackets', '--cb', help='Wraps element with curly brackets'),
         ltgt: bool = typer.Option(False, '--ltgt', '-l', help='Wraps element with <>'),
         tag: List[str] = typer.Option([''], '--tag', '-t', metavar='TAG_NAME', help='Wraps element with <TAG_NAME> </TAG_NAME>. Can be used multiple times'),

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
    stdin.process(lambda x: _wrap(x,
                                  prefix=prefix,
                                  suffix=suffix,
                                  quote=quote,
                                  double_quote=double_quote,
                                  back_quote=back_quote,
                                  parentheses=parentheses,
                                  brackets=brackets,
                                  curly_brackets=curly_brackets,
                                  ltgt=ltgt,
                                  tag=tag),
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

    print(stdin.value, end='' if stdin.value.endswith('\n') else '\n')
