# Advanced ShiboScript Features for Real-World Applications

This document describes the advanced features added to ShiboScript to make it suitable for real-world applications and enterprise use.

## Table of Contents
1. [Database Operations](#database-operations)
2. [Logging System](#logging-system)
3. [File System Utilities](#file-system-utilities)
4. [Network Utilities](#network-utilities)
5. [Security Functions](#security-functions)
6. [Threading and Concurrency](#threading-and-concurrency)
7. [System Information](#system-information)
8. [UUID Generation](#uuid-generation)
9. [Date/Time Utilities](#datetime-utilities)
10. [Queue Operations](#queue-operations)
11. [Advanced Math Functions](#advanced-math-functions)
12. [Enhanced Collections](#enhanced-collections)

## Database Operations

ShiboScript now includes SQLite database support for persistent data storage.

### Usage
```javascript
// Connect to database
var db_conn = db.connect("example.db");

// Execute queries
db.execute(db_conn, "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)");
db.execute(db_conn, "INSERT INTO users (name, email) VALUES (?, ?)", ["John Doe", "john@example.com"]);

// Fetch data
var users = db.fetch_all(db_conn, "SELECT * FROM users");
```

## Logging System

Professional logging capabilities for application monitoring and debugging.

### Usage
```javascript
// Setup logger
logging.setup("app", "app.log");

// Log messages
logging.info("Application started");
logging.warning("This is a warning");
logging.error("This is an error");
```

## File System Utilities

Comprehensive file system operations for real-world applications.

### Usage
```javascript
// Directory operations
fs.mkdir("new_directory");
fs.rmdir("directory_to_remove");

// File operations
var exists = fs.file_exists("some_file.txt");
var size = fs.file_size("file.txt");
var files = fs.list_files("/path/to/directory");

// File content operations
var lines = fs.read_lines("file.txt");
fs.write_lines("output.txt", ["line1", "line2"]);
fs.append_to_file("log.txt", "Additional log entry");
```

## Network Utilities

Network connectivity and diagnostics functions.

### Usage
```javascript
// Check host availability
var is_up = network.ping_host("google.com");

// Check port availability
var is_open = network.check_port("localhost", 8080);

// Get IP address
var ip = network.get_ip_address("google.com");
```

## Security Functions

Cryptographic and security-related utilities.

### Usage
```javascript
// Password management
var password = security.generate_password(16);
var hashed = security.hash_password("my_password");
var is_valid = security.verify_password("my_password", hashed);

// Encryption
var encrypted_data, key = security.encrypt_data("Secret message", null);
var decrypted_data = security.decrypt_data(encrypted_data, key);

// JWT tokens
var token = security.generate_jwt({"user_id": 123}, "secret_key");
var decoded = security.verify_jwt(token, "secret_key");
```

## Threading and Concurrency

Multi-threading support for concurrent operations.

### Usage
```javascript
// Thread pool execution
func slow_operation(x) {
    time.sleep(1);  // Sleep for 1 second
    return x * x;
}

var items = [1, 2, 3, 4, 5];
var results = threading.pool_execute(slow_operation, items, 3);
```

## System Information

Access to system metrics and information.

### Usage
```javascript
// System metrics
var cpu_usage = system.get_cpu_percent();
var mem_info = system.get_memory_info();
var disk_usage = system.get_disk_usage("/");
var sys_info = system.get_system_info();
```

## UUID Generation

Universally unique identifier generation.

### Usage
```javascript
var uuid1 = uuid.generate();   // Random UUID
var uuid2 = uuid.generate1();  // MAC address and timestamp based
var uuid3 = uuid.generate4();  // Random UUID (alias for generate)
```

## Date/Time Utilities

Enhanced date and time operations.

### Usage
```javascript
// Timestamp operations
var timestamp = datetime_utils.get_timestamp();
var formatted = datetime_utils.format_datetime("%Y-%m-%d %H:%M:%S");
var parsed = datetime_utils.parse_datetime("2023-01-01 12:00:00", "%Y-%m-%d %H:%M:%S");

// Time arithmetic
var future_time = datetime_utils.add_time(datetime.now(), days=7);
var time_diff = datetime_utils.diff_time(time1, time2);
```

## Queue Operations

Thread-safe queue operations for concurrent programming.

### Usage
```javascript
// Create and use queue
var q = queue.create(10);  // Max size of 10
queue.put(q, "first_item");
queue.put(q, "second_item");
var item = queue.get(q);  // Gets "first_item"
```

## Advanced Math Functions

Extended mathematical operations beyond basic arithmetic.

### Usage
```javascript
// Advanced math functions
var fact = math.factorial(5);
var log_val = math.log(10);
var ceil_val = math.ceil(3.7);
var floor_val = math.floor(3.7);
```

## Enhanced Collections

Additional collection operations and iterators.

### Usage
```javascript
// Filter and map operations
var numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
var evens = filter(func(x) { return x % 2 == 0; }, numbers);
var doubled = map(func(x) { return x * 2; }, numbers);

// Other collection functions
var enumerated = enumerate(["a", "b", "c"]);  // [(0, "a"), (1, "b"), (2, "c")]
var reversed_list = reversed([1, 2, 3]);       // [3, 2, 1]
var sorted_list = sorted([3, 1, 2]);          // [1, 2, 3]
```

## Running Advanced Scripts

To run scripts that use advanced features:

```bash
# Using the advanced interpreter
python advanced_shiboscript.py advanced_script.shibo

# Or in the REPL
python advanced_shiboscript.py
```

## Best Practices

1. **Error Handling**: Always wrap database operations in try-catch blocks
2. **Resource Management**: Close database connections when done
3. **Security**: Use the security functions for sensitive operations
4. **Logging**: Implement comprehensive logging for production applications
5. **Performance**: Use threading functions judiciously to avoid race conditions