# Dice DevOps Client

Dockerized client for the Dice DevOps capstone project. The client requests a generated file from the server over the shared Docker network, saves it to `/clientdata/received_payload.txt`, and verifies its integrity using SHA-256.

## Repository contents

```text
dice-devops-client/
├── .github/
│   └── workflows/
│       └── docker-publish.yml
├── app/
│   └── server.py
├── .dockerignore
├── docker-compose.yml
└── Dockerfile
```

> Check the actual files in this repository before submission and adjust this tree if your current client source filename or folder layout differs.

## Prerequisites

- Docker Desktop (or Docker Engine) with Docker Compose
- The Dice DevOps server running on the same Docker network
- A Docker Hub account if you intend to publish the image

## Connect to the server

The client Compose configuration uses this server URL:

```text
http://server:8000/file
```

The hostname `server` is resolved through the shared Docker network. The client and server Compose projects must both connect to the external network named `dice-net`.

Create the network once if it does not already exist:

```powershell
docker network create dice-net
```

Start the server project first, from the server repository:

```powershell
docker compose up --build -d
```

Then, from this client repository, build and run the client:

```powershell
docker compose up --build
```

The client is designed to perform its transfer and verification task and then exit. An exit status of `0` after successful completion is expected for this one-shot client task.

## Verify the result

View the client logs:

```powershell
docker compose logs client
```

The demonstrated successful output included:

- Connection to `http://server:8000/file`
- File saved at `/clientdata/received_payload.txt`
- Payload size of `1024` bytes
- `SUCCESS: File integrity verified!`

The Compose configuration defines a named volume `clientvol` mounted at `/clientdata`, so the received file is stored in the client volume.

To inspect the Compose service status, including a completed one-shot container:

```powershell
docker compose ps -a
```

## Copy the received file to the host (optional)

If the client container still exists, you can try:

```powershell
docker cp dice-client:/clientdata/received_payload.txt .\received_payload.txt
```

If Docker Desktop returns an API error, use the existing volume/container state to investigate rather than assuming the copy succeeded. In the demonstrated run, `received_payload.txt` was already present in the repository directory and measured `1024` bytes.

Calculate the local SHA-256 hash in PowerShell:

```powershell
Get-FileHash .\received_payload.txt -Algorithm SHA256 | Format-List
```

Compare the full hash with the checksum reported by the server/client logs. Matching hashes confirm that the local file content matches the server's generated payload.

## Docker Hub and GitHub Actions

The repository contains a GitHub Actions workflow for building and publishing the client image to Docker Hub.

Configure these GitHub Actions repository secrets if the workflow uses Docker Hub login:

- `DOCKERHUB_USERNAME` — your Docker Hub username
- `DOCKERHUB_TOKEN` — a Docker Hub access token (not your account password)

Do not place credentials in the workflow file or commit them to Git. After a successful workflow run, verify the image and tag in Docker Hub. Use the exact image name and tag configured in your workflow.

## Useful commands

```powershell
# Show client service and completed container
docker compose ps -a

# View client logs
docker compose logs --tail=50 client

# Run the client again
docker compose up --build

# Stop/remove Compose resources
docker compose down
```

The named `clientvol` volume is retained by a normal `docker compose down`. Avoid `docker compose down -v` unless you intentionally want to delete the stored payload.

## Troubleshooting

- **Network not found:** create the shared network with `docker network create dice-net`.
- **Name resolution or connection error:** make sure the server service is running and both projects are attached to the same external network.
- **Connection refused:** check the server logs and confirm it is listening on port `8000`.
- **Client exits after processing:** this is expected after a successful one-shot transfer; inspect its exit code and logs.
- **Checksum mismatch:** compare the full SHA-256 values, confirm the correct file was saved, and rerun the transfer.
- **Docker Hub authentication error:** verify `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` in GitHub repository Actions secrets.

## Capstone verification

The demonstrated client logs reported a `1024`-byte file and `SUCCESS: File integrity verified!`. The local PowerShell SHA-256 output matched the checksum reported in the application logs.

## Scope note

This README documents the client container, file retrieval, integrity check, and image-publishing workflow evidenced in the project. It does not claim that AWS EC2/VPC provisioning, Terraform, Grafana monitoring, or a complete automated deployment pipeline has been implemented.