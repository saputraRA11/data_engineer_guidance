from prefect.deployments import Deployment
from prefect.infrastructure.container import DockerContainer
from main import main

docker_container_block = DockerContainer.load("prefect-v1")

docker_deployment = Deployment.build_from_flow(
    flow=main,
    name="docker-flow",
    infrastructure=docker_container_block
)

if __name__ == "__main__":
    docker_deployment.apply()