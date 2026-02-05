# Testing Guide

## Running Tests

### All Tests
```bash
pytest
```

### With Coverage
```bash
pytest --cov=app --cov-report=term-missing --cov-report=html
```

### Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_security.py

# Specific test function
pytest tests/unit/test_security.py::test_password_hashing
```

## Test Structure

```
tests/
├── unit/                    # Unit tests (no external dependencies)
│   ├── test_security.py     # Password hashing, JWT
│   ├── test_csv_parser.py   # CSV validation
│   ├── test_auth_service.py # Token generation
│   └── ...
├── integration/             # Integration tests (with database)
│   ├── test_registration.py # Full registration flow
│   ├── test_login.py        # Authentication flow
│   ├── test_sample_upload.py # Sample upload
│   └── ...
└── fixtures/                # Test data
    ├── valid_sample.csv
    └── invalid_sample.csv
```

## Coverage Goals

- **Target**: 80%+ code coverage
- **Critical paths**: 100% (auth, security, data validation)
- **View report**: Open `htmlcov/index.html` after running tests with coverage

## Writing Tests

### Unit Test Example
```python
def test_password_hashing():
    password = "testpass123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
```

### Integration Test Example
```python
@pytest.mark.asyncio
async def test_user_registration(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code == 201
```

## CI/CD

Tests run automatically on:
- Pull requests to `dev` and `main`
- Pushes to any branch

GitHub Actions workflow: `.github/workflows/ci.yml`
