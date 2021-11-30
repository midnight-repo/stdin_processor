# stdin_processor (sp)
## Introduction
Advanced stdin/stdout and string manipulation in BASH often requires knowledge of a certain set of tools ("sed", "head", "tail", "grep", "sort", "xargs", "expr","cut", "awk" ...) and going through a couple of help manuals or stackoverflow questions. As it is substancially achievable, it does nevertheless feel less intuitive than OOP which provides string and list methods for complex operations.
This tool aims to improve productivity by providing a simple yet complete toolbox with flexible and intuitive options completed with a wide variety of commands, making any avanced operation as **quick** as thinking about it, as **simple** as a few pipes and **easy to read**.

It is fully written in python3, making it availiable on Linux, Windows, MacOS, and it's is based on typer, which is based on click, a famous library for creating command line tools.

## Table of contents
[Installation](#installation)

[Quick start](#quick-start)
  
[How it works](#how-it-works)
  - [STDIN shaping](#stdin-shaping)
  - [Mapping](#mapping)
  - [Detailed steps](#detailed-steps)

[Usage examples](#usage-examples)

## Installation
Using pip or pip3 :

    pip install stdin_processor


Check if successful :

    sp --help


[OPTIONAL] Install tab auto-completion for your shell

    sp --install-completion bash|zsh|fish|powershell|pwsh

## Quick start
stdin_processor is availiable as "sp" for "**s**tdin **p**rocessor" in the terminal once installed.

Since the tool reads stadard input, the basic usage would imply piping the standard output to process to the sp command :

```cat file.txt | sp <command> <options>```

```echo hello world ! | sp <command> <options>```

For complex operations, you can use pipe chains :

    echo hello, world ! | sp replace hello goodbye | sp encode b64

The tool possesses two types of options, global and subcommand specific:

  - Global options :

      - They are common to all subcommands of the sp command.
    
      - Those options are used as kwargs for the "STDIN.process" method, and are used to custom shape the standard input, before processing it by the subcommand.

  - Subcommand specific options :

    - Thoses options as their name implies, are specific to the subcommand you are using.

    - Thoses are used to custom the way the subcommand should process each element of standard input.

To list availiable commands :

    sp --help

To view help for any command :

    sp <command> --help

## How it works
The way this tool works can be split in two distinct operations: 
  - STDIN shaping (represented by the global options)
  - Mapping (represented by the command specific options)

### STDIN shaping
The purpose of this step is mainly, to determine how the STDIN should be split.

The STDIN is read by the tool as one whole string block. It is then split into a list of elements. The default separator is the line feed "\n" to read the standard input line by line, but you can use custom separators with the --sep global option (usable multiple times if more than one separator is needed).

This step is done before calling the subcommand, and this is why it is represented by the global options which are common to all subcommands. 
### Mapping
At this point, the standard input has been split into distinct elements.
The process of mapping is simply to process every element with the subcommand. This is where subcommand specific options take place.

### Detailed steps
The whole process actually takes 7 steps.

Let's say you pipe the content of file.txt to the stdin_processor.

The tool now recieves the content as one whole string block.

  - Step 1 : SPLIT

The first step is to split the STDIN string block into different elements. By default, lines, using the line feed "\n" as a separator.

Multiple separators can be used.

    cat file.txt | sp <command> --sep \\n --sep '\t' --sep ' '

  - Step 2 : GROUP

The second step is to group elements if needed. Let's say you wanted the tool to read the file two lines by two lines, you can use the --group-by global option for that :

    cat file.txt | sp <command> --group-by 2

The STDIN in now split into a list of elements, each one represented by two lines of the file.

If needed, you can also specify how thoses two lines should be joined together with the --group-join option (the default being a simple space character).

  - Step 3 : FLAG MATCHING ELEMENTS

Sometimes you might not want to process all the elements, but just those that match a certain condition (regular expression). If that is needed, you can also specify if you want to keep or not the elements that did not match with the --keep global option (default is to keep).
    
    cat file.txt | sp <command> --where <regex>

The third step adds to each element with a "match" and "keep" flag, so the mapping step knows what to to with it.

This is technically done by converting an element, which at this point is a string, to a dictionnary with keys "match":bool, "keep":bool, "value":string value of the element

For extra specificity, you can also only target individual or ranges of elements in the ones that matched. You can use the --index global option, that reads python slicing patterns (without the brackets), comma separated.
a[start:stop]  # items start through stop-1
a[start:]      # items start through the rest of the array
a[:stop]       # items from the beginning through stop-1
a[:]           # a copy of the whole array

If for exemple you want to process only the first (0), and the two last elements(-2:) that matched :

    cat file.txt | sp <command> -i 0,-2:

  - Step 4 : MAPPING

**The mapping step is where the subcommand and its specific options takes place.**

For each element of STDIN, **if** the **MATCH** flag is **True**, return the subcommand **processed value** of the element

For each element of STDIN, **if** the **MATCH** flag is **False**, **if** the **KEEP** flag is **True**, the the **unchanged value** of the element is returned

**else** the element is **not kept**

  - Step 5: REMOVING DUPLICATES

The purpose of this step is simply to remove duplicate values from the element list. This is specified with the --unique global option, default being to not remove duplicates.

    cat file.txt | sp <command> -u

  - Step 6: SORT

In case the output needs to be sorted, it is done in the step 7.

You can sort the element list in the order you want passing a pattern to the --sort global option.

If a more specific sorting is needed, you can use the --sort-key <regex> global option. This will sort the list, depending on what was the matched the regex for each element
  
    cat file.txt | sp <command> --sort 'Aa0!' --sort-key <regex>
  
  - Step 7 : JOIN

The last and final step is to join the list of elements.
 
The joinder can be provided with the --join global option, the default being a line feed "\n", to print each element in a new line.

    cat file.txt | sp <command> -j '; '

## Usage examples
### show and hide commands

We will first learn how to use the show and hide commands since they are a bit particular.

In fact, they do not have any command specific option, and this is for a good reason : they do not perform any action on elements of stdin. Instead, they simply chose to keep them or not.
