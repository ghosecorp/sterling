# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- C/Go rewrite for enhanced performance
- Clustering support for distributed caching
- Additional data types (lists, sets, sorted sets, hashes)
- Pub/Sub messaging support
- Master-slave replication

## [0.1.0] - 2025-11-25

### Added
- Initial release of Sterling Cache Server
- Basic key-value operations (GET, SET, DEL, EXISTS)
- TTL expiration support (EXPIRE, TTL commands)
- RDB (snapshot) persistence mode
- AOF (append-only file) persistence mode
- Async multi-client support via asyncio
- Memory management with configurable maxmemory
- LRU eviction policy
- Flexible logging (console or file)
- Thread-safe operations with async locks
- KEYS command for listing all keys
- Automatic persistence on write operations

### Features
- Python 3.8+ support
- Zero external dependencies (stdlib only)
- Configurable host and port
- Fresh or append log modes

### Known Limitations
- No hash, list, set, or sorted set support yet
- No pub/sub functionality
- Single-node only (no clustering)
- Basic eviction policies only

## [0.0.1] - 2025-11-20

### Added
- Project structure initialization
- Basic cache implementation
- Initial server framework

---

[Unreleased]: https://github.com/ghosecorp/sterling/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ghosecorp/sterling/releases/tag/v0.1.0
[0.0.1]: https://github.com/ghosecorp/sterling/releases/tag/v0.0.1