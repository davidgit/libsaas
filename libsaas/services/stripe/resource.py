import json

from libsaas import http, parsers
from libsaas.services import base


def parse_count(body, code, headers):
    if not 200 <= code < 300:
        raise http.HTTPError(body, code, headers)

    response = json.loads(body.decode('utf-8'))
    return response['count']


class StripeResource(base.RESTResource):

    @base.apimethod
    def update(self, obj):
        """
        Update this resource.

        :var obj: a Python object representing the updated resource, usually in
            the same format as returned from `get`. Refer to the upstream
            documentation for details.
        """
        self.require_item()
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json


class ListResourceMixin(object):

    @base.apimethod
    def get(self, count=None, offset=None):
        """
        Fetch all of the objects.

        :var count: A limit on the number of objects to be returned.
            Count can range between 1 and 100 objects.
        :vartype count: int

        :var offset: An offset into your object array. The API will return
            the requested number of objects starting at that offset.
        :vartype offset: int
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def count(self, *args, **kwargs):
        """
        Fetch an integer count of the number of objects of a collection. This
        is an absolute number, regardless of paging limits, so use this if you
        want to tally up a collection instead of iterating through all of its
        objects.

        Accepts the same arguments as `get`.
        """
        with base.extract_request():
            kwargs['count'] = 1
            request = self.get(*args, **kwargs)

        return request, parse_count

