from unittest.mock import patch

from listen import _is_valid_phrase, _pick_microphone_index


@patch("speech_recognition.Microphone.list_microphone_names")
def test_pick_bt_microphone_prefers_bluetooth(mock_list):
    mock_list.return_value = [
        "Default Microphone",
        "Bluetooth Hands-Free AG Audio",
        "USB Audio Device",
    ]

    assert _pick_microphone_index() == 1


def test_valid_phrase_filter_rejects_noise():
    assert not _is_valid_phrase("daru")
    assert _is_valid_phrase("sleep")
    assert _is_valid_phrase("hey jarvis")
    assert _is_valid_phrase("please show me my desktop")
