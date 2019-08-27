import os
import jprops
import requests
import io
import sys

ROOT_DIR = os.path.join(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, '.properties.cfg')


class ApplicationConfig:
    def __init__(self, url):
        try:
            props = self._from_local_config()
            self._set_props(props)
            return
        except FileNotFoundError:
            pass

        try:
            props = self._from_properties_url(url)
            self._set_props(props)
        except requests.exceptions.RequestException:
            # FIXME: do it in the better way
            sys.exit(1)

    def _set_props(self, props):
        self.eureka_url = props.get("eureka.client.serviceUrl.defaultZone")
        self.eureka_instance_name = props.get("eureka.instance.name")
        self.eureka_lease_renewal_interval_in_seconds = int(props.get("eureka.instance.leaseRenewalIntervalInSeconds", 5))
        self.eureka_registry_fetch_interval_seconds = int(props.get("eureka.client.registryFetchIntervalSeconds", 5))

    @staticmethod
    def _from_local_config() -> dict:
        with open(CONFIG_PATH, 'r') as file:
            return jprops.load_properties(file)

    @staticmethod
    def _from_properties_url(url) -> dict:
        session = requests.Session()
        session.trust_env = False
        response = session.get(url)
        props = jprops.load_properties(io.StringIO(response.text))
        session.close()
        return props
