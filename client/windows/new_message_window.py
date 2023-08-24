import curses
from datetime import datetime

import client_data

from .base_window import BaseWindow


class NewMessageWindow(BaseWindow):
    def __init__(self, stdscr, middle_window, login_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(client_data.NEW_MSG_HEIGHT, client_data.NEW_MSG_WIDTH, self.maxY // 4,
                                         self.maxX // 4)
        self.window.bkgd(' ', curses.color_pair(client_data.COLOR_PAIR))
        self.recipient = ''
        self.content = ''
        self.command = ''
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.middle_window = middle_window
        self.login_window = login_window
        self.message_exceeded = None
        self.max_msg_length = None

    def init_window(self):
        self.max_msg_length = client_data.MAX_MESSAGE_LENGTH

        self.window.border()
        self.window.refresh()
        self.window.addstr(1, 2, "Recipient: ")
        self.window.refresh()
        self.window.addstr(2, 2, "Content: ")
        self.window.refresh()
        self.window.addstr(10, client_data.NEW_MSG_WIDTH - 9, f'0/{self.max_msg_length}')
        self.window.refresh()

    def clear_line(self, y_poz):
        self.window.addstr(y_poz, 12, client_data.CLEAR_SPACE_NEW_MSG__WINDOW)

    def number_of_chars(self):
        count = len(self.content)
        if count >= 250:
            self.window.attron(curses.color_pair(client_data.ERROR_COLOR_PAIR))
        else:
            self.window.attron(curses.color_pair(client_data.COLOR_PAIR))
        self.window.addstr(10, client_data.NEW_MSG_WIDTH - 9, f'{count}/{self.max_msg_length} ')
        self.window.refresh()

    def get_new_message(self):
        self.content = ''
        self.command = {}
        self.window.attron(curses.color_pair(client_data.COLOR_PAIR))
        curses.curs_set(2)
        curses.echo()
        self.window.refresh()
        self.clear_line(1)
        self.clear_line(2)

        self.recipient = self.window.getstr(1, 15).decode(errors="ignore")
        self.init_window()

        self.message_exceeded = False

        content_y, content_x = 2, 15
        self.window.move(content_y, content_x)

        while True:
            key = self.window.getch()
            if key == 10:  # Enter
                break
            elif key == curses.KEY_BACKSPACE or key == ord('\b') or key == ord('\x7f'):  # Backspace
                if content_x > 15:
                    content_x -= 1
                    self.content = self.content[:-1]
                    self.window.delch(content_y, content_x)
                    self.window.insstr(content_y, client_data.NEW_MSG_WIDTH - 2, " ")
                    if content_x < client_data.NEW_MSG_WIDTH - 2:
                        self.window.move(content_y, content_x)
                    self.message_exceeded = False
                    self.number_of_chars()
                    self.window.move(content_y, content_x)
                    self.window.attron(curses.color_pair(client_data.COLOR_PAIR))
                else:
                    if content_y > 2:
                        content_y -= 1
                        content_x = len(self.content) % (client_data.NEW_MSG_WIDTH - 15) + 15
                        self.window.move(content_y, content_x)
                        self.message_exceeded = False
            elif key == curses.KEY_LEFT:
                if content_x > 15:
                    content_x -= 1
                    self.window.move(content_y, content_x)
            elif key == curses.KEY_RIGHT:
                if content_x < client_data.NEW_MSG_WIDTH - 2:
                    content_x += 1
                    self.window.move(content_y, content_x)
            elif key == curses.KEY_UP:
                pass
            elif key == curses.KEY_DOWN:
                pass
            elif key == curses.KEY_DC:  # DEL
                if content_x < client_data.NEW_MSG_WIDTH - 2:
                    self.content = self.content[:content_x - 15] + self.content[content_x - 14:]
                    self.window.delch(content_y, content_x)
                    self.window.insstr(content_y, client_data.NEW_MSG_WIDTH - 2, " ")
                    if content_x < client_data.NEW_MSG_WIDTH - 2:
                        self.window.move(content_y, content_x)
                    self.message_exceeded = False
                    self.number_of_chars()
                self.window.move(content_y, content_x)
            else:
                char = chr(key)
                if char.isprintable() and len(self.content) < self.max_msg_length:
                    if content_x == client_data.NEW_MSG_WIDTH - 3:
                        if content_y < client_data.NEW_MSG_HEIGHT - 1:
                            content_y += 1
                            content_x = 15
                    self.content += char
                    if len(self.content) >= self.max_msg_length:
                        self.window.move(content_y, content_x)
                    self.window.addch(content_y, content_x, char)
                    content_x += 1
                    curses.noecho()
                self.number_of_chars()
                self.window.move(content_y, content_x)
                self.window.attron(curses.color_pair(client_data.COLOR_PAIR))
                if len(self.content) >= self.max_msg_length:
                    self.message_exceeded = True
                else:
                    self.message_exceeded = False

        self.command = {
            self.login_window.login_username: {
                "new_message": (
                    {'sender': self.login_window.login_username},
                    {'date': str(self.date)},
                    {'recipient': self.recipient},
                    {'content': self.content}
                )
            }
        }

        self.window.erase()
        self.window.refresh()
        curses.noecho()
        self.middle_window.send_receive_command_and_show_respond(self.command)

    def show(self):
        self.init_window()
        self.window.keypad(1)
        self.window.timeout(-1)
        curses.curs_set(2)
        curses.echo()

        self.init_window()
        self.get_new_message()
        curses.noecho()
        curses.curs_set(0)
        self.window.keypad(0)
        self.window.timeout(100)
