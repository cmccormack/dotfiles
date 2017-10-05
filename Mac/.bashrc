#  ---------------------------------------------------------------------------
#
#  Description:  This file holds all my BASH configurations and aliases
#  Mac OS X Directory: ~/Users/[username]/.profile
#
#  Load order for Bash profile on Mac OSX (loads first found):
#   1. ~/.bash_profile
#   2. ~/.bash_login
#   3. ~/.profile


#   -------------------------------
#   1.  ENVIRONMENT CONFIGURATION
#   -------------------------------

    SB_BLUE="\[\033[1;34m\]"
    SB_CYAN="\[\033[0;36m\]"
    SB_YELLOW="\[\033[0;93m\]"
    SB_OFF="\[\033[0m\]"

#   Change Prompt
#   ------------------------------------------------------------
#   export PS1="\$(date +%k:%M:%S) (\u)[\w]# "
    export PS1="\`if [ \$? != 0 ]; then echo ðŸ’¥ ; else echo ðŸº  ; fi\` $SB_YELLOW (\u) $SB_CYAN[\W]# $SB_OFF"


#   Set Paths
#   ------------------------------------------------------------
    export PATH="/usr/local/bin:$PATH"
    export PATH="$PATH:/Library/Frameworks/Python.framework/Versions/Current/bin"


#   Set Default Editor (change 'Nano' to the editor of your choice)
#   ------------------------------------------------------------
    export EDITOR=/usr/bin/nano

#   Set default blocksize for ls, df, du
#   from this: http://hints.macworld.com/comment.php?mode=view&cid=24491
#   ------------------------------------------------------------
    export BLOCKSIZE=1k


#   Add color to terminal
#   (this is all commented out as I use Mac Terminal Profiles)
#   from http://osxdaily.com/2012/02/21/add-color-to-the-terminal-in-mac-os-x/
#   ------------------------------------------------------------
    export CLICOLOR=1
    export LSCOLORS=GxFxCxDxBxegedabagaced



#   Set aliases
#   ------------------------------------------------------------
    
#   General Aliases
    alias grep='grep --color=auto'
    alias ls="ls --color=auto"
    alias ll="ls -lahF"
    alias la="ls -lahF"
    alias l="ls -lhF"
    alias py="python3.3"
    alias rm="rm -i"
    alias cp="cp -iv"
    alias mv="mv -iv"
    alias mkdir="mkdir -pv"
    alias less="less -FSRXc"
    alias c="clear"
    
#   Mac Hidden Files
    function showFiles()
    {
        defaults write com.apple.finder AppleShowAllFiles YES
        killall Finder /System/Library/CoreServices/Finder.app
        echo 'Hidden files now visible'
    }

    function hideFiles()
    {
        defaults write com.apple.finder AppleShowAllFiles NO
        killall Finder /System/Library/CoreServices/Finder.app
        echo 'Hidden files not invisible'
    }


#   Networking Aliases
    alias myip='curl ip.appspot.com'


# Activation bash completion
    if [ -f $(brew --prefix)/etc/bash_completion ]; then
        source $(brew --prefix)/etc/bash_completion
    fi


# Add bash completion for git
    source ~/.git-completion.bash

# Backup .profile to Dropbox
    cp ~/.profile ~/Dropbox/Hobbies/Mac/_.profile

