from .connection import create_ldap_connection, LDAP_BASE_DN



# --------------------------------------------------
# ACTIVE DIRECTORY: LIST COMPUTERS(2)
# --------------------------------------------------

def list_ad_computers():

    # Connect to the Laconia Domain Controller.
    connection = create_ldap_connection()

    # Search Active Directory for computer accounts.
    connection.search(
        LDAP_BASE_DN,
        "(objectClass=computer)",
        attributes=["name", "sAMAccountName"]
    )

    # Build a readable list for SYN.
    computers = []

    for entry in connection.entries:
        computers.append(
            f"{entry.name} ({entry.sAMAccountName})"
        )

    connection.unbind()

    return "\n".join(computers)


