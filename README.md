Proof of Concept (PoC) for a directory-traversal → memory corruption vulnerability in sudo_logsrvd (Sudo project). This PoC demonstrates how a local, unprivileged user can supply a crafted log_id containing path-traversal sequences that cause sudo_logsrvd to read attacker-controlled files, leading to memory corruption and a crash (local DoS).
Do not run this PoC on production systems.

![sudo_logsrvd_strace](./sudo_logsrvd_strace.png)
