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

    SB_BOLD="\[\e[1m\]"
    SB_RED="\[\e[31m\]"
    SB_DIM="\[\e[2m\]"
    SB_MAGENTA="\[\e[35m\]"
    SB_BLUE="\[\e[1;34m\]"
    SB_CYAN="\[\e[0;36m\]"
    SB_LIGHTCYAN="\[\e[96m\]"
    SB_YELLOW="\[\e[0;93m\]"
    SB_OFF="\[\e[0m\]"
    SB_GREEN="\[\e[32m\]"
    SB_LIGHTGREEN="\[\e[92m\]"

#   Change Prompt
#   ------------------------------------------------------------
    # Use if terminal has full unicode support
    export PS1="\n┌─ \`if [ \$? != 0 ]; then echo 💥 ; else echo 🍺  ; fi\`  $SB_YELLOW($SB_BOLD\u$SB_OFF@$SB_YELLOW\h) $SB_LIGHTGREEN\t $SB_LIGHTCYAN[\W] $SB_OFF\n└────► # "
    # Use if terminal supports special characters
    # export PS1="\n┌─\`if [ \$? != 0 ]; then echo $SB_RED✸ ; else echo $SB_LIGHTGREEN✔  ; fi\` $SB_YELLOW($SB_BOLD\u$SB_OFF@$SB_YELLOW\h) $SB_LIGHTGREEN\t $SB_LIGHTCYAN[\W] $SB_OFF\n└────► # "
    # Use if terminal does not support special characters (eg. Windows CMD)
    # export PS1="\n┌─ \`if [ \$? != 0 ]; then echo $SB_RED X ; else echo $SB_LIGHTGREEN O  ; fi\`  $SB_YELLOW$SB_BOLD(\u$SB_OFF@$SB_YELLOW\h) $SB_LIGHTGREEN\t $SB_LIGHTCYAN[\W] $SB_OFF\n└────> # "



#   Set Default Editor (change 'Nano' to the editor of your choice)
#   ------------------------------------------------------------
    export EDITOR=/usr/bin/nano

#   Set default blocksize for ls, df, du
#   from this: http://hints.macworld.com/comment.php?mode=view&cid=24491
#   ------------------------------------------------------------
    export BLOCKSIZE=1k


#   Set aliases
#   ------------------------------------------------------------
    
#   General Aliases
    alias grep='grep --color=auto'
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


#   Networking Aliases
    alias myip='curl ip.appspot.com'
    


#   Add bash completion for git if exists
    if [ -f ~/.git-completion.bash ]; then
        source ~/.git-completion.bash
    else
        echo ".git-completion.bash file not found"
    fi
    
    
#   Helper Functions
#   ------------------------------------------------------------

    command_exists () { hash "$1" > /dev/null 2>&1; }
    os_version () { echo $(uname -s); }
    

#   Mac OSX-only Commands
    if [ $(os_version) == "Darwin" ]; then
    
#       Mac Hidden Files
        function showFiles() {
            defaults write com.apple.finder AppleShowAllFiles YES
            killall Finder /System/Library/CoreServices/Finder.app
            echo 'Hidden files now visible'
        }
        function hideFiles() {
            defaults write com.apple.finder AppleShowAllFiles NO
            killall Finder /System/Library/CoreServices/Finder.app
            echo 'Hidden files now invisible'
        }
        
#       Activate bash completion
        if ! command_exists brew; then
            echo "bash-completion not available (try 'brew install bash-completion' first)"
        elif ! [ -f $(brew --prefix)/etc/bash_completion ]; then
            echo "$(brew --prefix)/etc/bash_completion missing."
        else 
            source $(brew --prefix)/etc/bash_completion
        fi
        echo "Mac Commands Loaded"
    fi


