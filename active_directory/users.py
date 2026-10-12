
#IMPORTS#

from .connection import create_ldap_connection, LDAP_BASE_DN
from ldap3 import MODIFY_REPLACE





# --------------------------------------------------
# ACTIVE DIRECTORY: LIST USERS (1)
# --------------------------------------------------

def list_ad_users():

    # Connect to the Laconia Domain Controller.
    connection = create_ldap_connection()

    # Search Active Directory for user accounts.
    connection.search(
        LDAP_BASE_DN,
        "(&(objectCategory=person)(objectClass=user))",
        attributes=["displayName", "sAMAccountName"]
    )

    # Build a readable list for SYN.
    users = []

    for entry in connection.entries:

        username = str(entry.sAMAccountName)

        if username in ["Administrator", "Guest", "krbtgt"]:
            continue

        users.append(
        f"{entry.displayName} ({entry.sAMAccountName})"
    )

    connection.unbind()

    return "\n".join(users)


# --------------------------------------------------
# ACTIVE DIRECTORY: USER GROUP MEMBERSHIP
# --------------------------------------------------

def get_user_groups(username):

    connection = create_ldap_connection()

    connection.search(
        LDAP_BASE_DN,
        f"(sAMAccountName={username})",
        attributes=["memberOf"]
    )

    if not connection.entries:
        connection.unbind()
        return f"User '{username}' was not found."

    groups = []

    for group_dn in connection.entries[0].memberOf:
        group_name = str(group_dn).split(",")[0].replace("CN=", "")
        groups.append(group_name)

    connection.unbind()

    if not groups:
        return f"{username} is not a member of any listed groups."

    return "\n".join(groups)

# --------------------------------------------------
# ACTIVE DIRECTORY: USER DETAILS
# --------------------------------------------------

def get_user_details(username):

    connection = create_ldap_connection()

    connection.search(
        LDAP_BASE_DN,
        f"(&(objectClass=user)(sAMAccountName={username}))",
        attributes=[
            "displayName",
            "sAMAccountName",
            "distinguishedName",
            "memberOf",
            "userAccountControl",
            "pwdLastSet",
            "lastLogonTimestamp"
        ]
    )

    if not connection.entries:
        connection.unbind()
        return f"User '{username}' was not found."

    user = connection.entries[0]

    display_name = str(user.displayName) if user.displayName else "Not set"
    account_name = str(user.sAMAccountName)

    uac = int(user.userAccountControl.value)
    enabled = "No" if uac & 2 else "Yes"

    distinguished_name = str(user.distinguishedName)

    ou_parts = [
        part.replace("OU=", "")
        for part in distinguished_name.split(",")
        if part.startswith("OU=")
    ]

    ou = " > ".join(ou_parts) if ou_parts else "Default Users container"

    groups = []

    if user.memberOf:
        for group_dn in user.memberOf:
            group_name = str(group_dn).split(",")[0].replace("CN=", "")
            groups.append(group_name)

    connection.unbind()

    result = [
        f"Name: {display_name}",
        f"Username: {account_name}",
        f"Enabled: {enabled}",
        f"Location: {ou}",
        "Groups:"
    ]

    if groups:
        for group in groups:
            result.append(f"  - {group}")
    else:
        result.append("  - None listed")

    return "\n".join(result)

# --------------------------------------------------
# ACTIVE DIRECTORY: USER ACCOUNT STATUS
# --------------------------------------------------

def get_user_status(username):

    connection = create_ldap_connection()

    connection.search(
        LDAP_BASE_DN,
        f"(&(objectClass=user)(sAMAccountName={username}))",
        attributes=["displayName", "sAMAccountName", "userAccountControl"]
    )

    if not connection.entries:
        connection.unbind()
        return f"User '{username}' was not found."

    user = connection.entries[0]

    # Flag 2 means ACCOUNTDISABLE.
    uac = int(user.userAccountControl.value)

    if uac & 2:
        status = "Disabled"
    else:
        status = "Enabled"

    display_name = str(user.displayName) if user.displayName else username

    connection.unbind()

    return f"{display_name} ({username}): {status}"


# --------------------------------------------------
# ACTIVE DIRECTORY: PASSWORD EXPIRATION STATUS
# --------------------------------------------------

def get_password_expiration_status(username):

    connection = create_ldap_connection()

    connection.search(
        LDAP_BASE_DN,
        f"(&(objectClass=user)(sAMAccountName={username}))",
        attributes=[
            "displayName",
            "sAMAccountName",
            "userAccountControl",
            "pwdLastSet"
        ]
    )

    if not connection.entries:
        connection.unbind()
        return f"User '{username}' was not found."

    user = connection.entries[0]

    display_name = (
        str(user.displayName)
        if user.displayName
        else username
    )

    uac = int(user.userAccountControl.value)

    # ADS_UF_DONT_EXPIRE_PASSWD = 0x10000
    password_never_expires = bool(uac & 0x10000)

    pwd_last_set = user.pwdLastSet.value

    connection.unbind()

    if password_never_expires:
        status = "Password never expires"
    elif pwd_last_set is None or str(pwd_last_set) == "0":
        status = "Password must be changed at next logon"
    else:
        status = "Password is subject to the domain password expiration policy"

    return f"{display_name} ({username}): {status}"

# --------------------------------------------------
# ACTIVE DIRECTORY: PASSWORD LAST CHANGED
# --------------------------------------------------

