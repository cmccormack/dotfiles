#  ---------------------------------------------------------------------------
#
#  Description:  This file holds all my BASH configurations and aliases
#  Mac OS X Directory: ~/Users/[username]/.profile
#


#   -------------------------------
#   1.  ENVIRONMENT CONFIGURATION
#   -------------------------------

#   Change Prompt
#   ------------------------------------------------------------
    export PS1="\$(date +%k:%M:%S) (\u)[\w]# "


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
    #export LSCOLORS=ExFxBxDxCxegedabagacad
    export LSCOLORS=GxFxCxDxBxegedabagaced



#   Set aliases
#   ------------------------------------------------------------
    
#   General Aliases
    alias ll="ls -l"
    alias py27="python2.7"
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

#   Programming Aliases
    alias exers='exercism submit'
    alias exerf='exercism fetch'

# Activation bash completion
if [ -f $(brew --prefix)/etc/bash_completion ]; then
    source $(brew --prefix)/etc/bash_completion
fi

# Add bash completion for exercism.io
if [ -f ~/.config/exercism/exercism_completion.bash ]; then
    . ~/.config/exercism/exercism_completion.bash
fi

# Backup .profile to Dropbox
cp ~/.profile ~/Dropbox/Hobbies/Mac/_.profile
