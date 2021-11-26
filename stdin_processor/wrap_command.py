import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args

def _wrap(string, **kwargs):
    quote = kwargs.get('quote', None)
    double_quote = kwargs.get('double_quote', None)
    back_quote = kwargs.get('back_quote', None)
    parentheses = kwargs.get('parentheses', None)
    brackets = kwargs.get('brackets', None)
    curly_brackets = kwargs.get('curly_brackets', None)
    ltgt = kwargs.get('ltgt', None)
    tag = kwargs.get('tag', None)

    s = string

    wrapper = {
        'double_quote': lambda x: f'"{x}"',
        'quote': lambda x: f"'{x}'",
        'back_quote': lambda x: f"`{x}`",
        'parentheses': lambda x: f"({x})",
        'brackets': lambda x: f"[{x}]",
        'curly_brackets': lambda x: "{%s}" % x,
        'ltgt': lambda x: f"<{x}>",
        'tag' : lambda x,tag: f"<{tag}>{x}</{tag}>"
    }

    for element in kwargs:
        if kwargs[element] != False:
            if type(kwargs[element]) == bool:
                s = wrapper[element](s)
            elif element == 'tag' and kwargs[element] != ['']:
                for tag_name in kwargs[element]:
                    s = wrapper[element](s, tag_name)

    return s


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
           group_by: int = global_args.group_by,
           group_join: str = global_args.group_join,
           join: str = global_args.join,
           unique: bool = global_args.unique,
           sort: str = global_args.sort,
           keep: bool = global_args.keep,
           where: List[str] = global_args.where,
           indexes: str = global_args.index,
           _not: bool = global_args._not,
           ignore_case: bool = global_args.ignore_case
           ):


    stdin = STDIN()
    stdin.process(lambda x: _wrap(prefix + x + suffix,
                                  quote=quote,
                                  double_quote=double_quote,
                                  back_quote=back_quote,
                                  parentheses=parentheses,
                                  brackets=brackets,
                                  curly_brackets=curly_brackets,
                                  ltgt=ltgt,
                                  tag=tag),
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
