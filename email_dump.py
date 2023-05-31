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
import getpass
import imaplib
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
    email = input('Email: ')
    password = getpass.getpass()
    return email, password


class Email:
    def __init__(self, email: str, password: str) -> None:
        self.conn = imaplib.IMAP4_SSL('imap.gmail.com')
        self.email = email
        self.password = password

    def __enter__(self) -> Email:
        self.login()
        return self

    def __exit__(self, exec_type: type[BaseException] | None,
                 exec_val: BaseException | None, traceback: TracebackType | None) -> None:
        pass

    def login(self) -> None:
        self.conn.login(self.email, self.password)

    def get_emails_from_user(self, from_email: str) -> list[imaplib._AnyResponseData]:
        self.conn.select('Inbox')
        _, count = self.conn.search(None, 'FROM', f'"{from_email}"')

        emails: list[imaplib._AnyResponseData] = []

        for i in count[0].split():
            _, data = self.conn.fetch(i, '(RFC822)')
            emails.append(data)

        return emails

    def save_email_from_user(self, from_user: str, dir: str) -> None:
        pass


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
    print(download_dir)

    if args.email is None or args.password is None:
        args.email, args.password = _prompt_email_password()

    with Email(args.email, args.password) as email:
        print(email.get_emails_from_user(vars(args)['from']))

    return 0
