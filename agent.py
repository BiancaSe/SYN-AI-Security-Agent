# --------------------------------------------------
# IMPORTS
# --------------------------------------------------


import requests

# Lets us read and write JSON.
import json

# Lets Python work with files and environment settings. 
import os

#Lets Python run Windows commands such as ping and nslookup.
import subprocess


 # Tests network services such as SMB
import socket 

# Lets Python communicate with LDAP/ Active Directory.
from ldap3 import Server, Connection, ALL


# 
from active_directory.tool_definitions import (
    AD_USER_TOOLS,
    AD_GROUP_TOOLS,
    AD_COMPUTER_TOOLS
)

#
from active_directory.dispatcher import (
    AD_USER_FUNCTIONS,
    AD_GROUP_FUNCTIONS,
    AD_COMPUTER_FUNCTIONS
)






# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

# Local Ollama API.
OLLAMA_URL = "http://localhost:11434/api/chat"

# Local AI model used as SYN's brain.
MODEL = "qwen3:4b"

# File used to save SYN's conversation memory.
MEMORY_FILE = "memory.json"

# Laconia Active Directory connection settings
LDAP_SERVER = "192.168.10.10"


# --------------------------------------------------
# SÝN PERSONALITY
# --------------------------------------------------

messages = [
    {
        "role": "system",
        "content": """
You are a cybersecurity lab assistant and your name is SÝN

Personality:
- Be concise and to the point.
- Answer simple questions with simple answers.
- Do not add unnecessary explanations.
- Do not use emojis. Greet me with "Heia Norge!" when I start a new conversation and when I
  say goodbye.
- Do not make jokes unless the user asks for humor.
- Explain technical topics in plain English.
- Give step-by-step instructions when teaching.
- Admit when you are unsure.
- When the user greets you with "Status", respond exactly:
 "Awaken! Systems ready! Awaiting instructions..."


Lab information:
- The Active Directory domain is laconia.local.
- The Laconia domain controller is 192.168.10.10.
- User's name is Freya.
- Never confuse the operator's identity with your own. Your name is SÝN.
- Use the ping_dc tool when you need to determine whether
  the Laconia domain controller is reachable.
- Use the check_dns tool when you need to determine whether
  Laconia DNS is responding.
- Use the check_ldap tool when you need to determine whether
  the Laconia LDAP service is reachable.
- Use the list_ad_users tool when the user asks about users or user accounts in Laconia.
- Use the list_ad_computers tool when the user asks about computers,
  machines, or computer accounts in Laconia.
- Use the smb_status tool when you need to determine whether the
  Laconia SMB service is reachable on port 445.
- Use the check_smb tool when you need to determine whether
  the Laconia SMB service is reachable on port 445.
- Use the check_kerberos tool when you need to determine whether the Laconia
  Kerberos service is reachable on port 88.


- TOOL USE RULES:
- Always check the available tools before saying you cannot access information.
- If a tool can answer the user's question, use the tool instead of answering from memory.
- For Active Directory questions, prefer querying the Laconia Active Directory tools.
- Never claim that Active Directory information is unavailable until you have checked
  whether an available tool can retrieve it.
"""
    }
]


# --------------------------------------------------
# LOAD SAVED MEMORY
# --------------------------------------------------


# If SYN already has a memory file, load the previous
# conversation and add it after the system message.

if os.path.exists(MEMORY_FILE):

    with open(MEMORY_FILE, "r") as file:

        old_messages = json.load(file)

        messages.extend(old_messages)


#SYN TOOLS
# --------------------------------------------------
# 1. PING DOMAIN CONTROLLER
# --------------------------------------------------

def ping_dc():

    # This tool is intentionally restricted.
    # It can ONLY ping our Laconia domain controller.
    dc_ip = "192.168.10.10"

    # Run the Windows ping command.
    # -n 2 means send two ping packets.
    result = subprocess.run(
        ["ping", "-n", "2", dc_ip],
        capture_output=True,
        text=True
    )

    # Return the real ping output to SÝN.

    return result.stdout



# --------------------------------------------------
# 2. CHECK LACONIA DNS
# --------------------------------------------------

def check_dns():

    # Ask our domain controller's DNS server
    # to resolve the Laconia domain.
    result = subprocess.run(
        ["nslookup", "laconia.local", "192.168.10.10"],
        capture_output=True,
        text=True
    )

    # Return the real nslookup output to SÝN.
    return result.stdout


#--------------------------------------------------
#3. CHECK LDAP CONNECTION
# --------------------------------------------------

def check_ldap():

    # Define the Laconia DC as the LDAP server.

    # LDAP normally uses TCP port 389.
    server = Server(
        "192.168.10.10",
        port=389,
        get_info=ALL,
        connect_timeout=3
    )

    # Create an LDAP connection object.
    # We are NOT logging into Active Directory yet.
    # This test only checks whether SYN can establish
    # an LDAP connection to the server.

    connection = Connection(server)

    try:

        # Open the connection to the LDAP server.
        if connection.open():

            
            # Close the connection after the test.
            connection.close()

            return "LDAP is reachable on 192.168.10.10 port 389."

        else:

            return "LDAP connection failed."

    except Exception as error:

        return f"LDAP connection failed: {error}"


# --------------------------------------------------
# CHECK SMB CONNECTION
# --------------------------------------------------

def check_smb():
    try:
        connection = socket.create_connection(
            (LDAP_SERVER, 445),
            timeout=2
        )
        connection.close()
        return "SMB is reachable on 192.168.10.10 port 445."

    except OSError as error:
        return f"SMB connection failed: {error}"


