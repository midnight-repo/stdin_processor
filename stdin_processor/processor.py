import re
import string as chars
from collections import deque
import typer
import random


# WHAT IS DOES : this is used to read line feed, carriage return and tab characters as arguments or options from the command line
# HOW IT WORKS : replace '\\n' with '\n'
def backslashed(string):
    s = string
    backslash_chars = {
        '\\n': '\n',
        '\\r': '\r',
        '\\t': '\t'
    }
    for char in backslash_chars:
        if char in s or char == s:
            s = s.replace(char, backslash_chars[char])
    return s





# WHAT IT DOES : parses pattern index and returns a list containing targetted indexes
def parse_index_pattern(target_list, index_pattern):
    try:
        # this is just in case of spaces in the pattern
        patterns = [x for x in index_pattern.replace(' ', '').split(',')]

        while '' in patterns: patterns.remove('')

        list_length = len(target_list)
        indexed = []
        for pattern in patterns:
            index = pattern

            if not ':' in index:
                if '-' in index:
                    index = list_length - int(index.replace('-', ''))
                index = int(index)
                if not index in indexed:
                    indexed.append(index)

            else:

                # :-2
                if index.startswith(':'):
                    index = index.replace(':', '')
                    if '-' in index:
                        index = list_length - int(index.replace('-', ''))
                    for i in range(0, int(index)):
                        if not i in indexed:
                            indexed.append(i)

                # 5:
                elif index.endswith(':'):
                    index = index.replace(':', '')
                    if '-' in index:
                        index = list_length - int(index.replace('-', ''))
                    for i in range(int(index), list_length):
                        if not i in indexed:
                            indexed.append(i)

                # 7:12
                else:
                    start = index.split(':')[0]
                    if '-' in start:
                        start = list_length - int(start.replace('-', ''))

                    end = index.split(':')[1]
                    if '-' in end:
                        end = list_length - int(end.replace('-', ''))

                    for i in range(int(start), int(end)):
                        if not i in indexed:
                            indexed.append(i)


        return sorted(indexed)

    except:
        typer.echo(typer.style('Invalid index pattern', typer.colors.RED))
        exit()




