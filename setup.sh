echo "Beginning local dev environment setup"

for cmd in python3 pip curl git gcc
do
    if ! [ -x "$(command -v $cmd)" ]; then
        echo "Error: $cmd is not installed - exiting setup."
        exit 1
    fi
done

echo "All prerequisites installed - continuing with setup."

echo "Updating pip"
$(python3 -m pip install -U pip)

if [ -d "$HOME/.pyenv" ]; then
    echo "Pyenv already installed - continuing"
else
    echo "Installing pyenv"
    $(curl https://pyenv.run | bash)
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> "$HOME/.bashrc"
fi

if [ -d "$(pyenv root)/plugins/pyenv-virtualenv" ]; then
    echo "Pyenv virtualenv already installed - continuing"
else
    echo "Installing pyenv virtualenv"
    $(git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv)
fi

if [ -x "$(command -v poetry)" ]; then
    echo "Poetry already installed - continuing"
else
    echo "Installing poetry"
    $(curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"

    echo "Updating poetry"
    $(poetry self update --preview)
fi

$(source $HOME/.bashrc)

echo "Installing python 3.10.0 via pyenv"
$(pyenv install -s 3.10.0)

echo "Setting up local env on version 3.10.0"
VENV=$(basename $(pwd))
echo "Local venv is named: $VENV"
$(pyenv virtualenv 3.10.0 $(basename $(pwd)))
$(pyenv local $(basename $(pwd)))
$(poetry env use $(pyenv which python))

echo "Installing dependencies"
$(poetry install)

echo -e "$(tput setaf 2)Setup Complete$(tput sgr0)"
