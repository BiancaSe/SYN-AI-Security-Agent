# ==================================================
# SÝN WEB INTERFACE
# Laconia Cybersecurity Lab
# ==================================================


# --------------------------------------------------
# IMPORTS
# --------------------------------------------------


# Used for checking TCP services such as
# LDAP, Kerberos, and SMB.
import socket

# Used for checking the Domain Controller
# and DNS from Windows.
import subprocess

# Used when clearing SÝN's saved memory file.
import os

# Flask powers SÝN's local web interface.
from flask import Flask, request, render_template_string, redirect

# Import SÝN's actual brain, conversation memory,
# and memory file from agent.py.
from agent import ask_agent, messages, MEMORY_FILE


# --------------------------------------------------
# FLASK APPLICATION
# --------------------------------------------------

app = Flask(__name__)


# ==================================================
# DASHBOARD STATUS CHECKS
# ==================================================


# --------------------------------------------------
# DOMAIN CONTROLLER STATUS 
# --------------------------------------------------

def dc_status():

    # Ping the Laconia Domain Controller once.

    result = subprocess.run(
        ["ping", "-n", "1", "192.168.10.10"],
        capture_output=True,
        text=True
    )

    # A return code of 0 means the ping succeeded.

    return result.returncode == 0


# --------------------------------------------------
# DASHBOARD: DNS STATUS 
# --------------------------------------------------

def dns_status():

    # Ask the Laconia DNS server to resolve laconia.local.
    result = subprocess.run(
        ["nslookup", "laconia.local", "192.168.10.10"],
        capture_output=True,
        text=True
    )

    output = result.stdout.lower()

    # Return True if the expected Laconia information
    # appears in the DNS response.
    return "192.168.10.10" in output and "laconia.local" in output


# --------------------------------------------------
# DASHBOARD: TCP STATUS 
# --------------------------------------------------


def service_status(port):

    # Attempt to connect to a specific TCP port
    # on the Laconia Domain Controller.

    try:

        connection = socket.create_connection(
            ("192.168.10.10", port),
            timeout=2
        )

        connection.close()

        return True

    except OSError:

        return False


# --------------------------------------------------
# LDAP STATUS
# --------------------------------------------------

def ldap_status():

    # LDAP uses TCP port 389.

    return service_status(389)


# --------------------------------------------------
# KERBEROS STATUS
# --------------------------------------------------

def kerberos_status():

    # Kerberos uses TCP port 88.

    return service_status(88)


# --------------------------------------------------
# SMB STATUS
# --------------------------------------------------

def smb_status():

    # SMB uses TCP port 445.

    return service_status(445)





# --------------------------------------------------
# WEB PAGE
# --------------------------------------------------

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>SÝN</title>

    <style>
    
    @import url('https://fonts.googleapis.com/css2?family=Caesar+Dressing&display=swap');
    body {
        background: #0b0f14;
        color: #d8e6f3;
        font-family: Consolas, monospace;
        max-width: 900px;
        margin: 15px auto;
    }


h1 {
    font-family: "Caesar Dressing", fantasy;
    font-size: 52px;
    letter-spacing: 12px;
    color: #4da6ff;
    text-shadow: 0 0 10px #4da6ff;
}
   


   input {
    background: #111820;
    color: #d8e6f3;
    border: 1px solid #4da6ff;
    border-radius: 6px;
    padding: 12px;
    width: 600px;
    outline: none;
    box-shadow: 0 0 6px #4da6ff;
}

input:focus {
    border-color: #4da6ff;
    box-shadow: 0 0 14px #4da6ff;
}
    

    button {
        padding: 3px 10px;
        font-size: 12px;
        background: #4da6ff;`
        cursor: pointer;
    }

    .console {
    margin-top: 12px;
    padding: 12px;
    background: #080c10;
    border: 1px solid #4da6ff;
    border-radius: 8px;
    box-shadow: 0 0 12px #4da6ff;
    min-height: 40px;
}

.console strong {
    color: #4da6ff;
}

.status-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    column-gap: 30px;
    row-gap: 2px;
}

.status {
    margin-bottom: 10px;
    font-size: 14px;
    letter-spacing: 2px;
}

.status-light {
    display: inline-block;
    width: 10px;
    height: 10px;
    background: #00ff88;
    border-radius: 50%;
    margin-right: 8px;
    box-shadow: 0 0 10px #00ff88;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%   { opacity: 1; }
    50%  { opacity: 0.3; }
    100% { opacity: 1; }
}

.status-light.online {
    background: #00ff88;
    box-shadow: 0 0 10px #00ff88;
}

.status-light.offline {
    background: #ff3b3b;
    box-shadow: 0 0 10px #ff3b3b;
}

