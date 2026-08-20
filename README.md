# redis-lite

A minimal Redis-like in-memory key-value server, built from scratch in pure
Python, as a learning project to understand networking, protocol design, and
concurrency (as opposed to using a framework or an existing client library).

## Status

Milestones 1–3 done: a server (`Server` + `Store` + `Connection`) handling
`GET`/`SET`/`DEL` over a custom text protocol with explicit length-prefixed
values (so a value can contain spaces or newlines), serving multiple
clients concurrently on their own threads with a locked `Store`. Covered
by a pytest suite, including a value with an embedded newline and a test
proving an idle client doesn't stall another client's request. See
[DESIGN.md](DESIGN.md) for what's next.

## Why

<!-- TODO: one or two sentences, in your own words, on what you want to get
     out of this project. What do you not understand today that you want to
     understand by the end? -->

## Usage

Start the server:

```python
from server import Server
from store import Store

Server("127.0.0.1", 6380, Store()).start()
```

Talk to it with a raw TCP client. Requests/responses are `\r\n`-terminated
lines; `SET`'s value and an existing `GET`'s value are length-prefixed so
they can contain arbitrary bytes:

```python
import socket

with socket.create_connection(("127.0.0.1", 6380)) as s:
    s.sendall(b"SET name 5\r\nkamil\r\n")
    print(s.recv(1024))  # b'OK\n'

with socket.create_connection(("127.0.0.1", 6380)) as s:
    s.sendall(b"GET name\r\n")
    print(s.recv(1024))  # b'5\r\nkamil'

with socket.create_connection(("127.0.0.1", 6380)) as s:
    s.sendall(b"DEL name\r\n")
    print(s.recv(1024))  # b'1\n'
```

Run the tests:

```
pip install pytest
python -m pytest
```

## Roadmap

See [DESIGN.md](DESIGN.md) for the milestone plan and design decisions.