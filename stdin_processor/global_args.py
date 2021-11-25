import typer

#/!\ ADDING typer.style() instead of ARGS MAKES THEM NOT DETECTABLE BY ARGPARSER !


separators = typer.Option(['\n'],
                   '--separator',
                   '--sep',
                   metavar='SEPARATOR',
                   show_default=False,
                   help='The separator to use for stdin. This option can be used multiple times [default: "\\n"]')



join = typer.Option('\n',
                   '--join',
                   '-j',
                   metavar='JOINER',
                   show_default=False,
                   help='The character to use to join stdin [default: "\\n"]')


group_join = typer.Option(' ',
                   '--group-join',
                   '--gj',
                   metavar='JOINER',
                   help='The character to use to join elements of a same group when using -g/--group-by')

group_by = typer.Option(1,
                         '--group-by',
                         '-g',
                         metavar='GROUP_SIZE',
                         help='Chunks stdin elements by groups of a defined size')

where = typer.Option('.*\n*\r*\t*',
                     '--where',
                     '-w',
                     metavar='REGEX',
                     show_default=False,
                     help='Only process elements where regex is matched [default: .*\\n^\\r*\\t* (ALL)]')
_not = typer.Option(False,
                    '--not',
                    '-n',
                    help='What is matched is not and what is not is matched. Use with --where or --index')
ignore_case = typer.Option(False,
                           '--ignore-case',
                           '-I',
                           help='Ignore case when using --where option')

keep = typer.Option(True,
                    '--keep/--no-keep',
                    '-k/--nk',
                    help='Keep the elements that that did not match --where or --index')


unique = typer.Option(False,
                     '--unique/--no-unique',
                     '-u',
                     help='Removes duplicate values ; do not print an element that has already been printed')



sort = typer.Option('False',
                    metavar='PATTERN',
                    help='Sort stdin with PATTERN. PATTERN should contain 4 characters, one of each of those type: <digit>, <special character>, <uppercase character>, <lowercase character> [ex: !Xx3 or Hr:8 or 9zP?]' )





index = typer.Option('0:',
                     '--index',
                     '-i',
                     help='Comma separated list of indexes or ranges to show [ex: 0,:4,6:10,:-1] [default: 0: (ALL)]',
                     show_default=False,
                     metavar='INDEXES')



args_separator = typer.Option('',
                              typer.style('=========  The options listed below are common to all commands  =========', fg=typer.colors.BRIGHT_WHITE),
                              show_default=False,
                              metavar='')
