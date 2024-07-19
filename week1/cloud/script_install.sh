function main(){
    echo "========= install pyenv ===========";
    curl https://pyenv.run | bash;
    sudo apt update && echo -e 'export PYENV_ROOT="$HOME/.pyenv"\nexport PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc;
    echo -e 'eval "$(pyenv init --path)"\neval "$(pyenv init -)"' >> ~/.bashrc;
    exec "$SHELL";
    pyenv install -v 3.9;

    echo "========= install terraform ===========";
    sudo apt-get update && sudo apt-get install -y gnupg software-properties-common;
    wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null;
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list;
    sudo apt update && sudo apt-get install terraform;

    echo "========= install docker ===========";
    sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev;
    sudo apt install apt-transport-https ca-certificates curl software-properties-common;
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -;
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable";
    apt-cache policy docker-ce;
    sudo apt install docker-ce;
    sudo apt update && sudo groupadd docker;
    sudo usermod -aG docker ${USER};
    newgrp docker;
    docker ps;
}
main