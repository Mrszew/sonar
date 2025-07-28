# Third Party Integration Demo

This is a demo project for testing SonarCloud integration with GitHub Actions.

## Features

- Flask web application
- SonarCloud integration
- GitHub Actions workflow
- Docker support
- GitHub Container Registry integration

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python -m unittest discover`

## SonarCloud Integration

This project is configured with SonarCloud for code quality analysis.
The workflow runs on every push and pull request.

## Docker Integration

Docker images are automatically built and pushed to GitHub Container Registry:
- Images are built on push to main branch
- Available at: `ghcr.io/mrszew/sonar`
- Tags: `main`, `latest`, `sha-{commit}`

## Status

✅ Automatic Analysis disabled in SonarCloud
✅ GitHub Actions workflow configured
✅ Simple SonarCloud setup
✅ Docker build and push to GitHub Container Registry
✅ Write permissions for packages added
