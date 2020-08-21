#Zoho Desk API Integration

This integration uses the Serverless Framework to deploy functions that interact with Zoho Desk's RESTful API.
An authentication layer is set up so that a all a user needs to pass in is the route in Zoho Desk they want to hit,
and the secret_id containing their OAuth2 information. All authentication is done using the OAuth2 flow, and is 
completely automated after an initial request with minimal user interaction is made.

## Instructions for Setup:

* Initially, a self-client and web client will need to be created, even if the web client has a dummy redirect_uri
value. Gather the below information and input into Secrets Manager as json plaintext, so that it is ready after you
generate an authorization code in step 2 (the code is only good for 10 minutes).
```
{
    "client_id": "From self-client",
    "client_secret": "From self-client,
    "redirect_uri": "from web client",
    "code": "Authorization code/grant token that is generated from self-client (scope to use is below)",
    "org_id": "from Zoho Desk API settings page"
}
```
* Next, use the self-client to generate an authorization code (named code in Secrets Manager) using the correct scope.
The below scope gives all access. If you only need some access, choose the correct scopes from below.
All scopes should be separated by commas, no spaces. Please note that `AAAServer.profile.ALL` **must** be included in
**all scopes**.

```
Desk.tickets.ALL,Desk.activities.calls.READ,Desk.tasks.ALL,Desk.settings.ALL,Desk.search.READ,Desk.events.ALL,
Desk.articles.READ,Desk.articles.CREATE,Desk.articles.UPDATE,Desk.articles.DELETE,Desk.contacts.READ,Desk.contacts.WRITE,
Desk.contacts.UPDATE,Desk.contacts.CREATE,Desk.basic.READ,Desk.basic.CREATE,AAAServer.profile.ALL, Desk.activities.READ
```
* Enter the authorization code into the secret, saved with the key `code`.

## Instructions for calling Zoho Desk's API directly (in AWS Lambda)

* To call a route, simply pass in the path from Zoho's API docs (found https://desk.zoho.com/DeskAPIDocument#Introduction)
as well as the secret_id (secret name) where your information is stored into the event of the lambda function.

Example:
```
{
    "path": "tickets",
    "secret_id": "zoho-integration"
}
```
The above call will return a list of all tickets associated with the Zoho Desk account specified in the
Secrets Manager.

If a route requires added information (i.e. a ticket id, agent id, etc) look at Zoho's API docs and see how the route
is formatted, then pass it in with the correct information. For example, instead of listing all tickets, you could pass
in the following to list only a single ticket, with id 1234567:
```
{
    "path": "tickets/1234567",
    "secret_id": "zoho-integration"
}
```

## Scheduled Events
This integration with Zoho's Desk API has scheduled events that call the following routes one time a day. Each time the
route is called, the resulting dictionary of data is saved into a json file and saved in an S3 bucket.

Routes called once a day:
- Accounts (lists all accounts)
- Agents (lists all agents)
- Agent Time Entry (lists all time entries for a particular agent)
- Calls (lists all calls)
- Contacts (lists all contacts)
- Customer Happiness ()
- Departments (lists all departments)
- Notification (email delivery failures- lists all failures to deliver via email)
- Notification (pending approval- )
- Queue (lists all tickets by status in queue)
- Threads (lists all threads for a particular ticket)
- Ticket Tags (lists all available tags for tickets)
- Ticket Time Entry (lists all time entries for a particular ticket)
- Ticket (lists all tickets)