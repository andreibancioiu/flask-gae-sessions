import unittest
import myapp
import flask
from helpers import TestBase
from myapp.gaesession import SessionModel


class SessionsTestCase(TestBase):

    def test_can_add_to_session(self):
        with self.create_test_client() as client:
            data = dict(key='a', value='b', mutate='mutate')
            response = client.post('/', data=data)
            assert 'b' == flask.session['u:a']

        sid = self.get_session_id(response)
        db_session = SessionModel.get_by_id(sid)

        assert db_session.get_data()['u:a'] == 'b'
        assert SessionModel.query().count() == 1

    def test_create_session_changes_sid(self):
        with self.create_test_client() as client:
            response = client.get('/')
            sid_before = self.get_session_id(response)

            data = dict(create='create')
            response = client.post('/', data=data)
            sid_after = self.get_session_id(response)

            assert sid_before != sid_after

    def test_can_create_then_destroy_session(self):
        with self.create_test_client() as client:
            # Create
            data = dict(create='create')
            response = client.post('/', data=data)
            sid = self.get_session_id(response)

            assert SessionModel.get_by_id(sid) is not None

            # Destroy
            data = dict(create='destroy')
            response = client.post('/', data=data)
            sid_after_destroy = self.get_session_id(response)

            assert SessionModel.get_by_id(sid) is None
            assert sid != sid_after_destroy

if __name__ == '__main__':
    unittest.main()
