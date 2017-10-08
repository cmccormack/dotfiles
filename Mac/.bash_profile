#   Source Configuration Files
#   ------------------------------------------------------------
test -f ~/.profile && . ~/.profile
test -f ~/.bashrc && . ~/.bashrc


#   Set Paths
#   ------------------------------------------------------------
    if ! $(echo $PATH | grep -q "/usr/local/bin:"); then
      export PATH="/usr/local/bin:$PATH"
    fi