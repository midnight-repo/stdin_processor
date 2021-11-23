import re
import sys
import string as chars
import typer



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


# WHAT IT DOES : Generates a regex that can be used by re.split() to split a string by multiple separators
# HOW IT WORKS : Escaoes every character that is used in the regex synthax, this is used to neutralize regex operators in the separators
# joins with the OR regex operator "|"
# returns a regex like : escaped_separator|escaped_separator|escaped_separator
def regex_escape(*separators):
    regex_synthax_chars = list('[]{}^$.*?!,-|') + ['\d', '\D', '\w', '\W', '\s', '\S']

    escaped_separators = []
    for separator in separators:
        escaped_separator = ''.join(map(lambda x: '\\' + x if x in regex_synthax_chars else x, list(separator)))
        escaped_separators.append(escaped_separator)

    return '|'.join(escaped_separators)




class STDIN():
    def __init__(self):
        self.value = sys.stdin.read()


    # WHAT IT DOES : splits self.value by one or more separators
    def split(self, *separators):
        stdin = self.value
        backslashed_separators = map(backslashed, separators)
        split_stdin = re.split(regex_escape(*backslashed_separators), stdin)

        while '' in split_stdin: split_stdin.remove('')

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
    #   - creates a list of each of the categories mentionned above
    #   - sends each element of stdin to its corresponding list
    #   -
    def sort(self, order_pattern):

        elements = self.value

        if order_pattern == False:  # keep it as a string since cannot address value when typer argument is bool
            return
        elif len(order_pattern) != 4:
            typer.echo(typer.style("The sort pattern should contain 4 characters", fg=typer.colors.RED))
            exit()

        special_chars = [char for char in chars.printable if not char in chars.ascii_letters + chars.digits]

        # check if valid pattern
        p = []
        for char in order_pattern:
            if char in special_chars: p.append('special_chars')
            elif char.isupper(): p.append('upper')
            elif char.islower(): p.append('lower')
            elif char.isdigit(): p.append('digits')
        if all(x in p for x in ['special_chars', 'upper', 'lower', 'digits']):

            categories = {
                'special_chars': [x for x in chars.printable if not x in chars.ascii_letters + chars.digits],
                'upper': chars.ascii_uppercase,
                'lower': chars.ascii_lowercase,
                'digits': chars.digits
            }

            # categorise input elements
            sorted_categories = {}
            for category in p:
                l = []
                for element in elements:
                    if len(element) != 0:
                        if element[0] in categories[category]:
                            l.append(element)
                sorted_categories[category] = sorted(l)

            # return in order
            sorted_elements = []
            for category in p:
                if sorted_categories[category]:
                    sorted_elements += sorted_categories[category]

            self.value = sorted_elements
            return self.value

        else:
            typer.echo(typer.style("Something's wrong with the sort pattern", fg=typer.colors.RED))
            exit()


    # WHAT IT DOES : flags the input elements that match the regex passed to --where and --not
    # HOW IT WORKS :
    #   -
    def where(self, regex, ignore_case, **kwargs):
        keep = kwargs.get('keep', True)
        _not = kwargs.get('_not', False)

        matched = []
        condition = re.compile(regex, re.IGNORECASE) if ignore_case else re.compile(regex)

        for element in self.value:
            match = condition.match(element)
            if _not == True:
                match = not match

            matched.append({'value': element,
                            'keep': True if match else keep,
                            'match': True if match else False})


        self.value = matched
        return self.value



    # WHAT IT DOES : flags the elements of input if they correspond to the indexes mentionned in the --index option
    # Doesn't change the order even if --indexes is not ordered
    # HOW IT WORKS:
    #   -
    def indexes(self, indexes, **kwargs):
        keep = kwargs.get('keep', True)
        _not = kwargs.get('_not', False)

        try:
            patterns = [x for x in indexes.replace(' ', '').split(',')]

            # To not have duplicates but still keep the same order, we parse the indexes and add them in a sorted array
            # ex : [5:10] becomes [5,6,7,8,9]
            stdin_length = len(self.value)
            indexed = []
            for pattern in patterns:
                index = pattern

                if not ':' in index:
                    if not int(index) in indexed:
                        if '-' in index:
                            index = stdin_length + 1 - int(index.replace('-', ''))
                        indexed.append(index)


                else:

                    # :-2
                    if index.startswith(':'):
                        index = index.replace(':', '')
                        if '-' in index:
                            index = stdin_length + 1 - int(index.replace('-', ''))
                        for i in range(0, int(index)):
                            if not i in indexed:
                                indexed.append(i)

                    # 5:
                    elif index.endswith(':'):
                        index = index.replace(':', '')
                        if '-' in index:
                            index = stdin_length + 1 - int(index.replace('-', ''))
                        for i in range(int(index), stdin_length):
                            if not i in indexed:
                                indexed.append(i)

                    # 7:12
                    else:
                        start = index.split(':')[0]
                        if '-' in start:
                            start = stdin_length + 1 - int(start.replace('-', ''))

                        end = index.split(':')[1]
                        if '-' in end:
                            end = stdin_length + 1 - int(end.replace('-', ''))

                        for i in range(int(start), int(end)):
                            if not i in indexed:
                                indexed.append(i)



            matched = []
            for i in range(len(self.value)):
                match = i in indexed
                if _not:
                    match = not match

                matched.append({'value': self.value[i]['value'],
                                'keep': True if match else keep,
                                'match': True if match else False})

            self.value = matched
            return self.value


        except Exception as e:
            raise e
            typer.echo(e)
            typer.echo(typer.style('Something\'s wrong with the index pattern or you tried to process a sub element that does not exist', fg=typer.colors.RED))
            exit()



    def map(self, func):

        #TODO: maybe think about what if func takes more than 1 parameter
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
        group_by = kwargs.get('group_by', 1)
        group_join = kwargs.get('group_join')
        unique = kwargs.get('unique', False)
        sort = kwargs.get('sort', False)
        keep = kwargs.get('keep', '')
        where = kwargs.get('where', '.*|\n*|\r*|\t*')
        indexes = kwargs.get('indexes', '0:')
        _not = kwargs.get('_not', False)
        ignore_case = kwargs.get('ignore_case', False)
        joiner = kwargs.get('joiner', '\n')



        self.split(*separators)
        if group_by > 1:
            self.group_by(group_by, group_join)

        if sort != 'False':
            self.sort(sort)

        if where == '.*\n*\r*\t*':
            self.value = [{'value': x, 'keep': True, 'match': True} for x in self.value]
        else:
            self.where(where, ignore_case, keep=keep, _not=_not)

        if indexes != '0:':
            self.indexes(indexes, keep=keep, _not=_not)

        self.map(map_function)

        if unique:
            self.remove_duplicates()

        self.join(joiner)
        return self.value


#
# stdin = STDIN()
# s = stdin.split('\n', '\t')
# s = stdin.group_by(2, '::::')
# s = stdin.join('\t')
#
# print(s)

# TODO: clean the code for sorted
