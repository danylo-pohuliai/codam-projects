*This project has been created as part of the 42 curriculum by dpohulia.*

# Born2beRoot

## Description
Born2beRoot is a system administration project that introduces the fundamental concepts of virtualization, server configuration, and security. The goal of this project is to set up a complete, secure server environment inside a virtual machine without using a graphical user interface (GUI).

This project involves configuring a strict security architecture, including encrypted disk partitions using LVM, mandatory access control (AppArmor), advanced firewall rules (UFW), enforced password policies via PAM, and highly restricted `sudo` privileges. Additionally, it features an automated bash script that broadcasts system monitoring statistics to all terminals at regular intervals.

## Instructions

To evaluate or run the project, you need to verify the virtual machine's integrity and connect to it using the specific forwarded port.

**1. Create/Verify the Virtual Machine Signature**

To ensure the machine has not been modified, generate the SHA1 checksum of the virtual disk and save it to the signature file:
```bash
sha1sum Danylo.vdi > signature.txt
```

**2. Connect using SSH**

Once the machine is running and the disk is decrypted, connect to it from your host machine via SSH using the forwarded port:

```bash
ssh dpohulia@localhost -p 4241
```

---

### Users and Groups Management

To check the existing users and groups on the server, you can use the following commands:

* **List all users:** `cat /etc/passwd | cut -d: -f1`
* **List all groups:** `cat /etc/group | cut -d: -f1`
* **List of users in group:** `getent group <group_name>`
* **Create new group:** `sudo addgroup <group_name>`
* **Add a user to a group:** `sudo adduser <username> <group_name>`

### Hostname

To check the hostname use following commands:
`hostname` - shows current hostname
`sudo /etc/hostname` and `sudo /etc/hosts` to change the hostname
`sudo reboot` - to apply changes


### SSH Configuration

The SSH service is configured to run on a custom port and deny root login.

* **Check SSH status:**
```bash
sudo service ssh status
```


* **Configuration files location:**
* Server configuration: `/etc/ssh/sshd_config`
* Client configuration: `/etc/ssh/ssh_config`


### UFW (Uncomplicated Firewall)

The firewall is strictly configured to allow only necessary traffic. By default, UFW drops all incoming connections unless a specific port is explicitly opened.

* **Check firewall status and active rules:**
```bash
sudo ufw status
```
(You will only see ports 4242 for SSH and 80 for HTTP. All other ports, including the default SSH port 22, are implicitly blocked by the default deny policy).

* **Basic UFW commands:**
* Allow a specific port (e.g., for SSH): `sudo ufw allow 4242`
* Deny a specific port: `sudo ufw deny 8080`
* Deny all traffic from a specific IP address for specific port: `sudo ufw deny from 192.168.1.100 to any port 4242`
* Allow traffic only from a specific IP address: `sudo ufw allow from 192.168.1.50`
* Delete an existing rule: `sudo ufw delete allow 22`

### SUDO POLICY
The configuration is stored in `/etc/sudoers.d/sudo_config` and contains the following rules:

```ini
Defaults  passwd_tries=3
Defaults  badpass_message="Better luck next time :):(:())"
Defaults  logfile="/var/log/sudo/sudo_config"
Defaults  log_input, log_output
Defaults  iolog_dir="/var/log/sudo"
Defaults  requiretty
Defaults  secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```

**Explanation of the rules:**

* `passwd_tries=3`: Limits the user to a maximum of 3 password attempts when using `sudo`.
* `badpass_message`: Displays a custom error message if the wrong password is provided.
* `logfile`: Specifies the exact file where `sudo` usage logs will be saved.
* `log_input, log_output` & `iolog_dir`: Archives all inputs and outputs of commands executed via `sudo` into the specified directory.
* `requiretty`: Forces `sudo` to only run from a real TTY session (prevents executing `sudo` via automated scripts in the background without a terminal).
* `secure_path`: Restricts the directories where `sudo` will look for commands, preventing the execution of malicious scripts from untrusted locations.

---

### Password Quality & Expiration Policies
Strict password policies are enforced across the system using two main configurations.

