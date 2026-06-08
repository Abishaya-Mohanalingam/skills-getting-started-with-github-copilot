"""
Pytest configuration and shared fixtures for the test suite.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test."""
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
        "Soccer Team": {
            "description": "Competitive soccer team practicing drills and playing matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 22,
            "participants": ["alex@mergington.edu", "nina@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Basketball training, scrimmages, and inter-school games",
            "schedule": "Mondays, Wednesdays, 4:30 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["maria@mergington.edu", "kevin@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore visual arts: painting, drawing, and sculpture",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["linda@mergington.edu", "peter@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater rehearsals, acting workshops, and school productions",
            "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["sara@mergington.edu", "tom@mergington.edu"]
        },
        "Debate Club": {
            "description": "Practice public speaking, argumentation, and participate in debates",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["isabel@mergington.edu", "ryan@mergington.edu"]
        },
        "Math Club": {
            "description": "Work on math competitions, puzzles, and problem-solving sessions",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["anna@mergington.edu", "luke@mergington.edu"]
        }
    }

    # Clear existing activities and restore originals
    activities.clear()
    activities.update(original_activities)

    yield

    # Cleanup after test
    activities.clear()
    activities.update(original_activities)
