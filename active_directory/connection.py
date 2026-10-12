import keyring
from ldap3 import Server, Connection, ALL


# --------------------------------------------------
# LACONIA ACTIVE DIRECTORY CONNECTION
# --------------------------------------------------

LDAP_SERVER = "192.168.10.10"
LDAP_BASE_DN = "DC=laconia,DC=local"
LDAP_USER = r"LACONIA\synfetcher"

# Retrieve SÝN's LDAP password securely from Windows Credential Manager.
LDAP_PASSWORD = keyring.get_password("SYN_LDAP", LDAP_USER)


def create_ldap_connection():
    """Create and authenticate an LDAP connection to the Laconia DC."""

    server = Server(
        LDAP_SERVER,
        port=389,
        get_info=ALL
    )

    connection = Connection(
        server,
        user=LDAP_USER,
        password=LDAP_PASSWORD,
        auto_bind=True
    )

    return connection
