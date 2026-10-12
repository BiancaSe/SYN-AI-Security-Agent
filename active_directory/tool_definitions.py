# --------------------------------------------------
# ACTIVE DIRECTORY TOOL DEFINITIONS FOR SÝN
# --------------------------------------------------


AD_USER_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_user_groups",
            "description": "Gets the Active Directory groups that a specified Laconia user belongs to.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The Active Directory username, for example Duarte."
                    }
                },
                "required": ["username"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_user_details",
            "description": "Gets detailed information about a specified Active Directory user in Laconia, including name, username, account status, OU location, and group memberships.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The Active Directory username, for example Duarte."
                    }
                },
                "required": ["username"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_user_status",
            "description": "Checks whether a Laconia Active Directory user account is enabled or disabled.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The Active Directory username, for example Duarte."
                    }
                },
                "required": ["username"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_password_expiration_status",
            "description": "Checks the password expiration status of a Laconia Active Directory user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The Active Directory username, for example Duarte."
                    }
                },
                "required": ["username"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_password_last_changed",
            "description": "Gets the date and time when a Laconia Active Directory user's password was last changed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The Active Directory username, for example Duarte."
                    }
                },
                "required": ["username"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_user_last_logon",
            "description": "Gets the approximate last logon date and time for a Laconia Active Directory user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The Active Directory username, for example Duarte."
                    }
                },
                "required": ["username"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_account_lockout_status",
            "description": "Checks whether a Laconia Active Directory user account is currently locked out.",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The Active Directory username, for example Duarte."
                    }
                },
                "required": ["username"]
            }
        }
    },



    {
        "type": "function",
        "function": {
            "name": "list_ad_users",
            "description": "Lists the users in the Laconia Active Directory domain.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
    "type": "function",
    "function": {
        "name": "unlock_user_account",
        "description": "Unlocks a locked Laconia Active Directory user account.",
        "parameters": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "The Active Directory username to unlock, for example testuser."
                }
            },
            "required": ["username"]
        }
    }
},

{
    "type": "function",
    "function": {
        "name": "set_user_enabled_status",
        "description": "Enables or disables a Laconia Active Directory user account.",
        "parameters": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "The Active Directory username, for example testuser."
                },
                "enabled": {
                    "type": "boolean",
                    "description": "True enables the account. False disables the account."
                }
            },
            "required": ["username", "enabled"]
        }
    }
}

]

AD_GROUP_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_group_members",
            "description": "Lists the members of a specified Laconia Active Directory group.",
            "parameters": {
                "type": "object",
                "properties": {
                    "group_name": {
                        "type": "string",
                        "description": "The Active Directory group name, for example Laconian-Admins."
                    }
                },
                "required": ["group_name"]
            }
        }
    }
]


AD_COMPUTER_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_ad_computers",
            "description": "Lists the computers in the Laconia Active Directory domain.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

