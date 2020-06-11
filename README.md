# Purpose

Set of utilities to remotely check if a webpage loads.

# Configuration

Configuration of sites to check is contained in an external configuration file. The file is expected to live in the user's home directory and be called .pinger.conf. `~/.pinger.conf`

Example configuration:

```
---
sites:
    google:
      email_recipients:
      - user@example.com
      timeout: 0.1
      url: https://google.com
    yahoo:
      email_recipients:
      - foo@bar.com
      timeout: 1
      url: https://yahoo.com
```

# Setup

There is a make command to install dependencies:

`$ make setup`

# Running the checks

Running checks can be accomplished by:

`$ make run`
