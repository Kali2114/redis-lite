# Design

This doc tracks scope, architecture decisions, and the milestone plan. Update it
as you go — especially the Decisions Log, whenever you make a choice you might
later forget the reasoning for.

## Scope

<!-- TODO: What will this server support, at minimum, to call step N "done"?
     Be concrete: which commands, single-client or multi-client, in-memory
     only or persisted to disk? Nail down what's explicitly OUT of scope too
     (e.g. "no pub/sub for now", "no clustering", "no auth"). -->

## Data model

<!-- TODO: What value types does a key hold — just strings, or also lists/
     hashes/sets like real Redis? Is there a TTL/expiry concept? -->

## Protocol

<!-- TODO: How does a client talk to the server over the socket? Options to
     consider (write down why you picked one): a simplified text protocol
     you design yourself, or Redis's real RESP protocol. Each has different
     tradeoffs for how much you learn about wire-protocol design vs. how
     much prior art you can lean on. -->

## Architecture

<!-- TODO: Once you have a few pieces, sketch how they call each other.
     e.g. "TCP server accepts connections -> per-connection loop reads a
     command -> command dispatched to the in-memory store -> response
     written back over the socket". A rough diagram or a few bullet points
     is enough. -->

## Milestones

1. **Single-client TCP server** — plain socket server, one client at a time.
   - Done when: a client can connect and issue `GET`/`SET`/`DEL` against an
     in-memory dict, and get a response back over the same connection.
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

- YYYY-MM-DD: <!-- decision --> — because <!-- reasoning -->

## Open questions

- Protocol design: not yet decided (see Protocol section above).
- Concurrency model: threads vs. `asyncio` — not yet decided (see milestone 3).