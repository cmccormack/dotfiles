#  ---------------------------------------------------------------------------
#
#  Description:  This file holds all my BASH configurations and aliases
#


#   -------------------------------
#   1.  ENVIRONMENT CONFIGURATION
#   -------------------------------

#   Change Prompt
#   ------------------------------------------------------------
    export PS1="\$(date +%k:%M:%S) (\u)[\w]# "


#   Set Paths
#   ------------------------------------------------------------
    export PATH="$PATH:/usr/local/bin/"


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
    alias py="python3.3"
    alias rm="rm -i"
    alias cp="cp -iv"
    alias mv="mv -iv"
    alias mkdir="mkdir -pv"
    alias less="less -FSRXc"
    alias c="clear"

#   Networking Aliases
    alias myip='curl ip.appspot.com'

#   Programming Aliases
    alias exers='exercism submit'
    alias exerf='exercism fetch'



# Add bash completion for exercism.io
if [ -f ~/.config/exercism/exercism_completion.bash ]; then
    . ~/.config/exercism/exercism_completion.bash
fi

