from chinchilla  import *

visit("http://localhost:8000/login/")
fill_in("username", "markus")
fill_in("password", "secret")
submit()
visit("http://localhost:8000/secrets/")

