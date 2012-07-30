#!/usr/bin/env python

import xmlrpclib
import urllib2

def getheader(self, name, default=None):
	if self.headers is None:
		raise httplib.ResponseNotReady()
	return self.headers.getheader(name, default)

def getheaders(self):
	if self.headers is None:
		raise httplib.ResponseNotReady()
	return self.headers.items()

urllib2.addinfourl.getheader = getheader
urllib2.addinfourl.getheaders = getheaders


class ProxyTransport(xmlrpclib.Transport):
	"""Provides an XMl-RPC transport routing via a http proxy.
	
	This is done by using urllib2, which in turn uses the environment
	varable http_proxy and whatever else it is built to use (e.g. the
	windows registry).
	
	NOTE: the environment variable http_proxy should be set correctly.
	See checkProxySetting() below.
	
	Written from scratch but inspired by xmlrpc_urllib_transport.py
	file from http://starship.python.net/crew/jjkunce/ by jjk.
	
	A. Ellerton 2006-07-06
	"""

	def request(self, host, handler, request_body, verbose):
		self.verbose = verbose
		url = 'http://' + host + handler
		if self.verbose: "ProxyTransport URL: [%s]" % url

		request = urllib2.Request(url)
		request.add_data(request_body)
		# Note: 'Host' and 'Content-Length' are added automatically
		request.add_header("User-Agent", self.user_agent)
		request.add_header("Content-Type", "text/xml") # Important

		proxy_handler = urllib2.ProxyHandler()
		opener = urllib2.build_opener(proxy_handler)
		f = opener.open(request)
		return self.parse_response(f)


