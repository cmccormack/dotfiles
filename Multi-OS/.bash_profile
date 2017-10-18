#!/bin/bash

#  ---------------------------------------------------------------------------
#
#  Description:  This file is loaded when connecting via Interactive Login session
#
#  Execution load order:
#   1. /etc/profile
#   2. Execute only first file found from the following files:
#     2A. ~/.bash_profile
#     2B. ~/.bash_login
#     2C. ~/.profile
#   3. ~/.bash_logout
#
#   Caveat: Mac OSX treats every new terminal session as an Interactive Login
#
#   Credit to the following resources:
#     http://www.solipsys.co.uk/new/BashInitialisationFiles.html
#     https://shreevatsa.wordpress.com/2008/03/30/zshbash-startup-files-loading-order-bashrc-zshrc-etc/


#   Source Configuration Files
#   ------------------------------------------------------------

#   Load .bashrc from home directory.
#   BASH does NOT execute .bashrc when connecting via Interactive Login, but does execute
#       on Interactive Non-Login shell launch (eg. `$ bash`)
test -f ~/.bashrc && . ~/.bashrc

#   Load .profile from home directory.
#   This file will load automatically if ~/.bash_profile or ~/.bash_login don't exist
#   Disable unless required
# test -f ~/.profile && . ~/.profile



#   Set Paths
#   ------------------------------------------------------------

function add_path() {
    if [ ! $(echo "$PATH" | tr ":" "\n" | grep -c "^$1/*$") -gt 0 ]; then 
        export PATH="$1:$PATH"
    fi
}
    add_path "/usr/local/bin"
    
    #if ! $(echo $PATH | grep -q "/usr/local/bin:"); then
    #  export PATH="/usr/local/bin:$PATH"
    #fi
