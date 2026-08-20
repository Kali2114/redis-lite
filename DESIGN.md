# Design

This doc tracks scope, architecture decisions, and the milestone plan. Update it
as you go — especially the Decisions Log, whenever you make a choice you might
later forget the reasoning for.

## Scope

In scope, minimum to call this "done":
- Commands: `GET`, `SET`, `DEL` (plus `EXISTS` if convenient) against an
  in-memory string store.
- Single client first (milestone 1), then multiple concurrent clients
  (milestone 3).
- A custom text protocol with unambiguous framing (milestone 2).
- LRU eviction with a max store size (milestone 4).
- In-memory only; disk persistence is a stretch goal (milestone 5), not
  required for "done".

Out of scope for now (may revisit later):
- TTL/expiry on keys.
- Non-string value types (lists, hashes, sets).
- Auth, pub/sub, transactions, clustering/replication.

## Data model

- Keys and values are both strings (utf-8 bytes). No other value types for
  now — real Redis's lists/hashes/sets are a possible future extension once
  the core server works.
- No TTL/expiry for now. Adding it later is a natural extension: a
  background sweep or lazy-check-on-read against a stored expiry timestamp.

## Protocol

Decision: a custom text protocol, not RESP. Goal is to learn wire-protocol
design by making the framing decisions myself, rather than implementing an
existing spec.

Framing plan (staged across milestones, so early framing bugs are cheap to
hit and fix):
- Milestone 1: one command per line, fields space-separated
  (`SET key value\n`, `GET key\n`, `DEL key\n`). Simplest possible framing;
  known limitation is that values can't contain spaces or newlines yet.
- Milestone 2: replace the naive line format with explicit length-prefixed
  values (e.g. `SET key <byte-length>\r\n<raw bytes>\r\n`) so a value can
  contain arbitrary bytes, including spaces and newlines, without ambiguity.
  This is the point of milestone 2: framing that doesn't rely on
  newline-splitting alone.

## Architecture

Decision: object-oriented design — classes rather than free functions
operating on a plain dict. A natural split for milestone 1:
- `Store` — owns the in-memory dict, exposes `get`/`set`/`delete`.
- `Server` (or `Connection`/`ClientHandler`) — owns the socket, the
  accept/read loop, and command parsing, and holds a reference to a `Store`.

Rough flow stays the same: TCP server accepts a connection -> per-connection
loop reads bytes into a buffer and splits on newlines to find complete
commands -> each command is dispatched against the `Store` -> response
written back over the same connection. Once milestone 3 adds concurrent
clients, the `Store` (not the connection-handling classes) is where
thread-safety needs to be addressed, since it's the shared state multiple
handlers will touch at once.

## Milestones

1. **Single-client TCP server** — plain socket server, one client at a time.
   - Done when: a client can connect and issue `GET`/`SET`/`DEL` against an
     in-memory dict, and get a response back over the same connection.
   - Status: done — `Store` (store.py) and `Server` (server.py), covered by
     the pytest suite in `tests/` (GET/SET/DEL, unknown and empty commands).
2. **Custom text protocol** — define and parse your own command protocol
   (a simplified version of Redis's RESP is fine).
   - Done when: commands and responses are framed unambiguously (the parser
     knows where one command/response ends and the next begins) rather than
     relying on newline-splitting alone.
3. **Concurrent clients** — handle multiple simultaneous connections
   (threads or `asyncio`).
   - Done when: two clients connected at once can both `SET`/`GET` without
     one blocking or corrupting the other's view of the store.
4. **LRU eviction** — cap the store at a max size, evict least-recently-used
   keys when full.
   - Done when: you've benchmarked/tested that inserting past the cap evicts
     the correct key, and can explain the data structure choice (e.g. dict +
     doubly linked list vs. `OrderedDict`) and its complexity.
5. **(Stretch) Persistence** — snapshot the in-memory store to disk and
   reload it on restart, so a process crash doesn't lose all data.

## Decisions log

<!-- Add an entry each time you make a non-obvious choice. Keep entries short. -->

- 2026-08-18: Custom text protocol, not RESP — because the goal is to
  practice wire-protocol design decisions myself rather than implement an
  existing spec.
- 2026-08-18: Strings-only data model, no TTL at start — because getting
  the server/protocol/concurrency mechanics solid first matters more than
  breadth of features; richer types and expiry are natural extensions once
  the core loop works.
- 2026-08-18: Object-oriented architecture (`Store`, `Server`/connection
  classes) rather than free functions on a plain dict — user's preference
  for how to organize the codebase as it grows across milestones.

## Open questions

- Concurrency model: threads vs. `asyncio` — not yet decided (see milestone 3).