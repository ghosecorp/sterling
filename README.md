# Sterling Server

A high-performance, in-memory cache server written in Python with persistence support and multi-client capability.

[![PyPI version](https://badge.fury.io/py/sterling-server.svg)](https://badge.fury.io/py/sterling-server)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **In-Memory Data Store**: Fast key-value storage with O(1) access time
- **Persistence Options**: 
  - RDB (Database) snapshotting
  - AOF (Append-Only File) logging
- **Multi-Client Support**: Handle concurrent connections via asyncio
- **Memory Management**: 
  - Configurable `maxmemory` limits
  - LRU eviction policy support
- **TTL Expiration**: Automatic key expiration with time-to-live
- **Flexible Logging**: Console or file-based logging with append/fresh modes
- **Thread-Safe Operations**: Async locks for concurrent access

## Installation

### Via PyPI

```
pip install sterling-server
```

### Via TestPyPI

```
pip install -i https://test.pypi.org/simple/ sterling-server
```

### From Source

```
git clone https://github.com/ghosecorp/sterling.git
cd sterling
pip install -e .
```

## Quick Start

### Basic Usage

```
from sterling_server import SterlingServer

# Create server with default settings
server = SterlingServer()
server.run()
```

### Advanced Configuration

```
from sterling_server import SterlingServer

server = SterlingServer(
    host='0.0.0.0',              # Listen on all interfaces
    port=9162,                    # Custom port
    persistence_mode='RDB',       # 'RDB' or 'AOF'
    maxmemory=10000,              # Max keys before eviction
    eviction_policy='lru',        # 'lru', 'allkeys-lru', or 'noeviction'
    log_to_file=True,             # Enable file logging
    log_file_path='log/sterling.log',
    fresh_logs=False              # Append to existing logs
)

server.run()
```

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | str | `'localhost'` | Server bind address |
| `port` | int | `9162` | Server port |
| `persistence_mode` | str | `'RDB'` | Persistence strategy (`RDB` or `AOF`) |
| `maxmemory` | int | `None` | Maximum keys in memory (None = unlimited) |
| `eviction_policy` | str | `'noeviction'` | How to handle memory limits |
| `log_to_file` | bool | `False` | Log to file instead of console |
| `log_file_path` | str | `None` | Custom log file path (default: `log/server_logs.log`) |
| `fresh_logs` | bool | `False` | Start with fresh log file (True) or append (False) |

## Persistence Strategies

### RDB (Snapshot)
- Affects: ✅ Disk only
- Periodic snapshots of entire dataset
- Fast recovery, potential minor data loss
- Best for: Speed and simplicity

### AOF (Append-Only File)
- Affects: ✅ Disk only
- Logs every write operation
- Maximum durability, larger files
- Best for: Critical data requiring minimal loss

## Memory Management

| Feature | Affects RAM? | Affects Disk? | Purpose |
|---------|-------------|---------------|---------|
| Persistence (RDB/AOF) | ❌ | ✅ | Recovery after restart |
| maxmemory | ✅ | ❌ | Limit RAM usage |
| Eviction policy | ✅ | ❌ | Auto-delete old keys |
| TTL expiration | ✅ | ❌ | Auto-delete expired data |

## Examples

See the [examples/](examples/) directory for complete examples:
- `basic_server.py` - Minimal server setup
- `production_server.py` - Production configuration with logging
- `custom_persistence.py` - Different persistence strategies

## Future Development

**Performance Roadmap**: Sterling Server will be gradually rewritten in **C** or **Go** (decision pending) to unlock:
- Hardware-level optimizations
- Native system integration
- Enhanced performance characteristics
- Advanced memory management

**Commitment**: We will continue maintaining and actively developing the Python version, incorporating features from the C/Go implementation whenever possible. The Python server remains our primary focus for users who prefer Python integration and ease of deployment.

## Documentation

Full documentation available at: [https://github.com/ghosecorp/sterling/blob/main/README.md](https://github.com/ghosecorp/sterling/blob/main/README.md)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/ghosecorp/sterling/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ghosecorp/sterling/discussions)
- **Email**: ghosecorp@gmail.com

## Related Projects

- [sterling](https://github.com/ghosecorp/sterling-python-client) - Python client library
- Sterling clients for other languages (coming soon)

---

**Built with ❤️ by Ghosecorp**

