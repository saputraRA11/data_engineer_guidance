function main(){
    mkdir v1/keys;
    cp ~/.google/credentials.json v1/keys/credentials.json;
    terraform init;
    terraform apply;
}

main