**1. Password Expiration (`/etc/login.defs`)**
The maximum password age is set to 30 days, the minimum allowed time between changes is 2 days, and the user receives a warning 7 days before expiration.

**2. Password Complexity (`/etc/pam.d/common-password`)**
The `libpam-pwquality` module is installed to enforce strict complexity rules. The following line was added to the configuration:
`retry=3 minlen=10 ucredit=-1 dcredit=-1 lcredit=-1 maxrepeat=3 reject_username difok=7 enforce_for_root`

**Explanation of the PAM rules:**
* `retry=3`: Gives the user 3 attempts to enter a valid password that meets all requirements before aborting the command.
* `minlen=10`: The password must be at least 10 characters long.
* `ucredit=-1`: Must contain at least one **U**ppercase letter (negative value means strictly required).
* `dcredit=-1`: Must contain at least one **D**igit.
* `lcredit=-1`: Must contain at least one **L**owercase letter.
* `maxrepeat=3`: Cannot contain more than 3 consecutive identical characters (e.g., `1111` is blocked).
* `reject_username`: The password cannot contain the user's name in forward or reverse format.
* `difok=7`: At least 7 characters must be different from the previous password.
* `enforce_for_root`: Ensures that even the root user must obey these complexity rules.

To check this rules use `passwd`

### Monitoring Script & Cron
A bash script (`monitoring.sh`) was created to collect and display vital system information (CPU/RAM usage, active connections, disk space, etc.) to all logged-in users via the `wall` command.

**Execution:**
The script can be executed directly through the bash interpreter:
```bash
sudo bash /home/dpohulia/monitoring.sh
```

Alternatively, because the script includes the `#!/bin/bash` shebang at the top, it can be executed as a standalone binary (provided it has execution rights via `chmod +x`):

```bash
sudo ./monitoring.sh
```

To achieve an optimized, fast, and resource-efficient execution, the script relies on the following core Linux tools:

* **`awk`**: A powerful text-processing language used extensively in this script to extract specific columns, filter data, and perform mathematical calculations (like percentages) on the fly without spawning additional subshells.
  * *Example:* `awk '/Mem:/ {print $2}'` finds the line containing "Mem:" and prints its 2nd column.
* **`grep`**: A command-line utility for searching plain-text data sets for lines that match a regular expression.
  * *Script Context:* `grep -c` is used to instantly count matching lines (eliminating the need for `wc -l`), and `grep -q` is used for a silent boolean check to verify if LVM exists.
* **`read`**: A bash built-in command that reads a line from standard input and splits it into multiple variables.
  * *Script Context:* `read total used percent <<< $(...)` allows the script to fetch and assign three different values from a single `df` or `free` execution, preventing redundant system calls.
* **`free`**: Displays the total amount of free, used, and swap memory in the system.
  * *Example:* `free --mega` outputs the memory statistics in megabytes for easier mathematical processing.
* **`df`**: Reports file system disk space usage.
  * *Script Context:* `df -m` outputs data in megabytes. The script filters out virtual file systems and the `/boot` partition to calculate the real storage space of the server.
* **`lsblk`**: Lists information about block devices in a tree-like format. It is used in the script to easily parse and verify if the storage relies on Logical Volume Management (`lvm`).
* **`ss`**: A utility used to investigate network sockets (a modern and faster replacement for `netstat`).
  * *Example:* `ss -ta` lists all active TCP connections, allowing the script to count the `ESTAB` (established) ones.
* **`vmstat`**: Reports virtual memory and processor statistics.
  * *Script Context:* `vmstat 1 2` takes two system snapshots one second apart to get an accurate reading of the current idle CPU percentage, which is then subtracted from 100 to determine the active CPU load.

**Automation via Cron (`crontab`):**
Cron is background service (daemon) that automatically executes scheduled tasks at specified times or intervals.
Crontab is a configuration file and command used to define and manage scheduled tasks (cron jobs) for users.
To automate the execution as required by the subject, the script is scheduled using the root user's cron daemon.

