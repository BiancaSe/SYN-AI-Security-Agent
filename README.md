# SÝN — AI Security Agent

## Project Overview

** SÝN (named after the Norse goddess of defense and boundary keeper) is a Python-based, locally hosted AI-powered security agent I am developing as part of my [Laconia Cybersecurity Lab](https://github.com).

The project explores how a locally hosted large language model (LLM) can interact with enterprise infrastructure through controlled, purpose-built tools.

SÝN translates natural-language requests into Active Directory queries and administrative operations, combining AI-assisted interaction with Python automation and LDAP.

The goal is to progressively develop SÝN into a security operations assistant capable of supporting identity administration, infrastructure monitoring, security investigations, and incident response within a controlled lab environment.

## Technologies

| Component | Technology |
|---|---|
| Programming language | Python |
| Local AI runtime | Ollama |
| Language model | Qwen3 4B |
| Web interface | Flask |
| Directory communication | LDAP |
| Directory service | Microsoft Active Directory |
| Domain controller | Windows Server 2019 |
| Virtualization | VMware Workstation |
| Development environment | Visual Studio Code |

## Architecture

SÝN operates locally and communicates with the Laconia Active Directory environment through a dedicated LDAP service account.

The application uses modular Python components to interpret requests, select tools, execute directory operations, and present the results.

**Request workflow:**

1. A user submits a natural-language request.
2. The locally hosted AI model interprets the request.
3. The Python application selects an appropriate tool.
4. The tool communicates with Active Directory using LDAP.
5. SÝN processes the returned information and responds to the user.

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

## Implemented Capabilities

SÝN currently supports 11 Active Directory capabilities.

### Active Directory Queries

- List Active Directory users
- List domain computers
- Look up a user's group memberships
- List members of an Active Directory group
- Retrieve user account details
- Check whether user accounts are enabled or disabled
- Check password expiration status
- Retrieve when a password was last changed
- Retrieve last logon information
- Check account lockout status

### Active Directory Administration

- Unlock locked user accounts

### AI and Interface

- Natural-language interaction with a locally hosted AI model
- Python-based tool selection and execution
- Flask web interface
- LDAP communication with the Laconia Active Directory domain

## Security and Access Control

SÝN uses a dedicated Active Directory service account rather than relying on a domain administrator account for routine directory access.

Selected permissions are delegated within the lab environment to support controlled administrative operations.

The project provides hands-on experience with:

- Active Directory permissions and delegation
- LDAP-based identity management
- Service-account design
- AI-assisted infrastructure administration
- Security considerations for automated administrative actions

SÝN is developed and tested in an isolated virtual lab, not a production environment.

## Project Structure

The application is organized into modular Python components.

| File / Module | Purpose |
|---|---|
| `agent.py` | Main agent logic and tool dispatch |
| `web_agent.py` | Flask-based web interface |
| `users.py` | Active Directory user-related functionality |
| `active_directory/tool_definitions.py` | Definitions for Active Directory tools |

The modular design supports adding new capabilities without rebuilding the entire application.

## Development Roadmap

SÝN is an ongoing project with planned expansion across several areas.

### Active Directory Administration
- Reset user passwords
- Enable and disable user accounts
- Create and manage users and groups
- Manage Organizational Units (OUs)
- Inspect domain controller information
- Perform Active Directory health checks

### Networking and Infrastructure
- DNS queries and diagnostics
- DHCP information
- Network and service discovery
- Port and connectivity checks
- SMB share inspection
- Kerberos and LDAP diagnostics

### Security Operations
- Windows Event Log analysis
- Failed login and account lockout investigations
- Suspicious authentication detection
- Privileged-account monitoring
- Vulnerability and configuration assessments
- IOC and threat-intelligence lookups

### Monitoring and SIEM
- Splunk integration
- Automated lab health checks
- Security event correlation
- Alerts and notifications
- Incident and infrastructure reports
- Security dashboards

### Agent Safety and Intelligence
- Read-only and administrative operation modes
- Confirmation before sensitive actions
- Audit logging of administrative changes
- Permission-aware tool execution
- Investigation history
- Improved tool selection and error handling

These are planned features, not currently implemented capabilities.

## Learning Objectives

Through SÝN, I am developing practical experience in:

- Python programming and modular application design
- Working with locally hosted large language models
- Integrating AI with infrastructure management tools
- Active Directory administration and LDAP
- Authentication, authorization, and delegated permissions
- Designing and testing security automation
- Troubleshooting interactions between AI, application logic, and enterprise services

## Related Project

**Laconia Cybersecurity Lab**

SÝN is developed and tested against my VMware-based virtual enterprise network, which includes Windows Server 2019, Active Directory, Windows clients, Linux systems, Kali Linux, Parrot Security OS, and Splunk Enterprise.

The Laconia environment provides the infrastructure for testing SÝN's capabilities and exploring security operations workflows.

## Project Status

**Active development — 11 Active Directory capabilities implemented.**

SÝN is a personal cybersecurity and AI automation project built for hands-on learning, experimentation, and continued development.

Future work will focus on expanding Active Directory administration, integrating security monitoring tools, and implementing additional safeguards for automated actions.
