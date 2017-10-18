#!/bin/bash

#  ---------------------------------------------------------------------------
#
#  Description:  This file is loaded when connecting via Interactive Login
#
#  Execution load order:
#   1. /etc/profile
#   2. Executes only first file found from the following:
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

test -f ~/.profile && . ~/.profile
test -f ~/.bashrc && . ~/.bashrc


#   Set Paths
#   ------------------------------------------------------------
    if ! $(echo $PATH | grep -q "/usr/local/bin:"); then
      export PATH="/usr/local/bin:$PATH"
    fi
