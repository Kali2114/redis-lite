# redis-lite

A minimal Redis-like in-memory key-value server, built from scratch in pure
Python, as a learning project to understand networking, protocol design, and
concurrency (as opposed to using a framework or an existing client library).

## Status

Milestone 1 done: a single-client server (`Server` + `Store`) handling
`GET`/`SET`/`DEL` over a plain newline-delimited protocol, with a pytest
suite covering the happy paths plus unknown/empty commands. See
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

Talk to it with any raw TCP client, one command per line:

```
$ nc 127.0.0.1 6380
SET name kamil
OK
GET name
kamil
DEL name
1
```

Run the tests:

```
pip install pytest
python -m pytest
```

## Roadmap

See [DESIGN.md](DESIGN.md) for the milestone plan and design decisions.