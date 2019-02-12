#!/bin/bash

# Description:  This file holds all my BASH configurations and aliases

#* Exit early if not running interactively
#* ------------------------------------------------------------
  
  [[ "$-" != *i* ]] && return

#* Load alternate shell
#* ------------------------------------------------------------

# bash -c zsh


#* Export variables to the environment of all the child
#* processes running in the current shell.
#* ------------------------------------------------------------

  # Set Default Editor (change 'vim' to the editor of your choice)
  export EDITOR=/usr/bin/vim


  # Set default blocksize for ls, df, du
  # source: http://hints.macworld.com/comment.php?mode=view&cid=24491
  export BLOCKSIZE=1k


#* Colors and Formatting
#* ------------------------------------------------------------

  # Set Text Formatting
  BOLD="\[\e[1m\]"

  # Set Text Foreground Colors
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

  # Disable Colors
  Rcol="\[\e[0m\]"


#* Prompt
#* ------------------------------------------------------------

  # Prompt Variables
  PROMPT_COMMAND=__prompt_command
  
  function __prompt_command() {
    local EXIT="$?"
        
    # Return Status Badges
    local ENABLE_EMOJI=false
    local SUCCESS_BADGE="${L_GREEN}✔${Rcol} "
    local EMOJI_SUCCESS_BADGE="🍺  "
    local FAIL_BADGE="${L_RED}✸${Rcol} "
    local EMOJI_FAIL_BADGE="💥  "

    local User="${BOLD}${L_GREEN}\u${Rcol}"
    local Host="${L_GREEN}\h${Rcol}"
    local Time="${ORANGE}\t${Rcol}"
    local Path="${YELLOW}\W${Rcol}"

    # Use Emojis if Enabled
    if $ENABLE_EMOJI; then
      SUCCESS_BADGE=$EMOJI_SUCCESS_BADGE
      FAIL_BADGE=$EMOJI_FAIL_BADGE
    fi
    local BADGE=$([ ${EXIT} != 0 ] && echo ${FAIL_BADGE} || echo ${SUCCESS_BADGE})

    # Git Integration
    local Git_Branch=`my_git_branch`
    local Git_Status=`my_git_status`
    local Mod=$(echo ${Git_Status} | tr ':' '\n' | grep -c "M")

    if [ "${Mod}" -gt 0 ]; then Mod="${YELLOW}●${Rcol}"; else Mod="${L_GREEN}●${Rcol}"; fi

    # Build PS1 String
    Verbose_Theme="\n${WHITE}┌─${Rcol} ${BADGE}  ${User}@${Host} ${Time} ${WHITE}[${Rcol}${Path}${WHITE}]${Rcol}"
    if [ ! "${Git_Branch}" == "" ]; then 
      Git_Branch="${L_CYAN}${Git_Branch}${Rcol}"; Verbose_Theme+=" (${Git_Branch} ${Mod})"; fi
    Verbose_Theme+="\n${WHITE}└─► ${Rcol}# "

    Simpler_Theme="\n${YELLOW}\w${Rcol}"
    if [ ! "${Git_Branch}" == "" ]; then 
      Git_Branch="${L_CYAN}${Git_Branch}${Rcol}"; Simpler_Theme+=" [${Git_Branch}${Mod}]"; fi
    Simpler_Theme+="\n ${BOLD}$([ ${EXIT} != 0 ] && echo ${L_RED}\$${Rcol} || echo ${L_GREEN}\$${Rcol})${Rcol} "

    Theme=$Verbose_Theme

    PS1=$Theme
  }

    



#* Set aliases
#* ------------------------------------------------------------

  # General Aliases
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

  # Enable color support for commands if supported
  if [ -x /usr/bin/dircolors ]; then
      alias ls='ls --color=auto'
      alias grep='grep --color=auto'
      alias fgrep='fgrep --color=auto'
      alias egrep='egrep --color=auto'
  fi

# Special Aliases

  # Runs previous command as sudo
  alias please='sudo "$BASH" -c "$(history -p !!)"' 

  # Networking Aliases
  alias myip='curl ipinfo.io/ip'

  # Add bash completion for git if exists
  if [ -f ~/.git-completion.bash ]; then
    source ~/.git-completion.bash
  else
    echo ".git-completion.bash file not found"
  fi


#* Helper Functions
#* ------------------------------------------------------------

  command_exists() { command -v "$1" > /dev/null 2>&1; }

  os_version() { echo $(uname -s); }

  color() { echo "$1$2${Rcol}"; }

  my_git_branch(){
    echo `git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'`
  }

  my_git_status(){
    # Get status and branch and replace newline (\n) with colon (:)
    local Status="$(git status --porcelain 2>/dev/null | tr '\n' ':')"
    echo ${Status}
  }



#* Operating System/Shell-Specific Commands
#* ------------------------------------------------------------

  # Determine which OS/Shell using the kernel name
  unameOut="$(uname -s)"
  case "${unameOut}" in
      Linux*)     machine=Linux;;
      Darwin*)    machine=macOS;;
      CYGWIN*)    machine=Cygwin;;
      MINGW*)     machine=MinGw;;
      *)          machine="UNKNOWN:${unameOut}"
  esac

  # Mac OSX
  if [ ${machine} == "macOS" ]; then

    alias ls="ls -G"
    
    # Show/Hide Hidden Files
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
    # Reset Launch Services - Fixes 'Open With > Fetching...' issue
    function resetServices() {
        /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister -kill -seed -r -f -v -domain local -domain user -domain system
        echo 'Launch Services Reset!'
    }
      
    # Activate bash completion
    if ! command_exists brew; then
        echo "bash-completion not available (try 'brew install bash-completion' first)"
    elif ! [ -f $(brew --prefix)/etc/bash_completion ]; then
        echo "$(brew --prefix)/etc/bash_completion missing."
    else 
        source $(brew --prefix)/etc/bash_completion
    fi
    
  fi


  # MINGW
  if [ ${machine} == "MinGw" ]; then

    # Check that we haven't already been sourced.
    # [[ -z ${CYG_SYS_BASHRC} ]] && CYG_SYS_BASHRC="1" || return

    # If MSYS2_PS1 is set, use that as default PS1;
    # if a PS1 is already set and exported, use that;
    # otherwise set a default prompt
    # of user@host, MSYSTEM variable, and current_directory
    unset PROMPT_COMMAND
    [[ -n "${MSYS2_PS1}" ]] && export PS1="${MSYS2_PS1}"
    [[ $(declare -p PS1 2>/dev/null | cut -c 1-11) = 'declare -x ' ]] || \
      export PS1='\[\e]0;\w\a\]\n\[\e[32m\]\u@\h \[\e[35m\]$MSYSTEM\[\e[0m\] \[\e[33m\]\w\[\e[0m\]\n\$ '

    # Uncomment to use the terminal colours set in DIR_COLORS
    # eval "$(dircolors -b /etc/DIR_COLORS)"

    # Fixup git-bash in non login env
    shopt -q login_shell || . /etc/profile.d/git-prompt.sh

  fi