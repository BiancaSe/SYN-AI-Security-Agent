
# SÝN — AI Security Agent

## Project Overview

**SÝN** (named after the Norse goddess associated with defense and boundary keeping) is a Python-based, locally hosted AI security agent I am developing as part of my [Laconia Cybersecurity Lab](https://github.com/BiancaSe/Laconia-Cybersecurity-Lab).

The project explores how a locally hosted large language model (LLM) can interact with enterprise infrastructure through purpose-built Python tools.

SÝN translates natural-language requests into Active Directory queries and administrative operations, combining AI-assisted interaction, Python automation, and LDAP.

The long-term goal is to develop SÝN into a security operations assistant supporting identity administration, infrastructure monitoring, security investigations, and incident response within a controlled lab environment.

## Technologies

| Component | Technology |
|---|---|
| Programming language | Python |
| Local AI runtime | Ollama |
| Language model | Qwen3 4B |
| Web interface | Flask, HTML, CSS |
| Directory communication | LDAP / ldap3 |
| Credential storage | Python keyring |
| Directory service | Microsoft Active Directory |
| Domain controller | Windows Server 2019 |
| Virtualization | VMware Workstation |
| Development environment | Visual Studio Code |

## Architecture

SÝN operates locally and connects to the Laconia Active Directory environment using a dedicated LDAP service account.

The application separates AI interaction, tool definitions, execution logic, and Active Directory operations into modular Python components.

**Request workflow:**

1. A user submits a natural-language request through the web interface or agent.
2. Ollama runs the locally hosted Qwen3 model to interpret the request.
3. The Python dispatcher executes the selected tool.
4. The tool communicates with Active Directory through LDAP.
5. SÝN returns the result to the user.

**Architecture diagram:**

```text
        USER
          |
          v
   Flask Web Interface
          |
          v
     Python AI Agent
          |
          v
    Ollama / Qwen3
          |
          v
   Python Tool Dispatcher
          |
          v
    LDAP Integration
          |
          v
    Active Directory
     laconia.local
```

The Flask dashboard also performs separate connectivity checks against core domain services.

## Implemented Capabilities

### Active Directory — 12 Capabilities

**Directory queries and account information**

1. List Active Directory users
2. List domain computers
3. Retrieve a user's group memberships
4. List members of an Active Directory group
5. Retrieve user account details
6. Check whether accounts are enabled or disabled
7. Check password expiration status
8. Retrieve password last-changed information
9. Retrieve last logon information
10. Check account lockout status

**Administrative operations**

11. Unlock user accounts
12. Enable or disable user accounts — implemented in code; successful execution pending permissions verification

Administrative actions depend on the permissions delegated to SÝN's service account.

### Web Dashboard and Infrastructure Checks

SÝN includes a custom Flask dashboard providing an interactive AI chat interface and basic domain-service connectivity checks.

| Service | Dashboard Check |
|---|---|
| Domain Controller | ICMP ping |
| DNS | Domain name resolution using `nslookup` |
| LDAP | TCP connectivity on port 389 |
| Kerberos | TCP connectivity on port 88 |
| SMB | TCP connectivity on port 445 |

The dashboard displays the results as service-status indicators. These checks verify basic connectivity and availability, not continuous security monitoring or threat detection.

### AI Integration

- Natural-language interaction using a locally hosted Qwen3 model
- Python-based tool selection and execution
- Flask web interface connected to the AI agent
- LDAP-based Active Directory integration
- Local conversation memory

## Security and Access Control

SÝN uses a dedicated Active Directory service account rather than a domain administrator account for routine directory access.

- LDAP credentials are retrieved using Python `keyring`, rather than hardcoded into the source.
- Selected administrative permissions are delegated within the lab.
- Administrative operations remain subject to Active Directory access controls.
- The Flask interface runs locally.
- Development and testing take place in an isolated virtual lab, not a production environment.

**Current limitations:** The LDAP connection does not yet explicitly enforce TLS, and additional input validation, action confirmation, and audit logging are planned before broader administrative use.

## Project Structure

| File / Module | Purpose |
|---|---|
| `agent.py` | Main AI agent, Ollama integration, and conversation handling |
| `web_agent.py` | Flask dashboard, chat interface, and connectivity checks |
| `active_directory/connection.py` | LDAP connection and credential retrieval |
| `active_directory/dispatcher.py` | Active Directory tool execution |
| `active_directory/tool_definitions.py` | AI-accessible tool definitions |
| `active_directory/users.py` | User queries and account administration |
| `active_directory/groups.py` | Group membership queries |
| `active_directory/computers.py` | Domain computer queries |
| `Static/` | Dashboard images and assets |
| `SYN/` | Launcher, icons, and project documentation |

The modular design supports extending functionality without rebuilding the entire application.

## Development Roadmap

SÝN remains an active development project. Planned enhancements include:

### Active Directory Administration
- Password resets
- User and group creation and management
- Organizational Unit (OU) management
- Expanded domain-controller diagnostics

### Networking and Infrastructure
- DHCP information and diagnostics
- Network and service discovery
- SMB share inspection
- Advanced DNS, LDAP, and Kerberos diagnostics

### Security Operations and SIEM
- Windows Event Log analysis
- Failed-login and suspicious authentication investigations
- Privileged-account monitoring
- Splunk integration and security event correlation
- IOC and threat-intelligence lookups
- Security alerts and incident reports

### Agent Safety and Reliability
- Read-only and administrative operation modes
- Confirmation before sensitive actions
- Audit logging of administrative changes
- Improved permission handling and input validation
- Encrypted LDAP communication
- Investigation history and improved error handling
- Scheduled health checks and notifications

These are planned enhancements, not currently implemented features.

## Learning Objectives

Through SÝN, I am developing practical experience in:

- Python programming and modular application design
- Integrating locally hosted LLMs with infrastructure tools
- Active Directory administration and LDAP
- Authentication, authorization, and delegated permissions
- Web application development with Flask
- Network service connectivity and troubleshooting
- Designing, testing, and securing administrative automation

## Related Project

**[Laconia Cybersecurity Lab](https://github.com/BiancaSe/Laconia-Cybersecurity-Lab)**

SÝN is developed and tested against my VMware-based virtual enterprise network, which includes Windows Server 2019, Active Directory, Windows clients, Linux systems, Kali Linux, Parrot Security OS, and Splunk Enterprise.

The lab provides the infrastructure for testing SÝN's capabilities and developing security operations workflows.

## Project Status

**Active development — 12 Active Directory capabilities implemented in code, with enable/disable operations pending successful verification.**

The Flask dashboard and basic domain-service connectivity checks have been tested in the Laconia environment.

Future development will focus on expanded Active Directory administration, SIEM integration, security investigations, and stronger safeguards for automated operations.
