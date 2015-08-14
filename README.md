# `orphanblack`: Static Analysis for Software Clone Detection

Currently for Python only, with plans to extend to C++, Java and more!

## Installation
I think things are set up with PyPI such that

```
$ pip install orphanblack
```

should work. Because the software is in the early days, and this is my first python package, please forgive me if there are a few kinks.

## Usage
`orphanblack` is a complex tool with plenty of settings under the hood for both processing and display. Sensible defaults are used whenever possible. To get started, the following will analyse a single python module for clones.

```
$ cd path/to/your/code
$ orphanblack scan *.py

...

$ orphanblack report --verbose

Found 11 clones
...

```

It is also possible to output results as a webpage. After scanning code, just run

```
$ orphanblack html -o results.html
```

If no destination is specified, `orphanblack` will use `output.html` in the current directory.


## API

Not yet done, but on the way... for now, check out the Report class (`orphanblack/report.py`) which summarizes the results and should be fairly stable.

## Code Genealogy (How `orphanblack` Came To Be)
`orphanblack` is a direct code descendant of a [2008 package called `clonedigger`](http://clonedigger.sourceforge.net). I first stumbled on `clonedigger` in 2012 when examining other static analysis tools for python like pep8 and pyflakes, and really liked the concept. Sadly, I found the original code unusable for my purposes. I adapted the code several times in the intervening years, but always with limited success because of the convoluted inner workings of the package.

In the early summer of 2015, I switched to a new computer, inadvertantly deleting many of my modifications. I decided to bite the bullet and attempt a total refactor into something I found more palatable. I also wanted to create something that could play nicely with Sublime Text; a tool that could automatically run on every project -- python or otherwise -- I worked on. `orphanblack`, nicknamed after the clone-based BBC America series, is the result of my progress towards those goals.

The CLI and API are both inspired by [the wonderful dynamic analysis tool `coverage.py`](http://nedbatchelder.com/code/coverage), though there is no direct code relationship.

Because `clonedigger` is distributed under GPL3, I am forced to also use GPL3 in place of the MIT or LGPL3 liscences, which I personally prefer. I do not consider use of the `orphanblack` API to constitute incorporation and therefore to the greatest degree possible under the law I wish to allow the use of the API for even commercial purposes.

### A Short and Incomplete List of Improvements:
* Use [`Click`](http://click.pocoo.org/4/) in place of [`optparse`](https://docs.python.org/2/library/optparse.html) to simplify internal code.
* Use [`Jinja2` templating](http://jinja.pocoo.org/) to greatly simplify the previously ad-hoc production of HTML reports.
* Replace janky use of `arguments.py` globals with the `Parameters` class.
* Replace CLI with something a little less difficult to understand.
* Provide persistent, serialiazable results reports (stored in `.orphanblack` files when a scan is run.).
* Implement program-wide logging rather than ad-hoc error printouts.

#### Planned Features
* Grouping clones! Right now, if three regions of code are all similar to each other, three seperate clone reports, corresponding to each pair, are generated.
* An API, allowing integration with other linters and plugins.
* Other languages: So much of this work is already done. After just a little bit of internal rewriting, any language should be able to work with `orphanblack` just by providing an appropriate AST parser.
* Total internal rewrite, aiming for a well commented codebase.
* Diffs based on anti-unification patterns.
* ASTNode classes with built in anti-unification utilities
* Ability to handle sequences elegantly (i.e. deal with insertion / removal in edit distances)
* Configurations! (How this is implemented internally is something that I've had an idea on for a while / may become it's own project. Sort of like what Click is to argparse / optparse.)

### An Incomplete List of Features Removed (and Reasons):
* Removed timing and profiling tools: Profiling is great, but there are dedicated python profiling tools avalible.
* Removed diff highlighting in HTML reports: This may someday make a comeback, but for now, a clean Jinja2 template far outweighs the advantages of inline diffs.
* Formatting of code segments is less careful than before. This is a temporary change pending the rewrite of internal AST representation.
* Removed CPD XML output. This may be added back in later, using templates.
* Multiple settings like `distance-threshold` which will be added again using configurations.

## License and Warranty Information
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program as `LICENSE.txt`.  If not, see <http://www.gnu.org/licenses/>.

(C) Will Oursler 2015
