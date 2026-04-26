from helix.event_bus import EventBus, FileQueued

def test_event_bus():
    bus = EventBus()
    received = []

    def handler(event):
        received.append(event)

    bus.subscribe(FileQueued, handler)
    event = FileQueued(path="/foo.pdf")
    bus.publish(event)

    assert len(received) == 1
    assert received[0].path == "/foo.pdf"
