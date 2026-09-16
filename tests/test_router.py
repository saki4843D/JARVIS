import commands.router as router


def test_help_is_available_without_ai():
    response, should_exit = router.handle("help")
    assert "open apps" in response
    assert should_exit is False


def test_shutdown_requires_explicit_confirmation(monkeypatch):
    called = []
    monkeypatch.setattr(router, "shutdown", lambda: called.append(True) or "Shutting down.")
    response, should_exit = router.handle("shutdown computer")
    assert "Say yes" in response
    assert should_exit is False
    assert called == []

    response, should_exit = router.handle("yes")
    assert response == "Shutting down."
    assert should_exit is False
    assert called == [True]


def test_power_action_can_be_cancelled():
    router.handle("restart computer")
    response, should_exit = router.handle("cancel")
    assert response.startswith("Cancelled")
    assert should_exit is False


def test_file_deletion_requires_confirmation(tmp_path, monkeypatch):
    target = tmp_path / "temporary.txt"
    target.write_text("test", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    response, should_exit = router.handle("delete file temporary.txt")
    assert "confirm" in response.lower()
    assert should_exit is False
    assert target.exists()
    response, should_exit = router.handle("cancel")
    assert "not deleted" in response.lower()
    assert target.exists()


def test_simple_workflow_runs_each_step(monkeypatch):
    opened = []
    monkeypatch.setattr(router, "open_app", lambda name: opened.append(name) or True)
    response, should_exit = router.handle("open notepad and open calculator")
    assert "Opening notepad." in response
    assert "Opening calculator." in response
    assert opened == ["notepad", "calculator"]