# This class represents standard input and contains methods to manipulate it
class STDIN():
    def __init__(self, string_value):
        self.value = string_value


    # WHAT IT DOES : splits self.value by one or more separators
    # HOW IT WORKS : joins the regex escaped separators with 'OR' regex operator : '|'
    # returns a regex like : escaped_separator|escaped_separator|escaped_separator
    # split with re.split(regex)
    def split(self, *separators, **kwargs):
        clean = kwargs.get('clean', True)

        stdin = self.value
        backslashed_separators = map(backslashed, separators)
        regex_pattern = '|'.join([re.escape(separator) for separator in backslashed_separators])
        split_stdin = re.split(regex_pattern, stdin)

        if clean:
            while '' in split_stdin:
                split_stdin.remove('')

        self.value = split_stdin
        return self.value

    # WHAT IT DOES : groups elements of split stdin in subgroups of group_size and join elements of subgroups with group_join
    def group_by(self, group_size, subgroup_join):
        gj = backslashed(subgroup_join)
        grouped = [self.value[i:i + group_size] for i in range(0, len(self.value), group_size)]

        self.value = [gj.join(group) for group in grouped]
        return self.value



    # WHAT IT DOES : joins self.value with joiner
    def join(self, joiner):
        j = backslashed(joiner)
        joined = j.join(self.value)

        self.value = joined
        return self.value





    # WHAT IT DOES : removes duplicates from self.value without changing the order
    def remove_duplicates(self):
        without_duplicates = []
        for element in self.value:
            if not element in without_duplicates:
                without_duplicates.append(element)

        self.value = without_duplicates
        return self.value



    # WHAT IT DOES : sorts self.value in the order provided in the order_pattern which must contain
    #   - one uppercase char
    #   - one lowercase char
    #   - one digit
    #   - one special character

    # HOW IT WORKS :
    #   - categorizes each element to a category
    #   - sorts each category
    #   - appends each sorted category to the final list in the order mentioned in the pattern
    def sort(self, order_pattern, **kwargs):
        sort_key = kwargs.get('sort_key', None)

        if order_pattern == 'False':  # keep it as a string since cannot address value when typer argument is bool
            return
        elif len(order_pattern) != 4:
            typer.echo(typer.style("The sort pattern should contain 4 characters", fg=typer.colors.RED))
            exit()

        # check if valid pattern
        special_chars = [char for char in chars.printable if not char in chars.ascii_letters + chars.digits]
        pattern_categories = []
        for char in order_pattern:
            if char in special_chars: pattern_categories.append('special_chars')
            elif char.isupper(): pattern_categories.append('upper')
            elif char.islower(): pattern_categories.append('lower')
            elif char.isdigit(): pattern_categories.append('digits')
        if all(x in pattern_categories for x in ['special_chars', 'upper', 'lower', 'digits']):
            elements = self.value

            categories = {
                'special_chars': [x for x in chars.printable if not x in chars.ascii_letters + chars.digits],
                'upper': chars.ascii_uppercase,
                'lower': chars.ascii_lowercase,
                'digits': chars.digits
            }

            # categorise input elements
            sorted_categories = {}
            for category in pattern_categories:
                l = []
                for element in elements:
                    if len(element) != 0:
                        if element[0] in categories[category]:
                            l.append(element)

                if sort_key:
                    k = {}
                    for x in l:
                        m = re.search(sort_key, x)
                        k[x] = m[0] if m else x
                    sorted_categories[category] = sorted(l, key=lambda x: k[x])
                else:
                    sorted_categories[category] = sorted(l)

            # return in order
            sorted_elements = []
            for category in pattern_categories:
                if sorted_categories[category]:
                    sorted_elements += sorted_categories[category]

            self.value = sorted_elements
            return self.value

        else:
            typer.echo(typer.style("Something's wrong with the sort pattern", fg=typer.colors.RED))
            exit()


    def match(self, *regex, ignore_case, index_pattern, **kwargs):
        keep = kwargs.get('keep', True)
        _not = kwargs.get('_not', False)

        flagged = []


        # WHERE
        match_index = 0
        for element in self.value:
            matched = False
            for exp in regex:
                condition = re.compile(exp, re.IGNORECASE) if ignore_case else re.compile(exp)
                if condition.search(element):
                    matched = True
                    continue

            if _not == True:
                matched = not matched

            flagged.append({'value': element,
                            'keep': True if matched else keep,
                            'match': True if matched else False,
                            'match_index': match_index if matched else None})
            if matched: match_index += 1

        # INDEX
        indexed = parse_index_pattern([x for x in flagged if x['match'] == True], index_pattern)

        for i in range(len(flagged)):
            flagged[i]['match'] = True if flagged[i]['match_index'] in indexed else False
            flagged[i]['keep'] = True if flagged[i]['match_index'] in indexed else keep

        self.value = flagged
        return self.value


    # process the elements that are flagged with match=True
    def map(self, func):

        processed = []
        for element in self.value:
            if element['keep'] == True:
                if element['match'] == True:
                    processed.append(func(element['value']))
                if element['match'] == False:
                    processed.append(element['value'])
            else:
                continue

        self.value = processed
        return self.value



    def process(self, map_function, **kwargs):
        separators = kwargs.get('separators', ['\n'])
        clean = kwargs.get('clean', True)
        group_by = kwargs.get('group_by', 1)
        group_join = kwargs.get('group_join')
        unique = kwargs.get('unique', False)
        shuffle = kwargs.get('shuffle')
        sort = kwargs.get('sort', False)
        sort_key = kwargs.get('sort_key', None)
        keep = kwargs.get('keep', '')
        where = kwargs.get('where', ['.*|\n*|\r*|\t*'])
        indexes = kwargs.get('indexes', '0:')
        _not = kwargs.get('_not', False)
        ignore_case = kwargs.get('ignore_case', False)
        rotation = kwargs.get('rotation', 0)
        joiner = kwargs.get('joiner', '\n')



        self.split(*separators, clean=clean)

        if group_by > 1:
            self.group_by(group_by, group_join)

        if rotation != 0:
            val = deque(self.value)
            val.rotate(rotation)
            self.value = val

        # needs to be there for enum
        if shuffle:
            random.shuffle(self.value)


        self.match(*where, ignore_case=ignore_case, index_pattern=indexes, keep=keep, _not=_not)

        self.map(map_function)

        if unique:
            self.remove_duplicates()


        # before or after processing ? if prepend --where for exemple
        if sort != 'False':
            self.sort(sort, sort_key=sort_key)


        self.join(joiner)

        return self.value




