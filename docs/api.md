*NOTE: This section describes a feature that will be implemented in future versions. Actual support may be buggy or nonexistent.*

# Client API

The Client API has two major purposes:

1. Allow the automation and programmatic configuration of scans.
2. Allow fine grained / easy access to reports.

## Samples

```
import orphanblack

files = orphanblack.load_file_manifest('my_special_manifest.in') # This returns an iterator that will produce files to be scanned.

config = orphanblack.load_config('my_custom_conf.conf') # Produces a Configuration object.
config.scan.distance_threshold = foo()

report = orphanblack.scan(files, config) # Produces a Report object.

report.save('.orphanblack')
```

```
import orphanblack
report = orphanblack.load_report('.orphanblack')

for clone in report.clones:
  print clone.name

print report.parameters.distance_threshold
```

# Plugin API

The purpose of the plugin API is to allow `orphanblack` to use other parsers and therefore extend to new languages. It is first-and-foremost a tool for developers and is not exposed outside of `orphanblack`.

TODO: Document once written / refactor pythoncompiler to use.