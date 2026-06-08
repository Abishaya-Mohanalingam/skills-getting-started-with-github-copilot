"""
Test suite for the Mergington High School API.
"""

import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that all activities are returned."""
        response = client.get("/activities")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_get_activities_includes_activity_details(self, client, reset_activities):
        """Test that activities include all required fields."""
        response = client.get("/activities")
        data = response.json()

        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

    def test_get_activities_includes_participants(self, client, reset_activities):
        """Test that participants list is included."""
        response = client.get("/activities")
        data = response.json()

        activity = data["Chess Club"]
        assert "michael@mergington.edu" in activity["participants"]
        assert "daniel@mergington.edu" in activity["participants"]


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_participant_success(self, client, reset_activities):
        """Test successful signup for a new participant."""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200

        data = response.json()
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]

    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        """Test that participant is actually added to the activity."""
        client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")

        response = client.get("/activities")
        activities_data = response.json()
        assert "newstudent@mergington.edu" in activities_data["Chess Club"]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test signup for a non-existent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_participant_returns_400(self, client, reset_activities):
        """Test that duplicate signup returns 400 error."""
        response = client.post(
            "/activities/Chess Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_multiple_different_participants(self, client, reset_activities):
        """Test multiple participants can be added to an activity."""
        client.post("/activities/Gym Class/signup?email=student1@mergington.edu")
        client.post("/activities/Gym Class/signup?email=student2@mergington.edu")

        response = client.get("/activities")
        participants = response.json()["Gym Class"]["participants"]
        assert "student1@mergington.edu" in participants
        assert "student2@mergington.edu" in participants

    def test_signup_same_participant_different_activities(self, client, reset_activities):
        """Test same participant can sign up for multiple activities."""
        email = "multisport@mergington.edu"
        
        response1 = client.post(f"/activities/Chess Club/signup?email={email}")
        response2 = client.post(f"/activities/Gym Class/signup?email={email}")

        assert response1.status_code == 200
        assert response2.status_code == 200

        activities_data = client.get("/activities").json()
        assert email in activities_data["Chess Club"]["participants"]
        assert email in activities_data["Gym Class"]["participants"]


class TestUnregisterFromActivity:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_existing_participant_success(self, client, reset_activities):
        """Test successful unregistration of a participant."""
        response = client.delete(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200

        data = response.json()
        assert "Unregistered" in data["message"]
        assert "michael@mergington.edu" in data["message"]

    def test_unregister_removes_participant_from_activity(self, client, reset_activities):
        """Test that participant is actually removed from the activity."""
        client.delete("/activities/Chess Club/unregister?email=michael@mergington.edu")

        response = client.get("/activities")
        activities_data = response.json()
        assert "michael@mergington.edu" not in activities_data["Chess Club"]["participants"]

    def test_unregister_nonexistent_participant_returns_400(self, client, reset_activities):
        """Test unregistering a non-existent participant returns 400."""
        response = client.delete(
            "/activities/Chess Club/unregister?email=nonexistent@mergington.edu"
        )
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]

    def test_unregister_from_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test unregistering from non-existent activity returns 404."""
        response = client.delete(
            "/activities/Nonexistent Club/unregister?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_multiple_participants(self, client, reset_activities):
        """Test unregistering multiple participants."""
        # Add new participants first
        client.post("/activities/Gym Class/signup?email=student1@mergington.edu")
        client.post("/activities/Gym Class/signup?email=student2@mergington.edu")

        # Unregister them
        response1 = client.delete(
            "/activities/Gym Class/unregister?email=student1@mergington.edu"
        )
        response2 = client.delete(
            "/activities/Gym Class/unregister?email=student2@mergington.edu"
        )

        assert response1.status_code == 200
        assert response2.status_code == 200

        activities_data = client.get("/activities").json()
        assert "student1@mergington.edu" not in activities_data["Gym Class"]["participants"]
        assert "student2@mergington.edu" not in activities_data["Gym Class"]["participants"]


class TestIntegrationScenarios:
    """Integration tests combining multiple operations."""

    def test_signup_and_unregister_flow(self, client, reset_activities):
        """Test complete signup and unregister flow."""
        email = "integration@mergington.edu"
        activity = "Art Club"

        # Sign up
        signup_response = client.post(f"/activities/{activity}/signup?email={email}")
        assert signup_response.status_code == 200

        # Verify signup
        activities_data = client.get("/activities").json()
        assert email in activities_data[activity]["participants"]

        # Unregister
        unregister_response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert unregister_response.status_code == 200

        # Verify unregister
        activities_data = client.get("/activities").json()
        assert email not in activities_data[activity]["participants"]

    def test_participant_count_updates_on_signup(self, client, reset_activities):
        """Test that participant count increases on signup."""
        activity = "Drama Club"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity]["participants"])

        client.post(f"/activities/{activity}/signup?email=newcomer@mergington.edu")

        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity]["participants"])

        assert final_count == initial_count + 1

    def test_participant_count_decreases_on_unregister(self, client, reset_activities):
        """Test that participant count decreases on unregister."""
        activity = "Chess Club"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity]["participants"])

        client.delete(f"/activities/{activity}/unregister?email=michael@mergington.edu")

        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity]["participants"])

        assert final_count == initial_count - 1
