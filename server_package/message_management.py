from server_package.database_support import handle_db_file_error
import server_package.server_response as server_response
import server_package.server_data as server_data


class MessageManagement:
    def __init__(self, database_support):
        self.database_support = database_support

    @staticmethod
    def msg_snd():
        return {'Msg-snd': "OK"}

    def new_message(self, data):
        if not data:
            return server_response.E_INVALID_DATA

        recipient = data[2]
        username = recipient["recipient"]

        new_user_data = tuple(d[next(iter(d))] for d in data)

        if not self.database_support.check_if_user_exist(username):
            return server_response.E_USER_DOES_NOT_EXIST
        elif self.database_support.inbox_msg_counting(username) == server_data.MAX_MSG_IN_INBOX:
            return server_response.E_RECIPIENT_INBOX_IS_FULL
        else:
            self.database_support.add_new_message_to_db(new_user_data)
            return server_response.MESSAGE_WAS_SENT

    def msg_list(self, username):  # to show all messages in box in middle window show all msgs in box
        if not username:
            return server_response.E_INVALID_DATA

        all_inbox_msgs = self.database_support.show_all_messages_inbox(username)
        msg_list_dict = {}
        for index, (message_id, sender, date) in enumerate(all_inbox_msgs, start=1):
            formatted_date = date.strftime('%Y-%m-%d')
            msg_list_dict[index] = {'message_id': message_id, 'sender': sender, 'date': formatted_date}
        return {"msg": msg_list_dict}

    def msg_del(self, data):
        if not data:
            return server_response.E_INVALID_DATA

        username = list(data.keys())[0]
        msg_list_dict = self.msg_list(username)["msg"]
        msg_num = list(data.values())[0]
        cos_tam = list(msg_list_dict.keys())
        if int(msg_num) in cos_tam:
            msg_id_to_del = msg_list_dict[int(msg_num)]["message_id"]
            print(f'message to del = {msg_id_to_del}')
            self.database_support.delete_selected_message(int(msg_id_to_del))
            return server_response.MESSAGE_WAS_DELETED
        else:
            return server_response.E_MESSAGE_NOT_FOUND


    # @handle_db_file_error
    # def msg_show(self, data):  # to show selected message
    #     if not data:
    #         return server_response.E_INVALID_DATA
    #
    #     db_msgs = self.database_support.get_messages()
    #     for username, msg_num in data.items():
    #         if msg_num in db_msgs['messages'][username]:
    #             message_to_show = db_msgs['messages'][username][msg_num]
    #             return {"Message to show": message_to_show}
    #         else:
    #             return server_response.E_MESSAGE_NOT_FOUND

    def msg_show(self, data):   # to show selected message
        if not data:
            return server_response.E_INVALID_DATA

        username = list(data.keys())[0]
        msg_list_dict = self.msg_list(username)["msg"]
        msg_num = list(data.values())[0]
        cos_tam = list(msg_list_dict.keys())
        if int(msg_num) in cos_tam:
            msg_id_to_show = msg_list_dict[int(msg_num)]["message_id"]
            print(f'message to show = {msg_id_to_show}')
            message_to_show = self.database_support.show_selected_message(int(msg_id_to_show))
            print(message_to_show)
            print(type(message_to_show))
            return {"Message to show": message_to_show}
        else:
            return server_response.E_MESSAGE_NOT_FOUND

    @handle_db_file_error
    def msg_count(self, username):  # to count all messages in inbox
        if not username:
            return server_response.E_INVALID_DATA

        inbox_msg_count = self.database_support.inbox_msg_counting(username)
        if inbox_msg_count >= 5:
            inbox_msg_count = str(inbox_msg_count) + server_response.YOUR_INBOX_IS_FULL
        return {"msg-inbox-count": inbox_msg_count}

    def convert_datetime_datetime_to_string_date(self, datetime_from_db):
        if not datetime_from_db:
            return None
        else:
            converted_datetime = datetime_from_db.strftime('%Y-%m-%d')
            return converted_datetime