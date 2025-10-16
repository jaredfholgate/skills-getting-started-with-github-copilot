"""
Test configuration and fixtures for the High School Management System API tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def sample_activities():
    """Return a copy of the original activities data for testing."""
    return copy.deepcopy({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        }
    })

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities data before each test to ensure test isolation."""
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Team practices and inter-school basketball competitions",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim training sessions and meets preparation",
            "schedule": "Mondays and Wednesdays, 3:45 PM - 5:15 PM",
            "max_participants": 18,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting workshops and school play productions",
            "schedule": "Fridays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu", "amelia@mergington.edu"]
        },
        "Photography Workshop": {
            "description": "Learn photography techniques and photo editing",
            "schedule": "Wednesdays, 3:30 PM - 4:45 PM",
            "max_participants": 16,
            "participants": ["charlotte@mergington.edu", "ella@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Prepare for science competitions across multiple disciplines",
            "schedule": "Mondays, 3:30 PM - 4:45 PM",
            "max_participants": 20,
            "participants": ["ethan@mergington.edu", "logan@mergington.edu"]
        },
        "Mathletes": {
            "description": "Problem-solving sessions and math competition preparation",
            "schedule": "Thursdays, 3:30 PM - 4:45 PM",
            "max_participants": 22,
            "participants": ["harper@mergington.edu", "evelyn@mergington.edu"]
        }
    }
    
    # Clear and repopulate activities
    activities.clear()
    activities.update(original_activities)
    yield
    # Cleanup after test (optional, since autouse fixture runs before each test)
    activities.clear()
    activities.update(original_activities)