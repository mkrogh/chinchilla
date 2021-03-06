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


"""
Chinchilla is a convinience library for interacting with web pages.
It allows you to visit pages, fill out forms and follow links.
"""

def visit(url):
    """Visit/open page"""
    __send_request(url)

def page_content():
    """Get the current page content"""
    return current_page

def page_url():
    """Get the url of the current page"""
    return current_page_url

def fill_in(field, value=None):
    """Simulate filling in a form input field.
    Field will be matched, first on id, then on exact name attribute, and lastly fuzzy (contains) match on name attriubte.
    The value is optional, if missing you will be prompted for it at runtime.

    Will not really fill out the form on the page.
    Prints message if field could not be found.
    """
    global current_query
    q = "#{name},input[name={name}],input[name*={name}]".format(name=field)
    field = page_soup.select_one(q)
    if field:
        value = value or raw_input("What {name} do you want to use? ".format(name=field["name"]))
        current_query[field["name"]] = value
    else:
        __log("Could not find field matching '{name}'".format(name=field))

def submit():
    """Submits the form containing the input fields filled out using 'fill_in'.
    Will include all hidden fields in the form.
    
    Can handle GET forms.
    If a form cannot be found an error message will be printed.
    """
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
            if field.has_attr("value"):
                current_query[field["name"]]=field["value"]
        url = urljoin(current_page_url, form["action"])
        data = urllib.urlencode(current_query)
        if form.has_attr("method") and form["method"].lower() == "get":
            __send_request(url+"?"+data)
        else:
            __send_request(url,data)
    else:
        __log("Unable to find form :(")

def click_link(selector):
    """Follow link on page.
    Will try ID, and class first, otherwise it will look for a link with exact matching text.

    Prints error message if no link could be found.
    """
    link = None
    url=None
    if "" not in selector:
        q = "#{sel},a[class='{sel}']".format(sel=selector)
        link = page_soup.select_one(q)
    if link and link.has_attr("href"):
        url = link["href"]
    else:
        links = page_soup.find_all("a", text=selector)
        for link in links:
            if link.has_attr("href"):
              url = link["href"]
              break
    if url:
        url = urljoin(current_page_url, url)
        visit(url)
    else:
        __log("Could not find link for '{sel}'".format(sel=selector))

def has_content(what, silent=False):
    """
    Simple check if page_content contains the specified string.
    Per default an error message will be printed if string is not found.
    """
    status = what.lower() in page_content().lower()
    if not status:
        __log("Could not find {what} on {page}".format(what=what,page=current_page_url))
    return status

def __send_request(url, data=None):
    try:
        resp = client.open(url, data)
        content = resp.read()
        __update_globals(resp.geturl(), content)
    except urllib2.HTTPError as e:
        __log("'{error}' on '{page}' visiting: '{url}'".format(error=e.code, page=e.geturl(), url=url))
        __update_globals(e.geturl(), e.read())

def __update_globals(url, content):
    """Updates and resets global variables"""
    global current_query, current_page_url, current_page, page_soup
    current_page = content
    page_soup = BeautifulSoup(content, "html.parser")
    current_query = {}
    current_page_url = url

def __log(msg):
    print msg

def _client(new_client):
    global client
    client = new_client
