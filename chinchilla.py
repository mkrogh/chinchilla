import cookielib, urllib2, urllib
from urlparse import urljoin
from bs4 import BeautifulSoup
cookie_jar = cookielib.CookieJar()
client = urllib2.build_opener(
        urllib2.HTTPRedirectHandler(),
        urllib2.HTTPCookieProcessor(cookie_jar))

#globals
current_page = None
current_query = {}
page_soup = None

def visit(url):
    __send_request(url)

def page_content():
    return current_page

def fill_in(field, value=None):
    global current_query
    q = "#{name},input[name={name}],input[name*={name}]".format(name=field)
    field = page_soup.select_one(q)
    if field:
        value = value or raw_input("What {name} do you want to use? ".format(name=field["name"]))
        current_query[field["name"]] = value
    else:
        print "Could not find field matching '{name}'".format(name=field)

def submit():
    global current_query, current_page_url, current_page, page_soup
    q = "input[name={name}]".format(name=current_query.keys()[0])
    elm = page_soup.select_one(q)
    if elm:
        for parent in elm.parents:
            if parent.name == "form":
                form = parent
                break
    if form:
        hidden_fields = form.select("input[type=hidden]")
        for field in hidden_fields:
            if "value" in field:
                current_query[field["name"]]=field["value"]
        url = urljoin(current_page_url, form["action"])
        data = urllib.urlencode(current_query)
        if "method" in form and form["method"].lower() == "get":
            __send_request(url+"?"+data)
        else:
            __send_request(url,data)

def __send_request(url, data=None):
    try:
        resp = client.open(url, data)
        content = resp.read()
        __update_globals(resp.geturl(), content)
    except urllib2.HTTPError as e:
        print "'{error}' on '{page}' visiting: '{url}'".format(error=e.code, page=e.geturl(), url=url)
        __update_globals(e.geturl(), e.read())

def __update_globals(url, content):
    global current_query, current_page_url, current_page, page_soup
    current_page = content
    page_soup = BeautifulSoup(content, "html.parser")
    current_query = {}
    current_page_url = url
