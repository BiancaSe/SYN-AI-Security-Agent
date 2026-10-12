# --------------------------------------------------
# ACTIVE DIRECTORY TOOL DISPATCHER
# --------------------------------------------------

from .users import (
    list_ad_users,
    get_user_groups,
    get_user_details,
    get_user_status,
    get_password_expiration_status,
    get_password_last_changed,
    get_user_last_logon,
    get_account_lockout_status,
    unlock_user_account,
    set_user_enabled_status
)

from .groups import get_group_members
from .computers import list_ad_computers


AD_USER_FUNCTIONS = {
    "list_ad_users": list_ad_users,
    "get_user_groups": get_user_groups,
    "get_user_details": get_user_details,
    "get_user_status": get_user_status,
    "get_password_expiration_status": get_password_expiration_status,
    "get_password_last_changed": get_password_last_changed,
    "get_user_last_logon": get_user_last_logon,
    "get_account_lockout_status": get_account_lockout_status,
    "unlock_user_account": unlock_user_account,
    "set_user_enabled_status": set_user_enabled_status,
    
}

AD_GROUP_FUNCTIONS = {
    "get_group_members": get_group_members,
}
AD_COMPUTER_FUNCTIONS = {
    "list_ad_computers": list_ad_computers,
}


