from kol.Error import NightlyMaintenanceError, NotLoggedInError
from kol.util import Report

import urllib

class GenericRequest(object):
	"A generic request to a Kingdom of Loathing server."
	
	def __init__(self, session):
		self.session = session
		self.requestData = {}

	def doRequest(self):
		"""
		Performs the request. This method will ensure that nightly maintenance is not occuring.
		In addition, this method will throw a NotLoggedInError if the session thinks it is logged
		in when it actually isn't. All specific KoL requests should inherit from this class.
		"""
		
		Report.debug("request", "Requesting %s" % self.url)
		
		self.response = self.session.opener.open(self.url, urllib.urlencode(self.requestData))
		self.responseText = self.response.read()
		
		Report.debug("request", "Received response: %s" % self.url)
		Report.debug("request", "Response Text: %s" % self.responseText)
		
		if self.response.geturl().find("/maint.php") >= 0:
			self.session.isConnected = False
			raise NightlyMaintenanceError("Nightly maintenance in progress.")
			
		if self.response.geturl().find("/login.php") >= 0:
			if self.session.isConnected:
				self.session.isConnected = False
				raise NotLoggedInError("You are no longer connected to the server.")
