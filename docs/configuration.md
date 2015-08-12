*NOTE: This section describes a feature that will be implemented in future versions. Actual support may be buggy or nonexistent.*

# Locations

The default behavior can be overridden through the use of configuration files. By default, `orphanblack` will check to see if a `.orphanblackrc` file is present in the current working directory. If no such file is present it will check to see if `~/.orphanblackrc` file exists (henceforth refered to as user defaults). Otherwise, `orphanblack` will pick sensible defaults (program defaults).

Any other file can be specified with the `--configuration <filename>` flag.

If `~/.orphanblack` exists, but should not be used for a particular run, there is a `--use-program-defaults` flag that will override all other settings (including `--configuration`).

## Format

Confguration files are formatted as classic INI files: sections are introduced by a `[section]` header, and contain `name = value` entries. Lines beginning with `#` or `;` are ignored as comments. Strings don’t need quotes. Multi-valued strings can be created by indenting values on multiple lines. Boolean values can be specified as on, off, true, false, 1, or 0 and are case-insensitive.

Names that orphanblack doesn't expect will be ignored. If a name is unspecified then it will be populated by the program default (NOT the user default).

## Sample

A sample configuration file follows:

```
# Sample .orphanblackrc
[scan]
branch = TODO

[report]
branch = TODO

[html]
directory = coverage_html_report
```

## Options

### `[scan]` section

#### clustering_threshold

#### size_threshold

#### distance_threshold

### `[report]` section

### `[html]` section