def get_password_last_changed(username):

    connection = create_ldap_connection()

    connection.search(
        LDAP_BASE_DN,
        f"(&(objectClass=user)(sAMAccountName={username}))",
        attributes=[
            "displayName",
            "sAMAccountName",
            "pwdLastSet"
        ]
    )

    if not connection.entries:
        connection.unbind()
        return f"User '{username}' was not found."

    user = connection.entries[0]

    display_name = (
        str(user.displayName)
        if user.displayName
        else username
    )

    pwd_last_set = user.pwdLastSet.value

    connection.unbind()

    if not pwd_last_set:
        return f"{display_name} ({username}): Password has not been set."

    return (
        f"{display_name} ({username}): "
        f"Password last changed: {pwd_last_set}"
    )


# --------------------------------------------------
# ACTIVE DIRECTORY: USER LAST LOGON
# --------------------------------------------------

def get_user_last_logon(username):

    connection = create_ldap_connection()

    connection.search(
        LDAP_BASE_DN,
        f"(&(objectClass=user)(sAMAccountName={username}))",
        attributes=[
            "displayName",
            "sAMAccountName",
            "lastLogonTimestamp"
        ]
    )

    if not connection.entries:
        connection.unbind()
        return f"User '{username}' was not found."

    user = connection.entries[0]

    display_name = (
        str(user.displayName)
        if user.displayName
        else username
    )

    last_logon = user.lastLogonTimestamp.value

    connection.unbind()

    if not last_logon:
        return f"{display_name} ({username}): No last logon timestamp found."

    return (
        f"{display_name} ({username}): "
        f"Last logon: {last_logon}"
    )


# --------------------------------------------------
# ACTIVE DIRECTORY: ACCOUNT LOCKOUT STATUS
# --------------------------------------------------

def get_account_lockout_status(username):

    connection = create_ldap_connection()

    connection.search(
        LDAP_BASE_DN,
        f"(&(objectClass=user)(sAMAccountName={username}))",
        attributes=[
            "displayName",
            "sAMAccountName",
            "lockoutTime"
        ]
    )

    if not connection.entries:
        connection.unbind()
        return f"User '{username}' was not found."

    user = connection.entries[0]

    display_name = (
        str(user.displayName)
        if user.displayName
        else username
    )

    lockout_time = user.lockoutTime.value

    connection.unbind()

    if not lockout_time or str(lockout_time) == "0":
        return f"{display_name} ({username}): Not locked out"

    return f"{display_name} ({username}): Locked out"



#--------------------------------------------------
# ACTIVE DIRECTORY: UNLOCK USER ACCOUNTS
# --------------------------------------------------


def unlock_user_account(username):
    connection = create_ldap_connection()

    connection.search(
        LDAP_BASE_DN,
        f"(&(objectClass=user)(sAMAccountName={username}))",
        attributes=["displayName", "distinguishedName", "lockoutTime"]
    )

    if not connection.entries:
        connection.unbind()
        return f"User '{username}' was not found."

    user = connection.entries[0]

    display_name = (
        str(user.displayName)
        if user.displayName
        else username
    )

    user_dn = str(user.distinguishedName)
    lockout_time = user.lockoutTime.value

    # Do nothing if the account is already unlocked.
    if not lockout_time or str(lockout_time) == "0":
        connection.unbind()
        return f"{display_name} ({username}): Account is not locked out."

    # Setting lockoutTime to 0 unlocks the AD account.
    success = connection.modify(
        user_dn,
        {
            "lockoutTime": [
                (MODIFY_REPLACE, [0])   
          ]
        }
    )

    if success:
        connection.unbind()
        return f"{display_name} ({username}): Account unlocked successfully."

    error = connection.result
    connection.unbind()

    return f"Failed to unlock {display_name} ({username}): {error}"



#--------------------------------------------------
# ACTIVE DIRECTORY: Enable/Disable  USER ACCOUNTS
# --------------------------------------------------

def set_user_enabled_status(username, enabled):
    connection = create_ldap_connection()

    connection.search(
        LDAP_BASE_DN,
        f"(&(objectClass=user)(sAMAccountName={username}))",
        attributes=[
            "displayName",
            "distinguishedName",
            "userAccountControl"
        ]
    )

    if not connection.entries:
        connection.unbind()
        return f"User '{username}' was not found."

    user = connection.entries[0]

    display_name = (
        str(user.displayName)
        if user.displayName
        else username
    )

    user_dn = str(user.distinguishedName)
    current_uac = int(user.userAccountControl.value)

    # ACCOUNTDISABLE is bit 2 in userAccountControl.
    if enabled:
        new_uac = current_uac & ~2
        action = "enabled"
    else:
        new_uac = current_uac | 2
        action = "disabled"

    # Avoid making an unnecessary AD change.
    if new_uac == current_uac:
        connection.unbind()

        current_state = "enabled" if enabled else "disabled"
        return f"{display_name} ({username}) is already {current_state}."

    success = connection.modify(
        user_dn,
        {
            "userAccountControl": [
                (MODIFY_REPLACE, [new_uac])
            ]
        }
    )

    if success:
        connection.unbind()
        return f"{display_name} ({username}) successfully {action}."

    error = connection.result
    connection.unbind()

    return f"Failed to change {display_name} ({username}): {error}"