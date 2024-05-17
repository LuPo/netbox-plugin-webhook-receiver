<h1 align="center">NetBox Webhook Receiver</h1>

<p align="center"><i>NetBox Webhook Receiver is a NetBox plugin for managing webhook receiver endpoints and executing assigned actions.</i></p>

This plugin aims mainly to streamline the deployment process of scripts and export templates to Netbox by triggering the synchronisation of its Data Sources through incoming webhooks. Adding the receiver capability to Netbox opens other possible use cases, which might be worth exploring further. One example could be running Netbox Scripts triggered by remote events where it is not easy to execute a direct API call.

## Features
- [x] Per endpoint authentication (signature validation or custom header) on receiving webhooks
- [x] Webhook url enriched with automaticaly generated uuid value for additional security
- [x] Dedicated view to configure each webhook receiver url
- [x] Logical grouping of the receivers
- [x] Optionally store incoming webhook payload
- [x] Custom actions execution on successfully receving authenticated webhook message. Currently only one action available: Synchronize Netbox git 'Data Source'
- [x] Use of standard Netbox jobs to queue webhook actions in the workers.
- [ ] Additional actions to be implemented
- [ ] Plugin configuration parameters

## Requirements

* NetBox 4.0 or higher
* Python 3.10 or higher

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

## Screenshots

![Webhook Receivers](/docs/images/webhook_receivers.png)
![Webhook Receiver](/docs/images/webhook_receiver.png)
![Webhook Receiver Group](/docs/images/webhook_receiver_group.png)
