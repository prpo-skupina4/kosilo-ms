# kosilo-ms
Kosilo™ micro service

## Development

### Running Tests

To run the tests locally:

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r test_requirements.txt

# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=. --cov-report=term-missing
```

### CI/CD

This project uses GitHub Actions for continuous integration and deployment.

#### Continuous Integration

Tests run automatically on:
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches

The CI workflow runs:
- Unit tests with pytest
- Code coverage reporting
- Test results are uploaded to codecov

#### Docker Image Deployment

Docker images are automatically built and pushed to [Docker Hub](https://hub.docker.com/repository/docker/adrian4096/prpo-app) when a new release is created.

##### Required GitHub Secrets

To enable Docker Hub deployment, the following secrets must be configured in the repository settings:

1. **DOCKERHUB_USERNAME**: Your Docker Hub username
2. **DOCKERHUB_TOKEN**: Docker Hub access token (recommended) or password

**Setting up secrets:**
1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `DOCKERHUB_USERNAME` with your Docker Hub username
4. Add `DOCKERHUB_TOKEN` with your Docker Hub access token
   - Create a token at https://hub.docker.com/settings/security

##### Creating a Release

To trigger a Docker image build and push:

1. **Via Git Tags:**
   ```bash
   # Create and push a version tag
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Via GitHub Releases:**
   - Go to repository → Releases → "Create a new release"
   - Choose or create a tag (e.g., `v1.0.0`)
   - Fill in release title and description
   - Click "Publish release"

##### Image Tags

The workflow produces the following Docker image tags:

- **Version tag**: `adrian4096/prpo-app:X.Y.Z` (e.g., `1.0.0`)
- **Major.Minor tag**: `adrian4096/prpo-app:X.Y` (e.g., `1.0`)
- **Major tag**: `adrian4096/prpo-app:X` (e.g., `1`)
- **Latest tag**: `adrian4096/prpo-app:latest` (for non-prerelease tags on default branch)

**Example:**
- Git tag `v1.2.3` produces images tagged as: `1.2.3`, `1.2`, `1`, and `latest`
- Git tag `v2.0.0-beta.1` produces images tagged as: `2.0.0-beta.1` (no `latest` tag for prereleases)

##### Multi-Architecture Support

Images are built for multiple architectures:
- `linux/amd64` (x86_64)
- `linux/arm64` (ARM 64-bit)

##### Pulling the Image

```bash
# Pull latest version
docker pull adrian4096/prpo-app:latest

# Pull specific version
docker pull adrian4096/prpo-app:1.0.0

# Run the container
docker run -p 8000:8000 adrian4096/prpo-app:latest
```