* To edit the crontab: `sudo crontab -u root -e`
* The following rules are applied:

```bash
*/10 * * * * bash /home/dpohulia/monitoring.sh
@reboot sleep 40 && bash /home/dpohulia/monitoring.sh
```

**Explanation of the rules:**

* `*/10`: Executes the script precisely every 10 minutes (e.g., at 12:00, 12:10, 12:20).
* `@reboot sleep 40`: Executes the script at server startup. The `sleep 40` command introduces a necessary 40-second delay to ensure all system services (like networking and SSH) are fully initialized before the script gathers data and sends the broadcast message.
---

## Bonus Part: WordPress Deployment & Advanced Security

The bonus part of this project involves setting up a functional WordPress website using a lightweight, high-performance web stack (LLMP: Lighttpd, MariaDB, PHP) and protecting the infrastructure with an automated intrusion prevention service (`fail2ban`).

### 1. Web Server Configuration (`lighttpd`)
Instead of heavy web servers like Apache, **lighttpd** was selected for its minimal memory footprint, low CPU load, and speed.

* **Installation:**
```bash
  sudo apt install lighttpd
```


* **Verification:**

```bash
sudo systemctl status lighttpd
```


`systemctl` is a central tool for controlling the `systemd` system and service manager. The `status` command allows the administrator to verify if the web server is running actively, check its uptime, and view recent runtime logs to ensure there are no configuration errors.

### 2. Database Management (`MariaDB`)

WordPress requires a relational database to store its content, user data, and system settings.

* **Installation & Securing:**
```bash
sudo apt install mariadb-server
sudo mariadb-secure-installation
```


* **Database Initialization:**
After securing the environment, a dedicated database, a secure user account, and strict access privileges were established via the MariaDB console:
```sql
CREATE DATABASE wp_db;
CREATE USER 'dpohulia'@'localhost' IDENTIFIED BY '12345678';
GRANT ALL PRIVILEGES ON wp_db.* TO 'dpohulia'@'localhost';
FLUSH PRIVILEGES;
exit
```

### 3. PHP Environment & WordPress Installation

WordPress is built on PHP, requiring specific processing modules to interact with the web server and database.

* **Prerequisites & Download:**
First, pre-requisite utilities (`wget` for downloading and `zip` for archive extraction) were installed. Then, the official English version of WordPress was pulled directly from the source:
```bash
sudo apt install wget zip php-cgi php-mysql
cd /var/www
sudo wget [https://wordpress.org/latest.zip](https://wordpress.org/latest.zip)
sudo unzip latest.zip
```


* **Configuration (`wp-config.php`):**
The configuration file was created and modified using `nano` to link WordPress with the MariaDB instance:
```bash
sudo cp /var/www/wordpress/wp-config-sample.php /var/www/wordpress/wp-config.php
sudo nano /var/www/wordpress/wp-config.php
```


*(Inside the file, the exact values for `DB_NAME`, `DB_USER`, and `DB_PASSWORD` created in step 2 were specified).*
* **Final Setup:**
With port forwarding correctly configured in VirtualBox, the installation wizard was accessed from the host machine's web browser at `http://localhost:8080`. After completing the interactive setup form, the fully operational WordPress site became dynamically accessible at this address.

### 4. Intrusion Prevention (`fail2ban`)

To proactively defend the custom SSH port from automated dictionary attacks and brute-force attempts, `fail2ban` was integrated into the system.

* **Installation:**
```bash
sudo apt install fail2ban
```


* **Local Jail Configuration (`/etc/fail2ban/jail.local`):**
To ensure settings are persistent and do not get overwritten during system updates, a custom configurations file was populated with strict rules targeting the non-standard SSH port:
```ini
[DEFAULT]
bantime  = 10m
findtime = 10m
maxretry = 2

[sshd]
enabled = true
port    = 4242
filter  = sshd
logpath = /var/log/auth.log
```

To apply changes:
```bash
sudo fail2ban-client reload
```

