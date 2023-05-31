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
import argparse
import getpass
from pathlib import Path
from typing import Sequence

EXAMPLE_USE = '''
Example Use:
    email-dump --from example-email@email.com --dir dir/to/dump
    email-dump --from example-email@email.com
    email-dump --from example-email@email.com --email youemail@example.com --pass password
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
    parser.add_argument('--pass', type=str, help='The password used to login')

    args = parser.parse_args(argv)

    download_dir = args.dir if args.dir else '.'

    print(args, download_dir)

    return 0
