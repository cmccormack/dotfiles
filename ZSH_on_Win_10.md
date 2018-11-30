### Install Windows Subsystem for Linux

> [Inspired by evdokimovm.github.io](https://evdokimovm.github.io/windows/zsh/shell/syntax/highlighting/ohmyzsh/hyper/terminal/2017/02/24/how-to-install-zsh-and-oh-my-zsh-on-windows-10.html)

1. Install Windows Subsystem for Linux.
    * Go to `Settings -> Update and Security -> For developers` and change `Sideload apps` setting to `Developer mode`

2. Enable Windows Subsystem for Linux (Beta)
    * Open `command prompt` and type `OptionalFeatures.exe` and enable `Windows Subsystem for Linux (Beta)` then reboot your PC. After rebooting you need to open command prompt and use `bash` command. Then begin automatic downloading and installation of Linux Subsystem.
    * Up-to-date instructions can be found [here](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

3. Install Hyper Terminal Server
    * Go to official [hyper terminal website](https://hyper.is/) and download latest version of terminal for Windows.

4. (Optional) Install Node.js
    * Go to offical [node.js website](https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions-enterprise-linux-fedora-and-snap-packages) for the latest instructions.
    * At the time of writing, the instructions were as follows:
    ```sh
    curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash -
    sudo apt-get install -y nodejs
    ```
    * Validate proper installation:
    ```sh
    $ which npm
    /usr/bin/npm
    ```
    * May require session reload for changes to take effect.

5. Install git
    * Go to official [git-scm.com website](https://git-scm.com/download/linux) for the latest instructions.
    * Installation using apt-get:
    ```sh
    sudo apt-get install git -y
    ```

6. Install ZSH
    * Installation using apt-get:
    ```sh
    sudo apt-get install zsh
    ```
    * Enter shell: `$ bash-c zsh`
    * Go through setup wizard to customize the shell.
        * To run through the setup again later you can run the zsh-newuser-install:
        ```sh
        autoload -U zsh-newuser-install
        zsh-newuser-install -f
        ```

7. Install oh-my-zsh
    * Go to official [oh-my-zsh repo](https://github.com/robbyrussell/oh-my-zsh) for the latest instructions.
    * Installation using curl:
    ```sh
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
    ```

8. (Optional) Change theme
    * Themes can be found in `~/.oh-my-zsh/themes`.
        * Use only the first part of the name (eg. `~/.oh-my-zsh/themes/agnoster.zsh-theme` > `agnoster`)
    * Edit the THEME variable in `~/.zshrc`:
        ```zsh
        nano ~/.zshrc
        ```
        ```zsh
                    GNU nano 2.2.6          File: ~/.zshrc
        ...
        # Set name of the theme to load. Optionally, if you set this to "random"
        # it'll load a random theme each time that oh-my-zsh is loaded.
        # See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
        # ZSH_THEME="robbyrussell"
        ZSH_THEME="agnoster"
        ...
        ```
        Exit nano `[ctrl+x]`

9. (Optional) Install Powerline Fonts for themes that use them (eg. agnoster, ...)
    * Go to official [Powerline Fonts repo](https://github.com/powerline/fonts) for the latest instructions.
    * For Windows, I just downloaded the fonts I preferred and installed manually:
        * Download and install `Ubuntu Mono derivative Powerline.ttf` from `powerline/fonts`
        * Verify the actual font name in `C:\Windows\Fonts`
        * Update `.hyper.js` configuration to use font:
            * `[ctrl+,]` or `[≡] > Edit > Preferences...`
            ```js
            fontFamily: 'Ubuntu Mono derivative Powerline Regular, Menlo, [...]'
            ```