* **Verification & Management:**
To monitor the application state and track malicious connection bans during evaluation, the following administration commands are used:
* **Check overall service status:** `sudo fail2ban-client status`
* **View detailed SSH jail statistics & banned IPs:** `sudo fail2ban-client status sshd`


## Project Description

### Choice of Operating System

For this project, **Debian** was chosen over Rocky Linux.

* **Pros:** Debian is renowned for its exceptional stability, huge community support, and the highly intuitive `apt` package manager. It is considered one of the best distributions for learning foundational system administration.
* **Cons:** Packages in Debian's stable branch can be older compared to bleeding-edge distributions.

### Main Design Choices

* **Partitioning:** The disk is partitioned using LVM (Logical Volume Manager) over an encrypted LUKS container. This allows for flexible resizing of logical volumes (e.g., `/home`, `/var`, `/tmp`) while ensuring data remains completely inaccessible if the physical disk is compromised.
* **Security Policies:** Passwords expire every 30 days and require a minimum length of 10 characters, including uppercase, lowercase, and numeric characters, enforced by `libpam-pwquality`.
* The `fail2ban` service is implemented to protect the SSH port against brute-force attacks.
* **User Management:** Root login via SSH is strictly forbidden. A standard user (`dpohulia`) is created and added to the `user42` and `sudo` groups.
* **Services Installed:** Core: `sshd` (custom port 4242), `ufw` (firewall), `cron` (for the monitoring script).
* **Session Utilities:** `ls /usr/bin/*session` lists executables in `/usr/bin` whose names end with session. On this system, it returns only `dbus-run-session`, a utility that starts a temporary D-Bus session and runs a command within it. This indicates that no graphical desktop session manager (such as `gnome-session`, `xfce4-session`, or `lxsession`) is installed.
* Bonus Stack: `lighttpd`, `MariaDB`, `PHP`, and a fully functional `WordPress` site, monitored by `fail2ban`.



### Technical Comparisons

* **Debian vs Rocky Linux:** Debian is a community-driven distribution that uses `.deb` packages and the `apt` package manager. Rocky Linux is a downstream, enterprise-ready rebuild of RHEL (Red Hat Enterprise Linux) that uses `.rpm` packages and `dnf`. Debian is generally more beginner-friendly, while Rocky targets enterprise server environments.
* **aptitude vs apt:** `apt` is the default package manager on Debian-based systems, used to install, update, and remove software. `aptitude` is an alternative frontend that provides an interactive interface and more advanced dependency resolution, often suggesting multiple solutions when package conflicts occur.
* **AppArmor vs SELinux:** Both provide Mandatory Access Control (MAC). AppArmor (default on Debian) uses file paths to restrict programs based on predefined profiles, making it relatively easy to configure. SELinux (default on Rocky) works by labeling files, processes, and ports with security contexts, offering deeper control but with a much steeper learning curve.
* **UFW vs firewalld:** UFW (Uncomplicated Firewall) is a straightforward interface for managing `iptables` and is widely used in Debian/Ubuntu. `firewalld` is the dynamic firewall manager used in Rocky/RHEL, which relies on "zones" to manage trust levels of network connections.
* **VirtualBox vs UTM:** VirtualBox is a Type 2 hypervisor primarily used for x86/amd64 architectures, offering great compatibility across Windows and Linux hosts. UTM is a frontend for QEMU, specifically optimized for macOS and Apple Silicon (M1/M2/M3), capable of both virtualization and hardware emulation.

## Resources

* [Debian Official Documentation](https://www.debian.org/doc/)
* [LVM Administrator's Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_logical_volumes/index)
* [UFW Essentials](https://help.ubuntu.com/community/UFW)

### AI Usage Description
AI was used as an educational tutor to study the theoretical concepts of system administration, rather than generating direct solutions. Specifically, it helped with:
* **System Logic Analysis:** Breaking down the exact timing execution of `cron` jobs (the necessity of `sleep` with `@reboot` to prevent race conditions).
* **Security Synergy:** Analyzing the concept of "Defense in Depth" to understand how PAM (`pwquality`) and `fail2ban` complement each other on different layers of server security.
* **Learning theory:** :)