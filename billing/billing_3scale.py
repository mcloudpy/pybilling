import requests
import xmltodict
from billing import BillingException


DOMAIN_SERVER = "http://su1.3scale.net"


def create_application(admin_server, provider_key, account_id, plan_id, name, description):
    """
    Creates a new Application and returns the user_key for the new application, which is what is needed
    to report usage for it.

    @param admin_server: URL of the 3scale admin server (which will be <something>-admin.3scale.net). This is related
    to the entity that is created when you first register the project on 3scale.
    @param provider_key: Provider key, which is related to the same 3scale entity.
    @param account_id: A 3scale entity can have several accounts. This should be the ID of the account through which
    to create the Application.
    @param plan_id: The ID of the Application Plan to assign to the new Application.
    @param name: Name of the new Application.
    @param description: Description of the new Application.

    @return: The new Application's user_key. The user_key is required for usage reporting operations.
    """

    ret = requests.post("%s/admin/api/accounts/%s/applications.xml" % (admin_server, account_id), data=dict(
        provider_key=provider_key,
        plan_id=plan_id,
        name=name,
        description=description
    ))

    if ret.status_code != 201:
        raise BillingException("Create Application failed: %d %s" % (ret.status_code, ret.text))

    response = xmltodict.parse(ret.text)
    application = response["application"]

    return application["user_key"]


class ThreescaleBilling(object):
    """
    Class for Billing the 3scale service.
    """

    def __init__(self, provider_key, user_key):
        """
        Initializes the 3scale billing object.

        @param provider_key: 3scale Provider Key, linked to the 3scale instance
        @param user_key: 3scale User Key, linked to the specific Application. A Provider can have many Applications.
        """
        self._provider_key = provider_key
        self._user_key = user_key

    def report_hits(self, hits):
        """
        Reports Hits to the 3scale application.
        @param hits: The number of hits.
        """
        if hits < 0:
            raise BillingException("Error. Reported hits must be a positive integer.")
        ret = requests.get("%s/transactions/authrep.xml" % DOMAIN_SERVER, params=dict(
            {"usage[hits]": hits},
            provider_key=self._provider_key,
            user_key=self._user_key,
        ))
        if ret.status_code != 200:
            raise BillingException("Error reporting hits. Code: %s. Reason: %s" % (ret.status_code, ret.text))

    def report_time(self, time):
        """
        Reports time spent to the 3scale Application.
        @time: Time spent, in seconds.
        """
        if time < 0:
            raise BillingException("Error. Reported time must be a positive integer.")
        ret = requests.get("%s/transactions/authrep.xml" % DOMAIN_SERVER, params=dict(
            {"usage[time]": time},
            provider_key=self._provider_key,
            user_key=self._user_key
        ))
        if ret.status_code != 200:
            raise BillingException("Error reporting time. Code: %s. Reason: %s" % (ret.status_code, ret.text))