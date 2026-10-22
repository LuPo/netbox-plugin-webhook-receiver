# NetBox configuration used to run the plugin tests in CI.
# Copied to netbox/netbox/configuration.py in the NetBox checkout.
from netbox.configuration_testing import *  # noqa: F401,F403

PLUGINS = ["netbox_webhook_receiver"]
