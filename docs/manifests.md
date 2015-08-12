# Manifests

## File Manifests

When loading files into `orphanblack` for scanning you can specify a detailed manifest file and use that instead via the `--file-manifest` option. These manifests are based on the `MANIFEST.in` files used by `distutils`.

Each line must consist of EITHER a valid command (see below) or a comment, where the first non-whitespace character must be a pound symbol (i.e. `# This is a comment`). Because filenames and directories could include pound symbols and escaping is overcomplex for this, end of line comments are NOT allowed.

Valid commands and their formats:

| Command  | Arguments | Description |
| -------- | --------- | ----------- |
| include  | pat1 [pat2 ...]  | include all files matching any of the listed patterns |
| exclude  | pat1 [pat2 ...]  | exclude all files matching any of the listed patterns |
| explicit-include | file1 [file2 ...] | includes the listed files |
| explicit-exclude | file1 [file2 ...] | excludes the listed files |
| recursive-include  | dir pat1 [pat2 ...] | include all files under dir matching any pattern |
| recursive-exclude  | dir pat1 [pat2 ...] | exclude all files under dir matching any pattern |
| global-include | pat1 [pat2 ...] | include all files anywhere under the root matching any pattern |
| global-exclude | pat1 [pat2 ...] | exclude all files anywhere under the root matching any pattern |
| graft | dir | include all files under dir |
| prune | dir | exclude all files under dir |


An empty manifest file will produce no file matches (to override this, put `graft .` as the first line of your manifest, though this is not recommended). Commands are applied in the order they are given in the file: a later command can overrule an earlier one. Normally, early excludes will have little to no effect -- it is recommended (but not required) that manifest files list all `*-include` and `graft` statements before `*-exclude` and `prune` statements.

For clarification:

```
include *.txt
explicit-exclude example.txt
```

will not contain `example.txt`, but

```
explicit-exclude example.txt
include *.txt
```

will contain `example.txt` (though it will cause a warning in the log and on the console).

### Warnings and Errors

Manifest reading only produces errors (`ERROR`) if the Manifest file is

* non-existent
* unreadable
* contains invalid commands

In all these cases, `orphanblack` will assume the run is unrecoverable and terminate with `sys.exit(1)`.

So long as the manifest is parsed correctly, then only warnings will be issued. The manifest loading process will log `WARN` level commands in the following cases:

* An `explicit-include` or `explicit-exclude` references a file that does not exist or is not a file.
* A `recursive-include`, `recursive-exclude`, `graft`, or `prune` references a directory that does not exist.
* Any command uses a file where a directory was expected or vice versa.
* An explicitly included file is later excluded for any reason or vice versa.

TODO: Implement that last one.

### Default File Manifests

`orphanblack` comes packaged with a number of default manifests for common situations. In particular, every supported language has a default manifest that will be used if neither a manifest of an explicit list of files is provided. For instance, if `orphanblack scan` is run with `-l python`, then unless filenames are explicitly specified or a manifest is provided, the default `PYTHON_MANIFEST` will be used. This file contains the single rule

```
global-include *.py
```

TODO: Implement

## AST Manifests

*NOTE: This section describes a feature that will be implemented in future versions. Actual support may be buggy or nonexistent.*

Unlike file manifests, AST manifests include everything by default. Their primary purpose is to exclude analysis of classes and files by name.

`--ast-manifest`