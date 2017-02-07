import unittest
import Cookie
import myapp
from google.appengine.ext import ndb
from google.appengine.ext import testbed


class TestBase(unittest.TestCase):

    def setUp(self):
        print ""
        print "TestBase.setUp"
        self.app = myapp.app
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

        self.app.config['TESTING'] = True

    def tearDown(self):
        print "TestBase.tearDown"
        self.testbed.deactivate()

    def create_test_client(self):
        return self.app.test_client()

    def get_session_id(self, response):
        cookie = response.headers['Set-Cookie']
        cookie = Cookie.SimpleCookie(cookie)
        signed_id = cookie['session'].value
        return signed_id.split('.')[0]
