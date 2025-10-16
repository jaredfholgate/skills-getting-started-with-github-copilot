# FastAPI Tests

This directory contains comprehensive tests for the High School Management System API.

## Test Structure

- `conftest.py` - Test configuration and fixtures
- `test_app.py` - Main test suite with comprehensive endpoint testing

## Test Coverage

The tests cover:

### Root Endpoint (`/`)
- Redirects to static index.html

### Activities Endpoint (`/activities`)
- Returns all activities
- Correct data structure validation

### Signup Endpoint (`POST /activities/{activity_name}/signup`)
- Successful signup
- Nonexistent activity handling
- Duplicate signup prevention
- Multiple activity signups

### Unregister Endpoint (`DELETE /activities/{activity_name}/signup`)
- Successful unregistration
- Nonexistent activity handling
- Unregistering non-registered users
- Removing existing participants

### Integration Tests
- Complete signup/unregister workflows
- Data persistence during session

### Edge Cases
- Activity names with spaces
- Empty email parameters
- URL encoding handling

## Running Tests

### Using pytest directly:
```bash
# Basic test run
pytest tests/ -v

# With coverage report
pytest tests/ --cov=src --cov-report=term-missing -v
```

### Using the test runner script:
```bash
./run_tests.sh
```

## Test Results

Current test coverage: **100%** (33/33 statements covered)
Total tests: **17** (all passing)

## Dependencies

The following packages are required for testing:
- `pytest` - Testing framework
- `httpx` - HTTP client for testing FastAPI
- `pytest-asyncio` - Async testing support
- `pytest-cov` - Coverage reporting

These are automatically installed when you install from `requirements.txt`.