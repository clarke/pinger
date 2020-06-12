![pinger](https://github.com/clarke/pinger/workflows/pinger/badge.svg)

# pinger

Set of utilities to remotely check if a webpage loads.

---

## Configuration

Configuration of sites to check is contained in an external configuration file. The file is expected to live in the user's home directory and be called .pinger.conf. `~/.pinger.conf`

Example configuration:

```
---
runner:
    max_thread_workers: 8
email:
    port: 587
    smtp_server: smtp.gmail.com
    sender_email: user-account@gmail.com
    password: application-specific-password
sites:
- label: google
  email_recipients:
  - user@example.com
  timeout: 0.1
  url: https://google.com
  enabled: 1
- label: yahoo
  email_recipients:
  - foo@bar.com
  timeout: 1
  url: https://yahoo.com
  enabled: 0
```

Note: The default max_thread_workers is 5.

### Email

The email section is for the smtp configuration, so that email can be sent.

### Sites

The sites section is for the sites to be checked. Each site should contain:

- url (The URL to be called for the check)
- timeout (The connect timeout in seconds)
- email_recipients (A list of email addresses to notify on failure)
- enabled (Whether to enable the specific site, or to skip it. 0: disabled, 1: enabled)

### Note

Since this configuration file contains an smtp password, the file permissions should be as restrictive as possible. It should ideally be set to 0600, so that only the owner can read and write it.

## Setup

There is a make command to install dependencies:

`$ make setup`

## Running the checks

Running checks can be accomplished by:

`$ ./pinger_runner.py`

### Help

```
$ ./pinger_runner.py -h

usage: pinger_runner.py [-h] [-d] [-n] [-t] [-c CONFIG]
                        [-w MAX_THREAD_WORKERS]

Process some integers.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           turn on debug mode
  -n, --dry_run         show what steps would take place, but don't actually
                        do them.
  -t, --timer           time the run
  -c CONFIG, --config CONFIG
                        specify a configuration file
  -w MAX_THREAD_WORKERS, --max_thread_workers MAX_THREAD_WORKERS
                        set the maximum number of worker threads
```
