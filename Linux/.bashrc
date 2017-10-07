#!/bin/bash

#  ---------------------------------------------------------------------------
#
#  Description:  This file holds all my BASH configurations and aliases
#
#  Load order for Bash profile (loads first found):
#   1. ~/.bash_profile
#   2. ~/.bash_login
#   3. ~/.profile


#   -------------------------------
#   1.  ENVIRONMENT CONFIGURATION
#   -------------------------------

#   Set Text Formatting
    BOLD="\e[1m"
#   Set Text Foreground Colors
    RED="\e[31m"
    L_RED="\e[91m"
    DIM="\e[2m"
    BLUE="\e[34m"
    CYAN="\e[36m"
    L_CYAN="\e[96m"
    YELLOW="\e[33m"
    L_YELLOW="\e[93m"
    L_GREEN="\e[92m"
    GREEN="\e[32m"
    L_GRAY="\e[37m"
    D_GRAY="\e[90m"
    ORANGE="\e[38;5;215m"
#   Disable Colors
    Rcol="\e[0m"

#   Prompt
#   ------------------------------------------------------------

#   ASCII Symbols │ ┤ ├ ┘ ┌ ┐

#   Prompt Variables
    PROMPT_COMMAND=__prompt_command
    
    function __prompt_command() {
      local EXIT="$?"
      # Return Status Badges
      local ENABLE_EMOJI=true
      local SUCCESS_BADGE="${L_GREEN}✔${Rcol} "
      local EMOJI_SUCCESS_BADGE="🍺  "
      local FAIL_BADGE="${L_RED}✸${Rcol} "
      local EMOJI_FAIL_BADGE="💥  "

      local USER="${BOLD}${L_GREEN}\u${Rcol}"
      local HOST="${L_GREEN}\h${Rcol}"
      # echo "Calling parse_git_branch"
      local Time="${ORANGE}\t${Rcol}"
      local GIT_BRANCH="${CYAN}`my_git_branch`${Rcol}"
      local Path="${YELLOW}\W${Rcol}"
      # echo "Finished calling parse_git_branch"

      if $ENABLE_EMOJI; then
        SUCCESS_BADGE=$EMOJI_SUCCESS_BADGE
        FAIL_BADGE=$EMOJI_FAIL_BADGE
      fi

      local Git_Status="`my_git_status`"
      echo ${Git_Status}

      local BADGE=$([ $EXIT != 0 ] && echo $FAIL_BADGE || echo $SUCCESS_BADGE)

      PS1="\n"
      PS1+="┌─ ${BADGE}  ─┤${USER}@${HOST}├─┤${Time}├─┤${Path}"
      if [ ! "${GIT_BRANCH}" == "" ]; then PS1+="├─┤${GIT_BRANCH}"; fi
      PS1+="│\n└─► # "

    }


    # Use if terminal has full unicode support
    # export PS1="\n┌─ \`if [ \$? != 0 ]; then echo 💥 ; else echo 🍺  ; fi\`  ${L_YELLOW}(${BOLD}\u${Rcol}@${L_YELLOW}\h) ${L_GREEN}\t ${L_CYAN}[\W] ${Rcol}\`parse_git_branch\`\n└────► # "
    # Use if terminal supports special characters
    # export PS1="\n┌─ \`if [ \$? != 0 ]; then echo ${RED}✸ ; else echo ${L_GREEN}✔  ; fi\` ${L_YELLOW}(${BOLD}\u${Rcol}@${L_YELLOW}\h) ${L_GREEN}\t ${L_CYAN}[\W] ${Rcol}\n└────► # "
    # Use if terminal does not support special characters (eg. Windows CMD)
    # export PS1="\n┌─ \`if [ \$? != 0 ]; then echo ${RED} X ; else echo ${L_GREEN} O  ; fi\`  ${L_YELLOW}${BOLD}(\u${Rcol}@${L_YELLOW}\h) ${L_GREEN}\t ${L_CYAN}[\W] ${Rcol}\n└────> # "


#   Set Paths
#   ------------------------------------------------------------
    export PATH="/usr/local/bin:$PATH"
    

#   Set Default Editor (change 'Nano' to the editor of your choice)
#   ------------------------------------------------------------
    export EDITOR=/usr/bin/nano

#   Set default blocksize for ls, df, du
#   from this: http://hints.macworld.com/comment.php?mode=view&cid=24491
#   ------------------------------------------------------------
    export BLOCKSIZE=1k


#   Add color to terminal
#   from http://osxdaily.com/2012/02/21/add-color-to-the-terminal-in-mac-os-x/
#   ------------------------------------------------------------
#   export CLICOLOR=1
#   export LSCOLORS=GxFxCxDxBxegedabagaced



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
    color() { echo "$1$2${Rcol}"; }





function my_git_branch(){
    echo `git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'`
}

function my_git_status(){

  ## Get status and branch and replace newline (\n) with colon (:)
  local Status="$(git status --porcelain 2>/dev/null | tr '\n' ':')"

  echo "$(echo ${Status} | grep -v "^$" | wc -l | tr -d ' ' )"
  echo ${Status}
}







# get current branch in git repo
function parse_git_branch() {
  
  local Branch=`git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'`
  echo ${Branch}

# if [ ! "${BRANCH}" == "" ]
#  then
#    STAT=`parse_git_dirty`
#    echo "$CYAN(${BRANCH}$Rcol${STAT}$CYAN)$Rcol"
#  else
#    echo ""
#  fi
}



