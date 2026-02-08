---
name: SecurityHardening
description: Linux security logic, SSH hardening, and permission auditing.
triggers: [ssh, firewall, ufw, iptables, permissions, audit, secure, hardening, fail2ban]
---
# ASSERTIVE CONTEXT: SECURITY & HARDENING
- **SSH Protocol:** Advise disabling root login and password authentication in `/etc/ssh/sshd_config`. 
- **Permissions:** Use octal notation for `chmod` (e.g., `644`) for clarity. Recommend `find /path -type d -exec chmod 755 {} +` for batch directory updates.
- **Firewall:** Prioritize `ufw` for simplicity on Ubuntu/Debian and `firewalld` for RHEL-based systems. Always suggest "default deny" incoming policies.
- **Visibility:** Suggest checking `/var/log/auth.log` or `lastlog` to audit recent access attempts.