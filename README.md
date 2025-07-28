# Third-Party Integration Demo

## Description

This project demonstrates integration of third-party services with Continuous Integration and Deployment (Delivery) flows to automate scanning and analysis of code and store artifacts in appropriate repositories.

## Integrated Services

### 1. SonarCloud Integration
- **Static Code Analysis**: Automated code quality analysis on every pull request
- **Quality Gate**: Configured as mandatory requirement for PR validation
- **Security Scanning**: Automated vulnerability detection
- **Code Coverage**: Coverage reporting and thresholds

### 2. Docker Registry Integration
- **GitHub Container Registry**: Artifacts versioned and stored in GHCR
- **Automated Versioning**: Semantic versioning with tags
- **Pull Request Workflow**: Images built and tested on PRs
- **Production Deployment**: Images pushed to registry on main branch

## Setup Instructions

### Prerequisites
- GitHub account
- SonarCloud account (free for public repositories)
- Docker installed locally

### 1. SonarCloud Setup
1. Go to [SonarCloud](https://sonarcloud.io/) and create an account
2. Create a new organization
3. Create a new project for this repository
4. Get your SonarCloud token
5. Add `SONAR_TOKEN` to your GitHub repository secrets

### 2. GitHub Repository Setup
1. Create a new repository on GitHub
2. Push this code to your repository
3. Go to Settings > Secrets and variables > Actions
4. Add the following secrets:
   - `SONAR_TOKEN`: Your SonarCloud token

### 3. SonarCloud Configuration
Update `sonar-project.properties` with your organization key:
```properties
sonar.organization=your-organization-key
```

## Workflow Features

### Quality Gate Configuration
- **Code Coverage**: Minimum 80% coverage required
- **Code Duplication**: Maximum 3% duplication allowed
- **Security Hotspots**: Zero critical security issues
- **Code Smells**: Maximum 10 code smells per 1000 lines
- **Technical Debt**: Maximum 5% technical debt ratio

### Docker Registry Features
- **Automated Builds**: Images built on every push to main
- **Version Tagging**: Automatic semantic versioning
- **Pull Request Testing**: Images built and tested on PRs
- **Registry Storage**: Images stored in GitHub Container Registry

## Usage

### Running Locally
```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-server.txt

# Run tests
python -m unittest discover

# Run application
flask run
```

### Docker
```bash
# Build image
docker build -t third-party-integration-demo .

# Run container
docker run -p 8000:8000 third-party-integration-demo
```

## CI/CD Pipeline

The pipeline includes:
1. **Code Analysis**: SonarCloud scans on every PR
2. **Quality Gate**: PR blocked until quality standards met
3. **Testing**: Automated unit tests
4. **Artifact Building**: Docker images created and versioned
5. **Registry Storage**: Images pushed to GitHub Container Registry

## Business Benefits

- **Code Quality**: Automated quality assurance reduces technical debt
- **Security**: Automated security scanning prevents vulnerabilities
- **Compliance**: Quality gates ensure consistent code standards
- **Efficiency**: Automated analysis reduces manual review time
- **Traceability**: Versioned artifacts provide deployment history

## Original Application

This is based on the [CI/CD Tutorial Sample App](https://github.com/edonosotti/ci-cd-tutorial-sample-app) which demonstrates:
- Flask REST API
- Database operations with SQLAlchemy
- Automated unit tests
- Docker containerization
