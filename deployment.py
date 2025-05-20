from pydaffodil import Daffodil
import sys

subcommand = sys.argv[1] if len(sys.argv) > 1 else None

cli = Daffodil(remote_user="root", remote_host="147.93.62.212")

steps = []

if subcommand == "init":
    steps = [
        {"step": "make project folder", "command": lambda: cli.ssh_command("mkdir -p /var/www/project")},
        {"step": "Transfer nginx configuration", "command": lambda: cli.transfer_files("deployment/nginx", destination_path="/etc/nginx/sites-available")},
        {"step": "Create symlink for nginx configuration", "command": lambda: cli.ssh_command("ln -s /etc/nginx/sites-available/project.cloudmateria.com /etc/nginx/sites-enabled/")},
        {"step": "Transfer certbot configuration", "command": lambda: cli.transfer_files("deployment/certbot", destination_path="/root/certbot")},
        {"step": "renew Certbot", "command": lambda: cli.ssh_command("certbot --config /root/certbot/certbot.ini --nginx --cert-name certificate")},
        {"step": "Reload Nginx", "command": lambda: cli.ssh_command("systemctl reload nginx")},
    ]
    cli.deploy(steps)

elif subcommand == "publish":
    steps = [
        {"step": "Build the project", "command": lambda: cli.run_command("npm run build")},
        {"step": "Transfer files to remote server", "command": lambda: cli.transfer_files("build",destination_path="/var/www/project")},
        {"step": "Reload Nginx", "command": lambda: cli.ssh_command("systemctl reload nginx")},
    ]
    cli.deploy(steps)

elif subcommand == "unpublish":
    steps = [
        {"step": "Delete Project", "command": lambda: cli.ssh_command("rm -rf /var/www/project")},
        {"step": "Delete Nginx configuration", "command": lambda: cli.ssh_command("rm -f /etc/nginx/sites-available/project.cloudmateria.com")},
        {"step": "Delete symlink for Nginx configuration", "command": lambda: cli.ssh_command("rm -f /etc/nginx/sites-enabled/project.cloudmateria.com")},
        {"step": "Update Certbot configuration","command": lambda: cli.transfer_files("deployment/certbot", destination_path="/root/certbot")},
        {"step": "Update Certbot", "command": lambda: cli.ssh_command("certbot --config /root/certbot/certbot.ini --nginx --cert-name certificate")},
        {"step": "Reload Nginx", "command": lambda: cli.ssh_command("systemctl reload nginx")},
    ]
    cli.deploy(steps)
else:
    help_text = """
    Usage: python deployment.py [init|publish|unpublish]
    init: Initialize the deployment process.
    publish: Publish the project.
    unpublish: Unpublish the project.
    """

    print(help_text)
    sys.exit(1)