<h1 align="center">NetBox Webhook Receiver</h1>

<p align="center"><i>NetBox Webhook Receiver is a NetBox plugin for managing webhook receiver endpoints and executing assigned actions.</i></p>

This plugin aims mainly to streamline the deployment process of scripts and export templates to Netbox by triggering the synchronisation of its Data Sources through incoming webhooks. Adding the receiver capability to Netbox opens other possible use cases, which might be worth exploring further. One example could be running Netbox Scripts triggered by remote events where it is not easy to execute a direct API call.

## Features
- [x] Per endpoint authentication (signature validation or custom header) on receiving webhooks
- [x] Webhook url enriched with automaticaly generated uuid value for additional security
- [x] Dedicated view to configure each webhook receiver url
- [x] Logical grouping of the receivers
- [x] Optionally store incoming webhook payload, shown in the receiver's Payloads tab
- [x] Custom actions execution on successfully receving authenticated webhook message. Currently only one action available: Synchronize Netbox git 'Data Source'
- [x] Use of standard Netbox jobs to queue webhook actions in the workers.
- [x] Plugin configuration parameters
- [ ] Additional actions to be implemented

## Requirements

* NetBox 4.7 or higher
* Python 3.12 or higher

## Compatibility

| NetBox version | Plugin version |
|----------------|----------------|
| 4.7 and later  | 0.6.x          |
| 4.1 - 4.6      | 0.5.x          |

## Installation & Configuration

For general knowledge about netbox plugin installation please refer to the official guide: [Using Plugins - NetBox Documentation](https://netbox.readthedocs.io/en/stable/plugins/)

Install NetBox Webhook Receiver:
```bash
$ source /opt/netbox/venv/bin/activate
(venv) $ pip install netbox-plugin-webhook-receiver
```

To register this plugin in NetBox, add _netbox_webhook_receiver_ to the config file. `~/netbox/configuration.py`

```python
PLUGINS = [
    "netbox_webhook_receiver",
]
```

Please remember that this plugin introduces new database models, therefore you must run the provided database schema migrations:
```bash
$ source /opt/netbox/venv/bin/activate
(venv) $ cd /opt/netbox/netbox/
(venv) $ python3 manage.py migrate
```

Optional settings can be set in `PLUGINS_CONFIG`:

```python
PLUGINS_CONFIG = {
    "netbox_webhook_receiver": {
        # Username the queued jobs are attributed to (default: None, jobs have no user)
        "job_user": "admin",
        # Number of days to keep stored webhook payloads (default: 2)
        "payload_retention_days": 2,
    },
}
```

## Usage

Create a Webhook Receiver and copy the URL shown on its page into the webhook configuration of the sending service.

* GitLab: use the Token method with the `X-Gitlab-Token` header and set the same value as the webhook secret token.
* GitHub: use the Signature Verification method with the `X-Hub-Signature-256` header and the SHA-256 algorithm, set the webhook secret to the same secret key and the content type to `application/json`.

When a Data Source is assigned, every authenticated webhook queues its synchronization. A webhook arriving while a synchronization is still waiting in the queue doesn't queue another one.

With "Store payload" enabled, the received payloads are listed in the Payloads tab of the receiver, which helps to check what the sending service posts. Payloads are kept for `payload_retention_days`.

Upgrading from 0.5.x: the receiver UUID becomes unique. The migration fails if two receivers share a UUID, so give them different UUIDs before running `migrate`. Stored payloads from 0.5.x aren't linked to any receiver and expire with the retention period.

## Screenshots

![Webhook Receivers](/docs/images/webhook_receivers.png)
![Webhook Receiver](/docs/images/webhook_receiver.png)
![Webhook Receiver Payloads](/docs/images/webhook_receiver_payloads.png)
![Webhook Receiver Group](/docs/images/webhook_receiver_group.png)
