import urllib.parse


def test_get_activities(client):
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    # Basic sanity checks
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success(client):
    activity = "Chess Club"
    email = "testuser@example.com"
    # Sign up
    res = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert res.status_code == 200
    assert f"Signed up {email}" in res.json()["message"]

    # Verify participant appears
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]


def test_signup_already_signed(client):
    activity = "Chess Club"
    email = "duplicate@example.com"

    # First signup should succeed
    res1 = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert res1.status_code == 200

    # Second signup should fail with 400
    res2 = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert res2.status_code == 400


def test_remove_participant_success(client):
    activity = "Chess Club"
    participant = "michael@mergington.edu"  # exists in initial data

    res = client.delete(f"/activities/{urllib.parse.quote(activity)}/participants/{urllib.parse.quote(participant)}")
    assert res.status_code == 200
    assert f"Removed {participant}" in res.json()["message"]

    data = client.get("/activities").json()
    assert participant not in data[activity]["participants"]


def test_remove_participant_not_found(client):
    activity = "Chess Club"
    participant = "not-found@example.com"

    res = client.delete(f"/activities/{urllib.parse.quote(activity)}/participants/{urllib.parse.quote(participant)}")
    assert res.status_code == 404
