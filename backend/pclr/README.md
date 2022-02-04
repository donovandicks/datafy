# PCLR

## Runbook

0. `docker buildx build --platform linux/amd64 -t [container_tag] [path_to_project]`
1. `docker save -o [path to output file] [image]`
2. `scp -i [.pem file] [path to tar] [user@path_to_container:path_to_file]`
3. `ssh -i [.pem file] [user@path_to_container]`
4. via `ssh`: `sudo docker load -i [path_to_file]`
5. via `ssh`: `sudo docker run [image]`
