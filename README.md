# Babel Godot plugin (forked)

## Installation

Install dependencies: `pip install Babel`

Install this local module: `pip install -e .`

## Usage

See [README.rst] (./README.rst)

## Changes of this fork

- Support arrays with different types
- Support recursive json keys
- Improved [keyword matching](#matchers)

## Matchers

Keywords

- `text` - match text property
- `Label#text` - match text property in node Label
- `*/text` - match property ending with `/text`
- `text/*` - match property starting with `text/`

Values

- Only String values containing characters are parsed
- `_PLACEHOLDER_` - starting and ending with `_` are ignored
