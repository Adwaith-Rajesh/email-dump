# email-dump

Download all the emails sent by a user into separate folders along with attachments.

## Why

I made `email-dump` to be used alongside one of my other project [Calsen](https://github.com/Adwaith-Rajesh/calsen) which is a search engine for files. with email dump
I can now search for files in my mail.
The dump will also contain a file that has the subject and body in it.
This should allow [Calsen](https://github.com/Adwaith-Rajesh/calsen) to search through the email body, and at the very least, allows me to get to the directory that has the
attachment.

## Installation

```console
pip3 install email-dump
```

## Usage

```console
email-dump --from fromemail@example.com --dir /dir/to/dump/the/email
```

- passing _email_ and _password_ directly from the command line

```console
email-dump --from fromemail@example.com --dir /dir/to/dump/the/email --email youemail@example.com --password supersecretpassword
```

> `email-dump --help` for more details

## Bye.....
