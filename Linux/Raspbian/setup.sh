# Update repositories and install upgrades
sudo apt update && sudo apt upgrade -y

# Install tools
sudo apt install -y curl git htop neovim docker docker-compose zsh

# Install various dev dependencies
sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

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
