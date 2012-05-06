import urllib, urllib2
import json
import traceback


search_service = "http://search.maven.org/solrsearch/select?%s"


def search(query, start, maximum, format, core=None, advanced=None, verbose=False, **kwargs):
    advanced = advanced or {}
    query_params = {
        "rows": maximum,
        "wt": "json",
        "start": start,
        "q": query if query else ' AND '.join(['%s:"%s"' %(n, v) for n, v in advanced.iteritems()])}
    if core:
        query_params['core'] = core

    try:
        search_url = search_service % (urllib.urlencode(query_params))
        if verbose:
            print 'Requesting %s'%search_url
        request = urllib2.Request(search_url)
        body = urllib2.urlopen(request).read()
        data = json.loads(body)
        # print json.dumps(data, sort_keys=True, indent=4)
        result = SearchResult(data)
    except (urllib2.URLError, ValueError) as error:
        raise SearchError(error)

    try:
        result.lines = []
        for index, doc in enumerate(result.docs):
                result.lines.append(format.format(i=index+1, **doc))
    except KeyError as error:
        raise SearchError(error, "Invalid format. Key %s not found."%(error))
    except ValueError as error:
        raise SearchError(error, "Invalid format. %s."%(error))

    return result


class SearchError(Exception):

    def __init__(self, error, message='Bad request.'):
        self.error_message = message
        self.error = error
        self.trace = traceback.format_exc()


class SearchResult(object):

    def __init__(self, data):
        self.error = None
        self.data = data
        self.docs = data['response']['docs']
        self.total = data['response']['numFound']
        self.len = len(self.docs)
        self.start = data['response']['start'] + 1
        self.end = data['response']['start'] + self.len
        self.suggestions = []
        if data.has_key('spellcheck'):
            suggestions = data['spellcheck']['suggestions']
            for i in range(1, len(suggestions), 2):
                self.suggestions.extend(suggestions[i]['suggestion'])
                