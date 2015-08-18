# Configuration Submodule

## Why this submodule / why not just use `configparser` or `json`?

In 2004, there was apparently some kind of giant configuration fracas in the python community. The discussion, eventually archived as the ["ConfigParserShootout"](https://wiki.python.org/moin/ConfigParserShootout) on the python wiki, attempted (and ultimately failed) to define everything from a standard format for python configuration to a standard mindset when dealing with configuration in python.

Sadly, the main consequence of all the (generally insightful) discussion was simply a list of 12 wildly different implementations of what a configuration library would look like. Most are now no longer maintained. Almost all focus on configuration file formats / the parsing. In the intervening 11 years, none of these alternatives have risen to compete with the bare bones `ConfigParser`/`configparser`, which uses pretty standard INI files, and has a pretty messy and confusing API.

There are some real gems in the Shootout. To list a few:

* "[T]his is a problem which is being solved again and again, maybe the Python library should be providing mechanism \*and\* policy here." --JohannesGijsbers

* "A hierarchical "key" or "namespace" scheme should exist so that multiple settings may be stored in the user configuration file." --dan.gass

There are also some portions that, in developing `orphanblack` I have come to vehemently disagree with.

* "I don't believe that a configuration module should need to interface directly to command line options. Rather, an application should inspect command line arguments, select one or more configuration files to load, and then examine the configuration data together with command line options to determine behaviour." --JohannesGijsbers

TODO: Indent response

** This comes from an argument between JohannesGijsbers and VinaySajip about a more general problem: merging potentially conflicting configurations and handling overriding values. In my experience, while the code to define defaults / overriding / handle CLI flags is simple, it is also repetitive, a tad tricky to get right, and bug-prone. It's also effectivly duplicated work, especially if both the config parameters and the CLI options are documented with help information or defaults. Almost every CLI application needs this behavior, so while it's important that any configuration library work without a CLI, it's also essential that the common CLI use cases (i.e. overriding, flag generation, etc.) are supported.

* dan.gass and a few others advocate for a way to include Python objects / use python files as configuration files.

** This gets properly shot down by others, but sometimes for weird reasons. VinaySajip says he's "not so much [concerned about] bad guys in black hats", and is instead worried that's it's simply bad form to have arbitrary executable content in configuration files from a software development perspective. While I agree that this is sufficient reason to reject executable config files, I also think that the security concerns are inescapable. In fact, I'd advocate for type checking config files as much as possible from both a security and software engineering perspective.

## Thoughts

I think a lot of the (false) dichotomies from Shootout relate to the fact that while configuration files are usually arbitrary key-value stores, there's also an *implicit* schema for configuration files. For the most part, only certian keys will ever be checked, and the values associated with those keys will only ever be ingested certian ways. There are even certian key-value pairs that applications require to function. The config file-format, however nice it is, will never define this schema without being too bulky to be practical.

The way to create a pythonic solution to this problem is to put the solution where the problem is; give the user tools to explicitly express this schema without interrupting their workflow.

Furthermore, by focusing unduely on the configuration format -- and indeed by voicing their displeasure with exisiting, the Shootout missed an essential point about conflicting standards and how to deal with them:

[![See XKCD 927](https://imgs.xkcd.com/comics/standards.png)](https://xkcd.com/927/)

An enduring configuration tool shouldn't be tied to a single standard. As much as possible, it shouldn't even require the end user to think about what standard they're using. Whatever Lexer/Parser they choose should be mostly uncoupled from the process of getting values out of a file and putting them into a program where they need to go. Changing from INI to JSON should be a one-line change, not a half hour of tedious code review.

## A (new?) Model

Within a program, the developer defines a number of `ConfigurationParameter` objects. These describe keys that the program expects to find. They may be as simple as a name (and in many contexts, a string containing the name can be substituted!), but they can also contain information like default values, typing information, and secondary names that parameters might be stored under.

At runtime, a `Parser` acts on file and produces a `Configuration` object. This is essential a fancy key value store that also supports things like multiple values and sections in keys. Importantly the `Configuration` object is language agnostic. In fact, most of the time, the only thing it's used for is `resolve`ing `ConfigurationParameter` objects.

### Nuts and bolts of `resolve`

Can `raise` one of only a few exceptions:

1. A `ConfigurationKeyError` if the parameter does not match any of the provided keys.
2. A `MismatchedTypeError` indicates that while a value was found, that value could not be interpreted consistent with the typing information in the parameter.


## Valid parameter names

By convention, parameter names should be valid python names, except that they may contain dash characters (`-`). These will be converted to underscores (`_`) in the parameter's "safe name" (`parameter.safe_name`), to ensure they can be used in python code. In particular, names must NOT include periods (`.`) or brackets (`[` or `]`).

TODO: Escape these somehow if they occur in existing configs?

### Sections

Parameters may be associated to sections (and in some cases sub-sections and so on). These parameters are denoted with a dot (`.`) as in `"section.parameter"`. They may also be accessed in config objects as `config.section_safe_name.safe_name`.

### Multi-value Parameters

Parameters may have multiple values. These parameters are list-valued when accessed in python. They can be indavidually accessed with indexed names (e.g. `"parameter[2]"`) or directly from a configuration object (e.g. `config.safe_name[2]`)