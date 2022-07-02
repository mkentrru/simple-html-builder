# Custom markdown to html translator


## Usage

`./builder.py [directory]`

&nbsp;&nbsp;&nbsp;&nbsp;`directory` - optional argument *(uses current dir if not stated)*


## Working directory hierarchy:

| Path  | Meaning |
| ------------- |:-------------:|
| res/      | directory for building resources     |
| res/template.html  | html file with custom tags to be parsed with tool     |
| output/index.html      | resulting html page     |
| output/styles.css      | styles used    |
| output/img/      | directory for images used    |

### Template tags

This is casual html file. Add custom tags to trigger tool parser:

* `[ext] 'path in res/'` - import external source parser *(main tag)*
* `[table]` - put table built with `[ext]'s` table of content
* `//` - line comments - line will not be added to output


## External sources syntax

External source file is parsed to html. Result simply overrides 
tag mention in template

### Basic rules

* Each line is parsed separately
* `%%` is used to trigger line parsing
* If line does not contain `%%` it is treated as `<p>'your line'</p>` 
 **(lines with table tags do not get parsed)**
* You can highlight text by wrapping it with `{'highlighted text'}`

### Line parsing

#### HTML tags

You can use HTML container tags to wrap your text:

`h3 %% SAMPLE TEXT`.

Results as:

`<h3>SAMPLE TEXT</h3>`

Some multi-parameter HTML tags support is here: 

`a %% text for link // url `

Results as:

`<a href="url">text for link</a>`

Supported tags:
* `img %% 'path in res/'` - `<img>`
* `ifr %% 'src'` - `<iframe>`


#### Custom tags

* `anchor %% LEVEL // Text` - add anchor to table of content 
 *(LEVEL value handle is not implemented in table so far)*
* `link %% text // url` - same as `a`
* `st` - custom list entry
* `quote` - puts text to pretty square