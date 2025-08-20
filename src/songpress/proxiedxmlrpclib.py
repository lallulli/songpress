import xmlrpc.client

import requests


class RequestsTransport(xmlrpc.client.Transport):
	def request(self, host, handler, data, verbose=False):
		# set the headers, including the user-agent
		headers = {
			"User-Agent": "my-user-agent",
			"Content-Type": "text/xml",
			"Accept-Encoding": "gzip"
		}
		url = "https://%s%s" % (host, handler)
		response = None
		try:
			response = requests.post(url, data=data, headers=headers)
			response.raise_for_status()
			return self.parse_response(response)
		except requests.RequestException as e:
			if response is None:
				raise xmlrpc.client.ProtocolError(url, 500, str(e), "")
			else:
				raise xmlrpc.client.ProtocolError(url, response.status_code, str(e), response.headers)

	def parse_response(self, resp):
		"""
		Parse the xmlrpc response.
		"""
		p, u = self.getparser()
		p.feed(resp.text)
		p.close()
		return u.close()