.health-panel {
    width: 50%;
    margin-top: 8px;
    padding: 5px 10px;
    background: #080c10;
    border: 1px solid #4da6ff;
    border-radius: 8px;
}

.health-panel h2 {
    font-size: 16px;
    letter-spacing: 3px;
    margin-bottom: 3px 0;
}

.health-good {
    color: #00ff88;
    font-weight: bold;
}

.health-bad {
    color: #ff3b3b;
    font-weight: bold;
}

.user-message {
    margin: 15px 0;
    padding: 12px;
    background: #151c24;
    border-left: 3px solid #aaaaaa;
    border-radius: 5px;
}

.syn-message {
    margin: 15px 0;
    padding: 12px;
    background: #0c1824;
    border-left: 3px solid #4da6ff;
    border-radius: 5px;
}

.syn-message strong {
    color: #4da6ff;
}


.hero-image {
    width: 100%;
    max-width: 900px;
    border-radius: 12px;
    margin-bottom: 25px;
    box-shadow: 0 0 18px #4da6ff;
}


    </style>

</head>


<body>



<img
    src="/static/syn_dashboard.png"
    class="hero-image"
>

<div class="status-grid">
<div class="status">
    <span class="status-light {% if dc_online %}online{% else %}offline{% endif %}"></span>

    {% if dc_online %}
        LACONIA DC ONLINE
    {% else %}
        LACONIA DC OFFLINE
    {% endif %}
</div>



<div class="status">
    <span class="status-light {% if dns_online %}online{% else %}offline{% endif %}"></span>

    {% if dns_online %}
        LACONIA DNS ONLINE
    {% else %}
        LACONIA DNS OFFLINE
    {% endif %}
</div>


<div class="status">
    <span class="status-light {% if ldap_online %}online{% else %}offline{% endif %}"></span>

    {% if ldap_online %}
        LDAP :389 ONLINE
    {% else %}
        LDAP :389 OFFLINE
    {% endif %}
</div>



<div class="status">
    <span class="status-light {% if kerberos_online %}online{% else %}offline{% endif %}"></span>

    {% if kerberos_online %}
        KERBEROS :88 ONLINE
    {% else %}
        KERBEROS :88 OFFLINE
    {% endif %}
</div>



<div class="status">

    <span class="status-light {% if smb_online %}online{% else %}offline{% endif %}"></span>

    {% if smb_online %}
        SMB :445 ONLINE
    {% else %}
        SMB :445 OFFLINE
    {% endif %}
</div>
</div>

<div class="health-panel">
    <h2>LACONIA SYSTEM STATUS</h2>

    {% if dc_online and dns_online and ldap_online and kerberos_online and smb_online %}
        <div class="health-good">ALL SYSTEMS OPERATIONAL</div>
    {% else %}
        <div class="health-bad">SYSTEM ATTENTION REQUIRED</div>
    {% endif %}
</div>

<form method="POST">
    <input
        type="text"
        name="message"
        style="width: 500px;"
        autofocus
    >

    <button type="submit">
        Send
    </button>
</form>

<form method="POST" action="/clear">
    <button type="submit">
        CLEAR CHAT
    </button>
</form>

<div class="console">

    {% for message in chat_messages %}

        {% if message.role == "user" %}
            <div class="user-message">
                <strong>YOU:</strong>
                <p>{{ message.content }}</p>
            </div>

        {% elif message.role == "assistant" and message.content %}
            <div class="syn-message">
                <strong>SYN:</strong>
                <p>{{ message.content }}</p>
            </div>
        {% endif %}

    {% endfor %}

</div>

</body>
</html>
"""


# --------------------------------------------------
# WEB SERVER: CLEAR CHAT
# --------------------------------------------------

@app.route("/clear", methods=["POST"])
def clear_chat():

    # Keep SÝN's system/personality message.
    system_message = messages[0]

    # Remove the conversation history.
    messages.clear()

    # Put SÝN's system/personality message back.
    messages.append(system_message)

    # Delete the saved chat memory.
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)

    # Return to the main dashboard.
    return redirect("/")


# --------------------------------------------------
# WEB SERVER: MAIN PAGE
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    # If the user sends a message from the webpage,
    # send it to SÝN.
    if request.method == "POST":
        user_input = request.form["message"]
        ask_agent(user_input)

    # Build the webpage with the current
    # Laconia status and chat history.
    return render_template_string(
        PAGE,
        dc_online=dc_status(),
        dns_online=dns_status(),
        ldap_online=ldap_status(),
        kerberos_online=kerberos_status(),
        smb_online=smb_status(),
        chat_messages=messages
    )


# --------------------------------------------------
# START WEB SERVER
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
