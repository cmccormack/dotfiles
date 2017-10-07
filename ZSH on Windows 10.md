### Install Windows Subsystem for Linux

> [Source - evdokimovm.github.io](https://evdokimovm.github.io/windows/zsh/shell/syntax/highlighting/ohmyzsh/hyper/terminal/2017/02/24/how-to-install-zsh-and-oh-my-zsh-on-windows-10.html)

1. Install Windows Subsystem for Linux.
    * Go to `Settings -> Update and Security -> For developers` and change `Sideload apps` setting to `Developer mode`

2. Enable Windows Subsystem for Linux (Beta)
    * Open `command prompt` and type `OptionalFeatures.exe` and enable `Windows Subsystem for Linux (Beta)` then reboot your PC. After rebooting you need to open command prompt and use `bash` command. Then begin automatic downloading and installation of Linux Subsystem.

3. Install Hyper Terminal Server
    * Go to official [hyper terminal website](https://hyper.is/) and download latest version of terminal for Windows.

4. (Optional) Install Node.js
    * Go to offical [node.js website](https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions) for the latest instructions.
    * At the time of writing, the instructions were as follows:
    ```sh
    $ curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
    $ sudo apt-get install -y nodejs
    ```
    * Validate proper installation:
    ```sh
    $ which npm
    /usr/bin/npm
    ```
    * May require session reload for changes to take effect.

5. Install git
    * Go to official [git-scm.com website](https://git-scm.com/book/id/v2/Getting-Started-Installing-Git) for the latest instructions.
    * Installation using apt-get:
    ```
    $ sudo apt-get install git -y
    ```

6. Install ZSH
    * Installation using apt-get:
    ```
    $ sudo apt-get install zsh
    ```