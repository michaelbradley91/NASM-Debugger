# NASM-Debugger
Learning how to write my own NASM debugger in Python.
I plan to only target an extremely specific architecture at first.

## Requirements
I am using a Docker container during development, so you will need Docker installed.
[Follow the instructions here:](https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/#install-using-the-repository)

```bash
sudo apt-get remove docker docker-engine docker.io
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce
sudo groupadd docker
sudo usermod -aG docker "$USER"
```

This project also uses docker-compose to manage the container, so install that as well
as follows:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo curl -L https://raw.githubusercontent.com/docker/compose/1.24.0/contrib/completion/bash/docker-compose -o /etc/bash_completion.d/docker-compose
```

Then it is probably simplest to restart. You should be able to verify the installations
with the following:
```bash
docker --version
docker-compose --version
```

You must be running X Server in your desktop environment.

You should have `$XAUTHORITY` point to the XAuthority
file for your user as well. (This file essentially grants the application permission to
use X Server.) This was already set for me running a Gnome desktop so check if it is set
already first.

You should ensure `$XDG_RUNTIME_DIR` is set to a directory where temporary user-specific
files can be created.

Finally, you will need to set `$XKB_ROOT` to point to XKB on your file system. Mine
was located at `/usr/share/X11/xkb` so I set it to exactly that path.

You can run the application with:
```bash
docker-compose up
```

Ta da! :-\)

## Recommendations
I am working on the project in PyCharm Professional, so Docker
and Docker-Compose is integrated with the IDE. I also work with these plugins:

* Bash plugin so it is easy to run "sh" files.
* NASM plugin for some syntax highlighting.
* Markdown plugin for this file!

You will need to install the NASM assembler:

```bash
sudo apt update
sudo apt install nasm
```

You will also need GCC version 7+ (older versions may work. You will need the -Og
optimisation flag for the build script).

