# Tanapol Bot

This bot was created with the inspiration to integrate the workflow Slack, Backlog, and Github together.


# Installation

**required python3.6+**

1. Clone this repository
1. `pip3 install -r requirements.txt`
1. `cp secrets-sample.yml secrets.yml`
1. Get your SSL cert and key.
1. Fill in the appropriate secret to each field.

## Slack setup

1. Create your app.
1. Add scope to your app. Currently this bot uses.
  * `channels:history`
  * `channels:read`
  * `channels:write:user`
  * `groups:history`
  * `groups:read`
  * `reactions:read`
  * `reactions:write`
1. Subscribe to their event api (See their documentation)
1. Currently, the supported events are
  * `messages.channels`
  * `reaction_added`
  * `reaction_removed`
  * `message.groups`


# Contributing

Any contribution is welcome, even a grammar check in this readme.
Fork the code and submit a pull request with some explanation.
