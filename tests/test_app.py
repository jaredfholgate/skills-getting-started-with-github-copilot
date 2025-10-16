"""
Tests for the High School Management System API endpoints.
"""

import pytest
from fastapi import status
from src.app import activities


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to static index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    """Tests for the activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities."""
        response = client.get("/activities")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == len(activities)  # Should have all activities
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        
    def test_get_activities_returns_correct_structure(self, client):
        """Test that activities have the correct data structure."""
        response = client.get("/activities")
        data = response.json()
        
        # Check Chess Club structure
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
        assert chess_club["max_participants"] == 12


class TestSignupEndpoint:
    """Tests for the activity signup endpoint."""
    
    def test_signup_successful(self, client):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["message"] == "Signed up test@mergington.edu for Chess Club"
        
        # Verify the user was added to the activity
        assert "test@mergington.edu" in activities["Chess Club"]["participants"]
    
    def test_signup_nonexistent_activity(self, client):
        """Test signup for an activity that doesn't exist."""
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_signup_already_registered(self, client):
        """Test signup when user is already registered."""
        # First signup
        client.post(
            "/activities/Chess Club/signup",
            params={"email": "test@mergington.edu"}
        )
        
        # Try to signup again
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert data["detail"] == "Student is already signed up"
    
    def test_signup_existing_participant(self, client):
        """Test signup with an email that's already in the participants list."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}  # Already in Chess Club
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert data["detail"] == "Student is already signed up"
    
    def test_signup_multiple_activities(self, client):
        """Test that a user can sign up for multiple different activities."""
        # Sign up for Chess Club
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": "multitest@mergington.edu"}
        )
        assert response1.status_code == status.HTTP_200_OK
        
        # Sign up for Programming Class
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": "multitest@mergington.edu"}
        )
        assert response2.status_code == status.HTTP_200_OK
        
        # Verify user is in both activities
        assert "multitest@mergington.edu" in activities["Chess Club"]["participants"]
        assert "multitest@mergington.edu" in activities["Programming Class"]["participants"]


class TestUnregisterEndpoint:
    """Tests for the activity unregister endpoint."""
    
    def test_unregister_successful(self, client):
        """Test successful unregistration from an activity."""
        # First sign up
        client.post(
            "/activities/Chess Club/signup",
            params={"email": "test@mergington.edu"}
        )
        
        # Then unregister
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["message"] == "Unregistered test@mergington.edu from Chess Club"
        
        # Verify the user was removed from the activity
        assert "test@mergington.edu" not in activities["Chess Club"]["participants"]
    
    def test_unregister_nonexistent_activity(self, client):
        """Test unregister from an activity that doesn't exist."""
        response = client.delete(
            "/activities/Nonexistent Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_unregister_not_signed_up(self, client):
        """Test unregister when user is not signed up for the activity."""
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert data["detail"] == "Student is not signed up for this activity"
    
    def test_unregister_existing_participant(self, client):
        """Test unregistering an existing participant."""
        # Michael is already signed up for Chess Club
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["message"] == "Unregistered michael@mergington.edu from Chess Club"
        
        # Verify michael was removed
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
        # But daniel should still be there
        assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]


class TestCompleteWorkflow:
    """Integration tests for complete user workflows."""
    
    def test_signup_and_unregister_workflow(self, client):
        """Test complete workflow of signing up and then unregistering."""
        email = "workflow@mergington.edu"
        activity = "Programming Class"
        
        # Check initial state
        initial_participants = len(activities[activity]["participants"])
        assert email not in activities[activity]["participants"]
        
        # Sign up
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == status.HTTP_200_OK
        assert len(activities[activity]["participants"]) == initial_participants + 1
        assert email in activities[activity]["participants"]
        
        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert unregister_response.status_code == status.HTTP_200_OK
        assert len(activities[activity]["participants"]) == initial_participants
        assert email not in activities[activity]["participants"]
    
    def test_activity_data_persistence_during_session(self, client):
        """Test that activity data persists during a session."""
        # Get initial count
        response1 = client.get("/activities")
        initial_chess_participants = len(response1.json()["Chess Club"]["participants"])
        
        # Sign up a user
        client.post(
            "/activities/Chess Club/signup",
            params={"email": "persistence@mergington.edu"}
        )
        
        # Check that the change persists
        response2 = client.get("/activities")
        updated_chess_participants = len(response2.json()["Chess Club"]["participants"])
        
        assert updated_chess_participants == initial_chess_participants + 1
        assert "persistence@mergington.edu" in response2.json()["Chess Club"]["participants"]


class TestEdgeCases:
    """Tests for edge cases and error conditions."""
    
    def test_activity_name_with_spaces(self, client):
        """Test that activity names with spaces work correctly."""
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": "spaces@mergington.edu"}
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_empty_email_parameter(self, client):
        """Test behavior with empty email parameter."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": ""}
        )
        # FastAPI should still process this, but with empty string
        assert response.status_code == status.HTTP_200_OK
        assert "" in activities["Chess Club"]["participants"]
    
    def test_special_characters_in_activity_name(self, client):
        """Test behavior with URL encoding in activity names."""
        # Test with URL-encoded space (%20)
        response = client.post(
            "/activities/Programming%20Class/signup",
            params={"email": "encoded@mergington.edu"}
        )
        assert response.status_code == status.HTTP_200_OK