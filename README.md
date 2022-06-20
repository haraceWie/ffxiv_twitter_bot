# Twitter Webhook Boilerplate Python

This is a work-in-progress port of a Twitter webhook server to Python 3.x.
Several TODOs are noted in the code, but this should be functional.

Starter app / scripts for consuming events via Account Activity API.

The current functionality when setup includes:

1. When subscribed user receives a Direct Message that is 'Hello Bot', will reply with 'Hello World'
2. When a Tweet posted from the subscribed account is liked, the user who liked it's Screen Name will be printed

## Dependencies

* A Twitter app created on [apps.twitter.com](https://apps.twitter.com/)
* [Python](https://www.python.org)
* requires TwitterAPI Python library >= 2.4.8
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) (optional)

## Create and configure a Twitter app

1. Create a Twitter app on [apps.twitter.com](https://apps.twitter.com/)

2. On the **Permissions** tab > **Access** section > enable **Read, Write and Access direct messages**.

3. On the **Keys and Access Tokens** tab > **Your Access Token** section > click **Create my access token** button.

4. On the **Keys and Access Tokens** tab, take note of the `consumer key`, `consumer secret`, `access token` and `access token secret`.

## Setup the web app

1. Clone this repository:

    ```bash
    git clone https://github.com/rickredsix/twitter-webhook-boilerplate-python.git
    ```

2. Create a virtual environment

    ```bash
    virtualenv venv
    ```

3. Activate virtual environment:

    Note that the included venv is Python 2.7 and this current code requires 3.6.x
	
    ```bash
    source venv/bin/activate
    ```

4. Install python requirements

    ```bash
    pip install -r requirements.txt
    ```

5. Define key variables locally using the keys and access tokens noted previously (this is only for local example scripts, replace the text after the =)

    ```bash
    export CONSUMER_KEY={INSERT_CONSUMER_KEY}
    export CONSUMER_SECRET={INSERT_CONSUMER_SECRET}
    export ACCESS_TOKEN={INSERT_ACCESS_TOKEN}
    export ACCESS_TOKEN_SECRET={INSERT_ACCESS_TOKEN_SECRET}
    export ENVNAME={INSERT_TWITTER_DEV_ENV_NAME}
    export WEBHOOK_URL={WEBHOOK_URL_AFTER_DEPLOYMENT}
    ```

6. Deploy app. To deploy to Heroku see "Deploy to Heroku" instructions below.

    Take note of your webhook URL. For example:

    ```bash
    https://your.app.domain/webhook
    ```

## Configure webhook to receive events via the API

1. Create webhook config.

    ```bash
    python example-scripts/create-webhook.py
    ```

    (Take note of returned `webhook_id`).

2. Add user subscription.

    ```bash
    python example-scripts/subscribe-account.py
    ```

    Subscription will be created for user the context provided by the access tokens. By default the tokens on the app page are the account that created the app.

## Deploy to Heroku (optional)

1. Init Heroku app.

    ```bash
    heroku create
    ```

2. Run locally. (This won't do receive the events as you'll have to configure the webhook URL above as the Heroku URL)

    ```bash
    heroku local
    ```

3. Configure environment variables. Set up required environmental variables, these will be the keys and access tokens again, plus the Twitter ID of the account that is subscribed. You can find this on the app page listed as Owner ID. See Heroku documentation on [Configuration and Config Vars](https://devcenter.heroku.com/articles/config-vars).

    ```bash
    heroku config:set CONSUMER_KEY={INSERT_CONSUMER_KEY}
    heroku config:set CONSUMER_SECRET={INSERT_CONSUMER_SECRET}
    heroku config:set ACCESS_TOKEN={INSERT_ACCESS_TOKEN}
    heroku config:set ACCESS_TOKEN_SECRET={INSERT_ACCESS_TOKEN_SECRET}
    heroku config:set CURRENT_USER_ID={INSERT_USER_ID}
    ```

4. Deploy to Heroku.

    ```bash
    git push heroku master
    ```

## Documentation

* [Direct Message API](https://developer.twitter.com/en/docs/direct-messages/api-features)
* [Account Activity API (All Events)](https://developer.twitter.com/en/docs/accounts-and-users/subscribe-account-activity/api-reference/aaa-premium)
