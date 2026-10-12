from .connection import create_ldap_connection, LDAP_BASE_DN



# --------------------------------------------------
# ACTIVE DIRECTORY: GROUP MEMBERS(3)
# --------------------------------------------------

def get_group_members(group_name):

    # Connect to the Laconia Domain Controller.
    connection = create_ldap_connection()

    # Find the requested group.
    connection.search(
        LDAP_BASE_DN,
        f"(&(objectClass=group)(cn={group_name}))",
        attributes=["member"]
    )

    if not connection.entries:
        connection.unbind()
        return f"Group '{group_name}' was not found."

    # Build a readable list of the group's members.
    members = []

    for member_dn in connection.entries[0].member:
        member_name = str(member_dn).split(",")[0].replace("CN=", "")
        members.append(member_name)

    connection.unbind()

    if not members:
        return f"{group_name} has no listed members."

    return "\n".join(members)

