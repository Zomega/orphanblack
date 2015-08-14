# Usage

Scanning a large project for clones can be a computationally intensive process. For this reason, `orphanblack` always persists the results so that they can later be explored and analysed without being recomputed.

In general, using orphanblack proceeds in two steps: first a scan is run indexing code and identifiying clones. Summary information is stored to disk in a file (usually `.orphanblack` in the current working directory). A second command is run to view or explore this summary information.

Various functions are accessed through subcommands, like `orphanblack scan` or `orphanblack report`.

## Additional documentation

In addition to this documentation, the CLI can automatically report compile and report help information associated with each command and subcommand.

```
orphanblack --help
```

Will list all avalible subcommands and their functions.

```
orphanblack scan --help
```

Will explain functionality specific to the `scan` subcommand.

Because this information is auto-generated from the code, it will always be up to date. Because the CLI is currently in a state of flux, I recommend using these resources (at least until 1.0.0 or later, when the changes needed to support multiple languages are added in; then meaningful documentation can be written.)

TODO: man page?
