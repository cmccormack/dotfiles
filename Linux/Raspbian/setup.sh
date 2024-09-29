# Update repositories and install upgrades
sudo apt update && sudo apt upgrade -y

# Install tools
sudo apt install -y curl git htop neovim zsh

# Install various dev dependencies
sudo apt install -y build-essential libssl-dev zlib1g-dev \ ca-certificates
libbz2-dev libreadline-dev libsqlite3-dev \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Install python tools pipx and poetry
sudo apt install -y pipx
pipx ensurepath
pipx install poetry

# Add current user to docker group
sudo usermod -aG docker $USER

# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install Antigen to home directory
curl -L git.io/antigen > $HOME/antigen.zsh

# Copy antigenrc to home directory
cp .antigenrc $HOME/.antigenrc
echo '\n# Load Antigen' >> $HOME/.zshrc
echo 'source $HOME/.antigenrc' >> $HOME/.zshrc

# Install pyenv
curl https://pyenv.run | bash

# Add pyenv to .zshrc
echo '\n# Pyenv' >> ~/.zshrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Setup Docker
## Add Docker's official GPG key:
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

## Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

## Install latest version of Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
