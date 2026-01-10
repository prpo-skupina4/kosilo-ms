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

This project uses GitHub Actions for continuous integration. Tests run automatically on:
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches

The CI workflow runs:
- Unit tests with pytest
- Code coverage reporting
- Test results are uploaded to codecov