# get current status of git repo
function parse_git_dirty {
  status=`git status 2>&1 | tee`

  dirty=`echo -n "${status}" 2> /dev/null | grep "modified:" &> /dev/null; echo "$?"`
  # untracked=`echo -n "${status}" 2> /dev/null | grep "Untracked files" &> /dev/null; echo "$?"`
  # ahead=`echo -n "${status}" 2> /dev/null | grep "Your branch is ahead of" &> /dev/null; echo "$?"`
  # newfile=`echo -n "${status}" 2> /dev/null | grep "new file:" &> /dev/null; echo "$?"`
  # renamed=`echo -n "${status}" 2> /dev/null | grep "renamed:" &> /dev/null; echo "$?"`
  # deleted=`echo -n "${status}" 2> /dev/null | grep "deleted:" &> /dev/null; echo "$?"`
  bits=''
  if [ "${renamed}" == "0" ]; then
    bits=">${bits}"
  fi
  # if [ "${ahead}" == "0" ]; then    ## Ahead
  #   bits="*${bits}"
  # fi
  # if [ "${newfile}" == "0" ]; then
  #   bits="+${bits}"
  # fi
  # if [ "${untracked}" == "0" ]; then
  #   bit='?'
  #   bits="$(color ${L_YELLOW} $bit)$bits"
  # fi
  # if [ "${deleted}" == "0" ]; then
  #   bits="x${bits}"
  # fi
  # if [ "${dirty}" == "0" ]; then
  #   bits="${RED}!${Rcol}${bits}"
  # fi
  # if [ ! "${bits}" == "" ]; then
  #   echo "${bits}"
  # else
  #   echo ""
  # fi
}




function git_status(){
    ### Add Git Status ### {{{
    ## Inspired by http://www.terminally-incoherent.com/blog/2013/01/14/whats-in-your-bash-prompt/
    if [[ $(command -v git) ]]; then
      local GStat="$(git status --porcelain -b 2>/dev/null | tr '\n' ':')"

      if [ "$GStat" ]; then
        ### Fetch Time Check ### {{{
        local LAST=$(stat -c %Y $(git rev-parse --git-dir 2>/dev/null)/FETCH_HEAD 2>/dev/null)
        if [ "${LAST}" ]; then
          local TIME=$(echo $(date +"%s") - ${LAST} | bc)
          ## Check if more than 60 minutes since last
          if [ "${TIME}" -gt "3600" ]; then
            git fetch 2>/dev/null
            PS1+=' +'
            ## Refresh var
            local GStat="$(git status --porcelain -b 2>/dev/null | tr '\n' ':')"
          fi
        fi
        ### End Fetch Check ### }}}

        ### Test For Changes ### {{{
        ## Change this to test for 'ahead' or 'behind'!
        local GChanges="$(echo ${GStat} | tr ':' '\n' | grep -v "^$" | grep -v "^\#\#" | wc -l | tr -d ' ')"
        if [ "$GChanges" == "0" ]; then
          local GitCol=$Gre
          else
          local GitCol=${RED}
        fi
        ### End Test Changes ### }}}

        ### Find Branch ### {{{
        local GBra="$(echo ${GStat} | tr ':' '\n' | grep "^##" | cut -c4- | grep -o "^[a-zA-Z]\{1,\}[^\.]")"
        if [ "$GBra" ]; then
          if [ "$GBra" == "master" ]; then
            local GBra="M"      ## Because why waste space
          fi
          else
          local GBra="ERROR"      ## It could happen supposedly?
        fi
        ### End Branch ### }}}

        PS1+=" ${GitCol}[$GBra]${RCol}"	## Add result to prompt

        ### Find Commit Status ### {{{
        ## Test Modified and Untracked for "0"
        # local GDel="$(echo ${GStat} | tr ':' '\n' | grep -c "^[ MARC]D")"

        local GAhe="$(echo ${GStat} | tr ':' '\n' | grep "^##" | grep -o "ahead [0-9]\{1,\}" | grep -o "[0-9]\{1,\}")"
        if [ "$GAhe" ]; then
          PS1+="${Gre}↑${RCol}${GAhe}"    ## Ahead
        fi

        ## Needs a `git fetch`
        local GBeh="$(echo ${GStat} | tr ':' '\n' | grep "^##" | grep -o "behind [0-9]\{1,\}" | grep -o "[0-9]\{1,\}")"
        if [ "$GBeh" ]; then
          PS1+="${Red}↓${RCol}${GBeh}"    ## Behind
        fi

        local GMod="$(echo ${GStat} | tr ':' '\n' | grep -c "^[ MARC]M")"
        if [ "$GMod" -gt "0" ]; then
          PS1+="${Pur}≠${RCol}${GMod}"    ## Modified
        fi

        local GUnt="$(echo ${GStat} | tr ':' '\n' | grep -c "^\?")"
        if [ "$GUnt" -gt "0" ]; then
          PS1+="${Yel}?${RCol}${GUnt}"    ## Untracked
        fi
        ### End Commit Status ### }}}
      fi
      else
      MISSING_ITEMS+="git-prompt, "
    fi
    ### End Git Status ### }}}
}