# Prompt History

## Prompt 1

> Create me a markdown file called PROMPT_HISTORY.md. In it, we're going to proactively log every prompt I give you, starting with this one.

## Prompt 2

> Now, create me a Python file called "main.py".

## Prompt 3

> Help me refactor my entry page. (request.method == "GET" and url.path == "/") I want to create a simple form that allows a user to paste JSON describing the fraud event. Example below:
>
> {
>   "message": "Fraud event received",
>   "event": {
>     "email": "jsmith+promo17@gmail.com",
>     "country": "US",
>     "ip_country": "RO",
>     "card_country": "US",
>     "promo_code": "FREE30",
>     "prior_accounts_from_ip": 8,
>     "payment_attempts_last_hour": 5
>   }
> }
>
> Include a simple text box that captures this input, and a button that upon pressing, does a POST /analyze with the form input as the input that gets passed in.

## Prompt 4

> What would be the best way to handle and serve this page?

## Prompt 5

> Let's create the assets directory as you mentioned, with the requisite files.

## Prompt 6

> Alright, we now have a basic harness set up. First, help me ensure that the AI agent we're having help detect fraud returns a neater, defined JSON response. The JSON response should return the following fields:
>
> risk: This should return one of "low", "medium", or "high".
>
> summary: A string containing the summary of the incident.
>
> signals: An array of strings listing which signals led us to believe this is fraud.
>
> recommended_actions: An array of strings containing recommended actions to take to resolve this fraud incident.

## Prompt 7

> Let's also streamline this a bit by including some "local" signals that we can use to ascertain fraud in our file src/fraud_rules.py. Our function derive_signals() should take the JSON event as an input and output a list of signals as a list of "strings" in Python. I would like to enforce the following:
>
> If the ip_country != account country (field "country"), then append a string stating this mismatch to the signal list that we return.
>
> If the card_country != account country (field "country"), then append a string stating this mismatch to the signal list that we return.
>
> If the number of prior accounts associated with the same IP is greater than 4, add this to the list of signals to return.
>
> If the number of purchase attempts from this card is greater than 4, add this to the list of signals to return.

## Prompt 8

> When we are waiting for a response for the user, I would like to replace the simple "Analyzing..." text with a pseudo-animation. Can you replace it with a changing text that cycles between "Analyzing." "Analyzing.." and "Analyzing..." ?

## Prompt 9

> Let's talk 404 errors. How are we currently handling a situation where the agent is unreachable for whatever reason?

## Prompt 10

> That makes sense, and thank you for the correction. Can we add some code to handle these errors and notify the end user?
