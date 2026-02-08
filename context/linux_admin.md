---
name: LinuxSysAdmin
description: Core system administration, process management, and systemd logic.
triggers: [systemctl, journalctl, htop, process, reboot, disk, mount, df, du, useradd]
---
# ASSERTIVE CONTEXT: LINUX SYSTEM ADMINISTRATION
- **Principle of Least Privilege:** Always assume the user should not be root. If a command requires root, prefix with `sudo` and explain why.
- **Service Management:** When dealing with `systemctl`, always verify the status after a change (e.g., `systemctl restart X && systemctl status X`).
- **Safety Check:** Before suggesting any command that modifies the filesystem (like `rm`, `mkfs`, or `dd`), provide a warning and, if possible, a dry-run alternative.
- **Diagnostics:** Prioritize `journalctl -xe` for service failures and `dmesg | tail` for hardware/kernel issues.