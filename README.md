Chinchilla - a simple sequential webpage interaction tool
=========================================================

Chinchilla is distant python cousin to the larger ruby [capybara](https://github.com/jnicklas/capybara) test framework.

The initial goal of Chinchilla is to make it easier access content that normally require web page interactions,
such as pages behind a login.

Currently chinchilla is sequential, and relies on globals, so I'm quite sure it is not thread safe.

Chinchilla needs beautiful soup to be installed.

Usage
-------

```
from chinchilla import *

visit("http://localhost:8000/login/")
fill_in("username", "markus")
fill_in("password", "secret")
submit()
visit("http://localhost:8000/secret_page/")
print page_content()
```

`fill_in("username", "markus")` tries to find an input field based on the name supplied by:

- finding it by ID `#username`
- find an input whith the excact name `username`
- find an input where `username` is in the input name

If you want you can leave out the second argument of `fill_in`, in which case chinchilla will ask you to input it via `raw_input`.

Why?
-------

Chinchilla was made to allow local html validation of pages protected by login.
Having worked with capybara for test cases in ruby, I wanted something with the same simple syntax.

Chinchilla can be used for anything where you need to interact with a web page,
as long as that interaction does not require JavaScript.

TODO
----

- `click_link` functionallity
- Something like capybaras `within` for easier selection
- `has_content` - check if the page contains.
- `has_element` - check if a given css selector exists on page
- Maybe lazy instantiation of beautiful soup
