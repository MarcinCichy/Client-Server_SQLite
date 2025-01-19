import os
import unittest
from server_package.message_management import MessageManagement
import server_package.server_response as server_response
from server_package.database_support import DatabaseSupport
import build_test_db

# Ustawienie dla testów – np. SQLite
os.environ['TEST_ENV'] = 'test'
# os.environ['TEST_ENGINE'] = 'postgresql'
os.environ['TEST_ENGINE'] = 'sqlite'


class TestMessageManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        build_test_db.drop_temp_db()
        build_test_db.create_temp_db()
        build_test_db.fill_temp_db()

    @classmethod
    def tearDownClass(cls):
        build_test_db.drop_temp_db()

    def setUp(self):
        self.database_support = DatabaseSupport()
        self.msg_mgmt = MessageManagement(self.database_support)

    def test_new_message_valid_data(self):
        sender = {'sender': 'user1'}
        date = {'date': '2024-02-18'}
        recipient = {'recipient': 'user3'}
        content = {'content': 'MSG CONTENT'}
        data = [sender, date, recipient, content]
        response = self.msg_mgmt.new_message(data)
        self.assertEqual(response, server_response.MESSAGE_WAS_SENT)

    def test_new_message_invalid_data(self):
        data = None
        response = self.msg_mgmt.new_message(data)
        self.assertEqual(response, server_response.E_INVALID_DATA)

    def test_new_message_full_inbox(self):
        sender = {'sender': 'user5'}
        date = {'date': 'YYYY-MM-DD'}
        recipient = {'recipient': 'user1'}
        content = {'content': 'MSG CONTENT'}
        data = [sender, date, recipient, content]

        result = self.msg_mgmt.new_message(data)
        self.assertEqual(result, server_response.E_RECIPIENT_INBOX_IS_FULL)

    def test_msg_list_no_messages(self):
        result = self.msg_mgmt.msg_list('NO_MSGS_USER')
        self.assertEqual(result, {"msg": {}})

    def test_msg_list_with_messages(self):
        result = self.msg_mgmt.msg_list('user1')
        self.assertNotEqual(result, {"msg": {}})

    def test_msg_del_existing_message(self):
        result = self.msg_mgmt.msg_del({'user3': '1'})
        self.assertEqual(result, server_response.MESSAGE_WAS_DELETED)

    def test_msg_del_non_existing_message(self):
        result = self.msg_mgmt.msg_del({'RECIPIENT': '7'})
        self.assertEqual(result, server_response.E_MESSAGE_NOT_FOUND)

    def test_msg_show_existing(self):
        result = self.msg_mgmt.msg_show({'user1': '2'})
        self.assertEqual(result, {"Message to show": {'content': 'Greetings, user5!',
                     'date': '2024-02-18',
                     'message_id': 4,
                     'recipient_id': 'user1',
                     'sender_id': 'user4'}})

    def test_msg_show_non_existing(self):
        result = self.msg_mgmt.msg_show({'user2': '4'})
        self.assertEqual(result, server_response.E_MESSAGE_NOT_FOUND)

    def test_msg_count(self):
        result = self.msg_mgmt.msg_count('user2')
        self.assertEqual(result, {"msg-inbox-count": 1})


if __name__ == '__main__':
    unittest.main(verbosity=2)
