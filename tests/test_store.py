from store import Store

def test_eviction_removes_least_recently_used():
    store = Store(max_size=3)
    store.set("a", "1")
    store.set("b", "2")
    store.set("c", "3")
    store.get(
        "a")
    store.set("d",
              "4")
    assert store.get("a") == "1"
    assert store.get("b") is None
    assert store.get("c") == "3"
    assert store.get("d") == "4"