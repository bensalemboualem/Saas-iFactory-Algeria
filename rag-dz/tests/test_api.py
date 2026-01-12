import requests

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    data = r.json()
    assert data["CH"] == "contact@iafactory.ch"
    assert data["DZ"] == "contact@iafactoryalgeria.com"
    print("✅ Root OK")

def test_health():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    print("✅ Health OK")

def test_kpis():
    r = requests.get(f"{BASE_URL}/kpis")
    assert r.status_code == 200
    data = r.json()
    assert "mrr" in data
    print("✅ KPIs OK")

def test_clients():
    r = requests.get(f"{BASE_URL}/clients")
    assert r.status_code == 200
    print("✅ Clients OK")

def test_contacts():
    r = requests.get(f"{BASE_URL}/contacts")
    assert r.status_code == 200
    data = r.json()
    assert data["CH"]["email"] == "contact@iafactory.ch"
    assert data["DZ"]["email"] == "contact@iafactoryalgeria.com"
    print("✅ Contacts OK")

if __name__ == "__main__":
    print("\n🧪 Tests API IA Factory\n")
    test_root()
    test_health()
    test_kpis()
    test_clients()
    test_contacts()
    print("\n✅ TOUS LES TESTS PASSÉS!\n")
