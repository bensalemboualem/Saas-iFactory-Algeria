def test_generate_video(client):
    response = client.post("/api/v1/generate", json={"prompt": "Test", "duration_seconds": 5})
    assert response.status_code == 200
    assert "task_id" in response.json()