# --------------------------------------------------
# CHECK KERBEROS CONNECTION 
# --------------------------------------------------

def check_kerberos():
    try:
        connection = socket.create_connection(
            (LDAP_SERVER, 88),
            timeout=2
        )
        connection.close()
        return "Kerberos is reachable on 192.168.10.10 port 88."

    except OSError as error:
        return f"Kerberos connection failed: {error}"




#--------------------------------------------------  
# TELL QWEN WHICH TOOLS EXIST
# --------------------------------------------------

# These definitions tell Qwen which Python tools SÝN is allowed to use.
# Qwen does not run these functions itself.
# Qwen decides which tool is appropriate, and
# agent.py runs the actual Python function.

TOOLS = [

    #PING TOOL

    {
        "type": "function",
        "function": {
            "name": "ping_dc",
            "description":
                "Ping the Laconia domain controller at "
                "192.168.10.10 to determine whether it is reachable.",

            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },


    #DNS TOOL

    {
    "type": "function",
    "function": {
        "name": "check_dns",
        "description":
          "Check whether Laconia DNS is working by resolving laconia.local "
          "using the domain controller at 192.168.10.10.",

        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
},


    #LDAP TOOL

    {
        "type": "function",
        "function": {
            "name": "check_ldap",
            "description":
                "Check whether the LDAP service on the Laconia domain "
                "controller at 192.168.10.10 port 389 is reachable.",

            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },


#SMB TOOL
{
    "type": "function",
    "function": {
        "name": "check_smb",
        "description": "Checks whether the Laconia SMB service is reachable on port 445.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
},

#KERBEROS TOOL

{
    "type": "function",
    "function": {
        "name": "check_kerberos",
        "description": "Checks whether the Laconia Kerberos service is reachable on port 88.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

]

TOOLS.extend(AD_USER_TOOLS)
TOOLS.extend(AD_GROUP_TOOLS)
TOOLS.extend(AD_COMPUTER_TOOLS)


# ASK SÝN


def ask_agent(user_input):

    # Add the user's message to SÝN's conversation history.

    messages.append({
        "role": "user",
        "content": user_input
    })

    # Ask Qwen what to do.

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "tools": TOOLS,
            "stream": False
        }
    )

    data = response.json()
    message = data["message"]

    # Did Qwen request a tool?

    if message.get("tool_calls"):

      # Remember Qwen's tool request.
    
        messages.append(message)

     # Qwen may request one or more tools. DISPATCHER

        for tool_call in message["tool_calls"]:

            tool_name = tool_call["function"]["name"]

                     # RUN PING TOOL

            if tool_name == "ping_dc":

                print("[Running ping_dc...]")
                tool_result = ping_dc()

            # RUN DNS TOOL

            elif tool_name == "check_dns":

                print("[Running check_dns...]")
                tool_result = check_dns()

            # RUN LDAP TOOL

            elif tool_name == "check_ldap":

                print("[Running check_ldap...]")
                tool_result = check_ldap()

            # RUN SMB TOOL
            
            elif tool_name == "check_smb":

                print("[Running check_smb...]")
                tool_result = check_smb()

            # RUN KERBEROS TOOL
            elif tool_name == "check_kerberos":
                tool_result = check_kerberos()

         
     
           

           
            # RUN ACTIVE DIRECTORY USER TOOLS
            elif tool_name in AD_USER_FUNCTIONS:
                arguments = tool_call["function"]["arguments"]
                tool_result = AD_USER_FUNCTIONS[tool_name](**arguments)

            # RUN ACTIVE DIRECTORY GROUP TOOLS
            elif tool_name in AD_GROUP_FUNCTIONS:
                arguments = tool_call["function"]["arguments"]
                tool_result = AD_GROUP_FUNCTIONS[tool_name](**arguments)


            # RUN ACTIVE DIRECTORY COMPUTER TOOLS
            elif tool_name in AD_COMPUTER_FUNCTIONS:
                arguments = tool_call["function"]["arguments"]
                tool_result = AD_COMPUTER_FUNCTIONS[tool_name](**arguments)




            #UNKNOWN TOOL

            else:

                tool_result = "Unknown tool."

            # Give the tool result back to Qwen.

            messages.append({
                "role": "tool",
                "tool_name": tool_name,
                "content": tool_result
            })


        # Ask Qwen to interpret the result.

        final_response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "tools": TOOLS,
                "stream": False
            }
        )

        final_data = final_response.json()
        answer = final_data["message"]["content"]

        # No Tool was requested, just return Qwen's answer.

    else:

        answer = message["content"]


    # Remember SÝN's answer.

    messages.append({
        "role": "assistant",
        "content": answer
    })

    # Save memory.
    # messages[0] is the permanent system prompt.
    # We do not save it into memory.json because
    # agent.py creates it every time SÝN starts.


    with open(MEMORY_FILE, "w") as file:
        json.dump(messages[1:], file, indent=4)

    # Give SÝN's final answer back to whichever
    # interface called ask_agent().
    #
    # This could be the terminal or web_agent.py.

    return answer


# --------------------------------------------------
# TERMINAL MODE
# --------------------------------------------------

# This section runs ONLY when agent.py is started
# directly with:
#
#     python agent.py
#
# It does NOT run when web_agent.py imports agent.py.


if __name__ == "__main__":

    while True:

        user_input = input("You: ")

         # Allow us to leave terminal mode.

        if user_input.lower() in ["exit", "quit"]:
            print("SÝN: Heia Norge!")
            break

        answer = ask_agent(user_input)

        print("SÝN:", answer)

     