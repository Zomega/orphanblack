import click

import click.types  # TODO: USE THIS TO DO TYPESTUFF STUFF!

# TODO: support multiple args. (i.e. lists in JSON)


# This (abstract) class holds the values from parsed configuration files, etc.
# Configurations can be edited manually, or processed via various provided
# functions. One of the most common operations is an "overlay", where a second
# configuration file overrides any values it has in common with the first.
#
# Another common operation is to expose a section of a Configuration as a
# first-class Configuration via the "section" function.
#
# Values may be extracted from Configurations manually or passed into functions
# that use the @parameter decorator.
class Configuration:
    def resolve(self, parameter):
        raise NotImplementedError()


class KVConfiguration:
    def __init__(self, data):
        self.data = data

    def resolve(self, parameter):
        if not parameter.name in self.data:
            return None
        return self.data[parameter.name]


# TODO: write this more carefully. Handle the nasty cases that might occur?
def parse_ini_config():
  import ConfigParser
  config = ConfigParser.ConfigParser()
  config.read('test.ini')
  sections = config.sections()
  for section in sections:
    options = config.options(section)
    for option in options:
        value = config.get(section, option)
        print section, option, value, type(value)

parse_ini_config()

# Valid parameter names
# =====================
#
# By convention, parameter names should be valid python names, except that they
# may contain dash characters (`-`). These will be converted to underscores
# (`_`) in the parameter's "safe name" (`parameter.safe_name`), to ensure they
# can be used in python code.
#
# Sections
# --------
#
# Parameters may be associated to sections (and in some cases sub-sections and
# so on). These parameters are denoted with a dot (`.`) as in `"section.parameter"`.
# They may also be accessed in config objects as `config.section.parameter`.
#
# Parameters may have multiple values. These parameters are list-valued when
# accessed in python. They can be indavidually accessed with indexed names
# (e.g. `"section.parameter[2]"`) or directly from a configuration object (e.g.
# `config.section.parameter[2]`)
#


# Holds data on a single parameter as used by functions, etc.
# NOTE: This class NEVER holds any actual configuration values.
# Instead it may be "resolved" against a Configuration to retrive
# its value in that particular configuration.
#
#  Usage Example
#  =============
#
#  >>> config = ... # Make a Configuration object
#  >>> param = ...  # Make a ConfigurationParameter
#  >>> config.resolve(param)
#  4  # The value of the parameter will show up here
#     # if the parameter is not resolved then "None"
#     # will appear instead. If a type-mismatch (or
#     # similar) occurs the appropriate exception
#     # will be raised.
class ConfigurationParameter:
    def __init__(self, name, type=None, default=None):
        self._name = name
        self._type = click.types.convert_type(type)
        self._default = None  # TODO: what if default *is* None? Make a NO_DEFAULT flag...

    @property
    def name(self):
        return self._name

    @property
    def safe_name(self):
        return self.name  # TODO: Sanitize

    @property
    def flag_name(self):
        return '--' + self.safe_name

    @property
    def type(self):
        return self._type

    @property
    def default(self):
        return self.default


#TODO: rename varaibles to parameters
def get_configuration_parameters(f):
    if hasattr(f, '_configuration_parameters'):
        return f._configuration_parameters
    return set()


# Decorator that allows configurations to seamlessly pass function arguments.
# Any parameter specified with this decorator will be given a value before the
# function is called. If no value can be resolved, then an exception will be
# raised.
#
#  Usage Example
#  =============
#
#  @parameter('size')
#  @parameter('shape')
#  @parameter('weight')
#  def print_some_values(size, shape, weight):
#    print size, shape, weight
#
#  config = ... # Generate a Configuration by any means.
#
#  print_some_values(config) # Will print values out so long as size, shape,
#  and weight are resolved in config. If one or more isn't resolved, a
#  UnresolvedParameterError will be raised.
#
# If a clear default value exists, use "@parameter('foo', default='bar')"
# To limit the types that will be allowed for the parameter, use
# "@parameter('foo', type=int)" etc. Note that this will cause a
# MismatchedTypeError to be raised in the event of a mismatched type.
#
# TODO: Optionally Take in a configparamter and translate.
# TODO: types, etc?
# TODO: Also, allow for extra args?
def parameter(name, type=None, default=None):
    def wrapper(f):
        def wrapped_f(*args):
            f(*args)
        param = ConfigurationParameter(name, type, default)
        wrapped_f._configuration_parameters = get_configuration_parameters(f)
        wrapped_f._configuration_parameters.add(param)

        return wrapped_f
    return wrapper


# A rather complex decorator that allows users to manually specify options
# for a given purpose at a CLI.
#
# Given a target function, creates a set of CLICK options that can be used to
# override the configured parameters.
#
# TODO: Add Configuration construction after the fact.
def generate_cli_config_options(target):
    def wrapper(f):
        wrapped_f = f
        for param in get_configuration_parameters(target):
            # TODO: better way to get the name of the configuration variable.
            # TODO: Help options from descriptions somewhere?
            # Note that the default is NOT passed so that it is clear which
            # options the user explicitly specified.
            wrapped_f = click.option(param.flag_name, type=param.type)(wrapped_f)  # "Setting up flag for", var
        return wrapped_f
    return wrapper


#@configured_with('file', FORMAT)
@parameter('a', type=int)
@parameter('b', type=(unicode, int))
@parameter('c')
@parameter('longname')
def test(a, b, c):
    print a, b, c

print get_configuration_parameters(test)


@click.command()
@generate_cli_config_options(test)
def cli(**kwargs):
    print "CLI...", kwargs

if __name__ == '__main__':
    cli()
