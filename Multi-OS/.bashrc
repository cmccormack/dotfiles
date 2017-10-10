#!/bin/bash

#  ---------------------------------------------------------------------------
#
#  Description:  This file holds all my BASH configurations and aliases
#
#  Load order for Bash profile (loads first found):
#   1. ~/.bash_profile
#   2. ~/.bash_login
#   3. ~/.profile


#   Load alternate shell
#   -------------------------------
#   bash -c zsh

#   -------------------------------
#   1.  ENVIRONMENT CONFIGURATION
#   -------------------------------

#   Set Text Formatting
    BOLD="\[\e[1m\]"
#   Set Text Foreground Colors
    RED="\[\e[31m\]"
    L_RED="\[\e[91m\]"
    DIM="\[\e[2m\]"
    BLUE="\[\e[34m\]"
    MAGENTA="\[\e[35m\]"
    CYAN="\[\e[36m\]"
    L_CYAN="\[\e[96m\]"
    YELLOW="\[\e[33m\]"
    L_YELLOW="\[\e[93m\]"
    ORANGE="\[\e[38;5;215m\]"
    L_GREEN="\[\e[92m\]"
    GREEN="\[\e[32m\]"
    L_GRAY="\[\e[37m\]"
    D_GRAY="\[\e[90m\]"
    WHITE="\[\e[97m\]"
#   Disable Colors
    Rcol="\[\e[0m\]"

#   Prompt
#   ------------------------------------------------------------

#   ASCII Symbols │ ┤ ├ ┘ ┌ ┐

#   Prompt Variables
    PROMPT_COMMAND=__prompt_command
    
    function __prompt_command() {
      local EXIT="$?"
      
#     Return Status Badges
      local ENABLE_EMOJI=false
      local SUCCESS_BADGE="${L_GREEN}✔${Rcol} "
      local EMOJI_SUCCESS_BADGE="🍺  "
      local FAIL_BADGE="${L_RED}✸${Rcol} "
      local EMOJI_FAIL_BADGE="💥  "

      local User="${BOLD}${L_GREEN}\u${Rcol}"
      local Host="${L_GREEN}\h${Rcol}"
      local Time="${ORANGE}\t${Rcol}"
      local Path="${YELLOW}\W${Rcol}"

#     Use Emojis if Enabled
      if $ENABLE_EMOJI; then
        SUCCESS_BADGE=$EMOJI_SUCCESS_BADGE
        FAIL_BADGE=$EMOJI_FAIL_BADGE
      fi
      local BADGE=$([ ${EXIT} != 0 ] && echo ${FAIL_BADGE} || echo ${SUCCESS_BADGE})

#     Git Integration
      local Git_Branch=`my_git_branch`
      local Git_Status=`my_git_status`
      local Mod=$(echo ${Git_Status} | tr ':' '\n' | grep -c "M")
      if [ "${Mod}" -gt 0 ]; then Mod="${YELLOW}●${Rcol}"; else Mod="${L_GREEN}●${Rcol}"; fi

#     Build PS1 String
      # PS1="\n"
      # PS1+="${WHITE}┌─${Rcol} ${BADGE}  ${User}@${Host} ${Time} ${WHITE}[${Rcol}${Path}${WHITE}]${Rcol}"
      # if [ ! "${Git_Branch}" == "" ]; then 
      #   Git_Branch="${L_CYAN}${Git_Branch}${Rcol}"
      #   PS1+=" (${Git_Branch} ${Mod})"; fi
      # PS1+="\n${WHITE}└─► ${Rcol}# "


      Verbose_Theme="\n${WHITE}┌─${Rcol} ${BADGE}  ${User}@${Host} ${Time} ${WHITE}[${Rcol}${Path}${WHITE}]${Rcol}"
      if [ ! "${Git_Branch}" == "" ]; then 
        Git_Branch="${L_CYAN}${Git_Branch}${Rcol}"; Verbose_Theme+=" (${Git_Branch} ${Mod})"; fi
      Verbose_Theme+="\n${WHITE}└─► ${Rcol}# "

      Simpler_Theme="\n${YELLOW}\w${Rcol}"
      if [ ! "${Git_Branch}" == "" ]; then 
        Git_Branch="${L_CYAN}${Git_Branch}${Rcol}"; Simpler_Theme+=" [${Git_Branch}${Mod}]"; fi
      Simpler_Theme+="\n ${BOLD}$([ ${EXIT} != 0 ] && echo ${L_RED}\$${Rcol} || echo ${L_GREEN}\$${Rcol})${Rcol} "

      Theme=$Simpler_Theme

      PS1=$Theme
    }

    

#   Set Default Editor (change 'Nano' to the editor of your choice)
#   ------------------------------------------------------------
    export EDITOR=/usr/bin/nano

#   Set default blocksize for ls, df, du
#   from this: http://hints.macworld.com/comment.php?mode=view&cid=24491
#   ------------------------------------------------------------
    export BLOCKSIZE=1k



#   Set aliases
#   ------------------------------------------------------------
    

#   Enable color support for commands if supported
    if [ -x /usr/bin/dircolors ]; then
        alias ls='ls --color=auto'
        alias grep='grep --color=auto'
        alias fgrep='fgrep --color=auto'
        alias egrep='egrep --color=auto'
    fi

#   General Aliases
    alias l="ls -CF"
    alias ll="ls -lhF"
    alias la="ls -lAhF"
    alias py="python3.3"
    alias rm="rm -i"
    alias cp="cp -iv"
    alias mv="mv -iv"
    alias mkdir="mkdir -pv"
    alias less="less -FSRXc"
    alias c="clear"
    alias please='sudo "$BASH" -c "$(history -p !!)"' ## Runs previous command as sudo

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
    color() { echo "$1$2${Rcol}"; }



    function my_git_branch(){
      echo `git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'`
    }

    function my_git_status(){
      # Get status and branch and replace newline (\n) with colon (:)
      local Status="$(git status --porcelain 2>/dev/null | tr '\n' ':')"
      echo ${Status}
    }




#   Mac OSX-only Commands
    if [ $(os_version) == "Darwin" ]; then

      alias ls="ls -G"
    
#     Mac Hidden Files
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
      
#     Activate bash completion
      if ! command_exists brew; then
          echo "bash-completion not available (try 'brew install bash-completion' first)"
      elif ! [ -f $(brew --prefix)/etc/bash_completion ]; then
          echo "$(brew --prefix)/etc/bash_completion missing."
      else 
          source $(brew --prefix)/etc/bash_completion
      fi
      
    fi