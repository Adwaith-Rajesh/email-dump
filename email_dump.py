"""
MIT License

Copyright (c) 2023 Adwaith Rajesh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations

import argparse
import email
import getpass
import imaplib
import os
from pathlib import Path
from types import TracebackType
from typing import Sequence

EXAMPLE_USE = '''
Example Use:
    email-dump --from example-email@email.com --dir dir/to/dump
    email-dump --from example-email@email.com
    email-dump --from example-email@email.com --email youemail@example.com --password password
'''


def _check_dir(dirpath: str) -> str:
    if Path(dirpath).is_dir():
        return dirpath
    raise NotADirectoryError(dirpath)


def _prompt_email_password() -> tuple[str, str]:
    email_add = input('Email: ')
    password = getpass.getpass()
    return email_add, password


def _save_file(filepath: str, content: bytes) -> None:
    with open(filepath, 'wb') as f:
        f.write(content)


class Email:
    def __init__(self, email_add: str, password: str) -> None:
        self.conn = imaplib.IMAP4_SSL('imap.gmail.com')
        self.email_add = email_add
        self.password = password

    def __enter__(self) -> Email:
        self.login()
        return self

    def __exit__(self, exec_type: type[BaseException] | None,
                 exec_val: BaseException | None, traceback: TracebackType | None) -> None:
        pass

    def login(self) -> None:
        self.conn.login(self.email_add, self.password)

    def get_emails_from_user(self, from_email: str) -> list[imaplib._AnyResponseData]:
        self.conn.select('Inbox')
        _, count = self.conn.search(None, 'FROM', f'"{from_email}"')

        emails: list[imaplib._AnyResponseData] = []

        for i in count[0].split():
            _, data = self.conn.fetch(i, '(RFC822)')
            emails.append(data)

        return emails

    def save_email_from_user(self, from_email: str, dir: str) -> None:
        emails = self.get_emails_from_user(from_email=from_email)

        for idx, e in enumerate(emails):
            Path(os.path.join(dir, str(idx))).mkdir(exist_ok=True)

            if not isinstance(e, tuple):
                return

            raw_email = e[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                if bool(filename):
                    file_path = os.path.join(dir, str(idx), filename)
                    _save_file(filepath=file_path,
                               content=part.get_payload(decode=True))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='dump all the email sent by a specific user',
        epilog=EXAMPLE_USE,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--from', '-f', type=str,
                        help='email of the user to dump from.', required=True)
    parser.add_argument('--dir', '-d', type=_check_dir,
                        help='The directory to dump all the emails to.')

    parser.add_argument('--email', type=str,
                        help='The email address used to login.')
    parser.add_argument('--password', type=str,
                        help='The password used to login')

    args = parser.parse_args(argv)

    download_dir = args.dir if args.dir else '.'

    if args.email is None or args.password is None:
        args.email, args.password = _prompt_email_password()

    with Email(args.email, args.password) as mail:
        mail.save_email_from_user(vars(args)['from'], download_dir)

    return 0
