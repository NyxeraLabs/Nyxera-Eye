from threading import Thread

from nyxera_eye.api.ops_runtime import OpsRuntimeStore


def test_ops_runtime_store_initial_scan_completes_without_deadlock() -> None:
    result: dict[str, dict] = {}

    def _build_store() -> None:
        result["snapshot"] = OpsRuntimeStore().snapshot()

    thread = Thread(target=_build_store, daemon=True)
    thread.start()
    thread.join(timeout=2.0)

    assert not thread.is_alive()
    assert result["snapshot"]["metrics"]["scan_runs"] == 1
    assert len(result["snapshot"]["metrics"]["scan_history"]) == 1


def test_ops_runtime_run_scan_returns_snapshot() -> None:
    store = OpsRuntimeStore()

    snapshot = store.run_scan(batch_size=8)

    assert snapshot["metrics"]["scan_runs"] == 2
    assert len(snapshot["devices"]) == 8
    assert len(snapshot["metrics"]["scan_history"]) == 2
