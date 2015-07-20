Changelog
=========

## [unreleased][unreleased]

## [0.0.1] - 2015-07-17
### Added
- Basic functionallity of chinchilla.
  - `visit(url)` open a page
  - `fill_in(field, value)` fill in an input field with value
  - `submit()` submits the form that has been filled in
  - `click_link("Login")` follows link with id, class or text matching argument
  - `page_content()` returns the current page's content
  - `page_url()` returns the current page's url
  - `has_content(content)` returns true or false, can be html.
