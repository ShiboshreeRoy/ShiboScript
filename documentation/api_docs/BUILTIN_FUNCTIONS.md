# ShiboScript Built-in Functions API Documentation

This document details all the built-in functions available in ShiboScript.

## Table of Contents
1. [Basic Functions](#basic-functions)
2. [Mathematical Functions](#mathematical-functions)
3. [String Functions](#string-functions)
4. [List Functions](#list-functions)
5. [Dictionary Functions](#dictionary-functions)
6. [File Operations](#file-operations)
7. [Network Functions](#network-functions)
8. [Cryptographic Functions](#cryptographic-functions)
9. [Date and Time](#date-and-time)
10. [System Functions](#system-functions)
11. [Advanced Data Structures](#advanced-data-structures)
12. [Web Development](#web-development)
13. [Database Functions](#database-functions)
14. [Error Handling](#error-handling)
15. [Logging and Monitoring](#logging-and-monitoring)

## Basic Functions

### `print(value)`
Outputs a value to the console.

**Parameters:**
- `value`: Any value to print

**Returns:** `null`

**Example:**
```javascript
print("Hello, World!")
print(42)
```

### `len(container)`
Returns the length of a container.

**Parameters:**
- `container`: A list, string, dictionary, or other container

**Returns:** `number`

**Example:**
```javascript
var listLen = len([1, 2, 3])  # 3
var strLen = len("hello")      # 5
```

### `type(value)`
Returns the type of a value.

**Parameters:**
- `value`: Any value

**Returns:** `string`

**Example:**
```javascript
var t = type(42)        # "int"
var t2 = type("hello")  # "str"
```

### `str(value)`
Converts a value to a string.

**Parameters:**
- `value`: Any value

**Returns:** `string`

**Example:**
```javascript
var s = str(42)  # "42"
```

### `int(value)`
Converts a value to an integer.

**Parameters:**
- `value`: A number or string representation of a number

**Returns:** `number`

**Example:**
```javascript
var i = int("42")  # 42
```

### `float(value)`
Converts a value to a floating-point number.

**Parameters:**
- `value`: A number or string representation of a number

**Returns:** `number`

**Example:**
```javascript
var f = float("3.14")  # 3.14
```

### `range(start, stop)`
Creates a range of numbers.

**Parameters:**
- `start`: Starting number
- `stop`: Ending number (exclusive)

**Returns:** `list`

**Example:**
```javascript
var nums = range(0, 5)  # [0, 1, 2, 3, 4]
```

### `input()`
Reads user input from the console.

**Parameters:** None

**Returns:** `string`

**Example:**
```javascript
var name = input("Enter your name: ")
```

## Mathematical Functions

### `min(values...)`
Returns the minimum value from a list of values.

**Parameters:** Variable number of values

**Returns:** The smallest value

**Example:**
```javascript
var m = min(1, 5, 3, 9, 2)  # 1
```

### `max(values...)`
Returns the maximum value from a list of values.

**Parameters:** Variable number of values

**Returns:** The largest value

**Example:**
```javascript
var m = max(1, 5, 3, 9, 2)  # 9
```

### `sum(numbers...)`
Returns the sum of a list of numbers.

**Parameters:** Variable number of numbers

**Returns:** `number`

**Example:**
```javascript
var s = sum(1, 2, 3, 4, 5)  # 15
```

### `abs(number)`
Returns the absolute value of a number.

**Parameters:**
- `number`: A number

**Returns:** `number`

**Example:**
```javascript
var a = abs(-5)  # 5
```

### `round(number)`
Rounds a number to the nearest integer.

**Parameters:**
- `number`: A number

**Returns:** `number`

**Example:**
```javascript
var r = round(3.7)  # 4
```

## String Functions

### `upper(string)`
Converts a string to uppercase.

**Parameters:**
- `string`: A string

**Returns:** `string`

**Example:**
```javascript
var u = upper("hello")  # "HELLO"
```

### `lower(string)`
Converts a string to lowercase.

**Parameters:**
- `string`: A string

**Returns:** `string`

**Example:**
```javascript
var l = lower("HELLO")  # "hello"
```

### `split(string, separator?)`
Splits a string into a list.

**Parameters:**
- `string`: A string to split
- `separator`: Separator character (optional, defaults to space)

**Returns:** `list`

**Example:**
```javascript
var words = split("hello world", " ")  # ["hello", "world"]
```

## List Functions

### `append(list, value)`
Adds a value to the end of a list.

**Parameters:**
- `list`: The list to modify
- `value`: Value to add

**Returns:** Modified list

**Example:**
```javascript
var arr = [1, 2, 3]
arr = append(arr, 4)  # [1, 2, 3, 4]
```

### `remove(list, value)`
Removes a value from a list.

**Parameters:**
- `list`: The list to modify
- `value`: Value to remove

**Returns:** Modified list

**Example:**
```javascript
var arr = [1, 2, 3, 2]
arr = remove(arr, 2)  # [1, 3, 2] - removes first occurrence
```

### `pop(list, index?)`
Removes and returns an element at the given index.

**Parameters:**
- `list`: The list to modify
- `index`: Index of element to remove (optional, defaults to last)

**Returns:** Removed element

**Example:**
```javascript
var arr = [1, 2, 3]
var last = pop(arr)     # 3, arr becomes [1, 2]
var first = pop(arr, 0) # 1, arr becomes [2]
```

### `sort(list)`
Sorts a list in ascending order.

**Parameters:**
- `list`: The list to sort

**Returns:** Sorted list

**Example:**
```javascript
var sorted = sort([3, 1, 4, 1, 5])  # [1, 1, 3, 4, 5]
```

### `reverse(list)`
Reverses a list.

**Parameters:**
- `list`: The list to reverse

**Returns:** Reversed list

**Example:**
```javascript
var reversed = reverse([1, 2, 3])  # [3, 2, 1]
```

## Dictionary Functions

### `keys(dictionary)`
Returns a list of keys from a dictionary.

**Parameters:**
- `dictionary`: The dictionary

**Returns:** `list`

**Example:**
```javascript
var d = {"a": 1, "b": 2}
var k = keys(d)  # ["a", "b"]
```

### `values(dictionary)`
Returns a list of values from a dictionary.

**Parameters:**
- `dictionary`: The dictionary

**Returns:** `list`

**Example:**
```javascript
var d = {"a": 1, "b": 2}
var v = values(d)  # [1, 2]
```

### `items(dictionary)`
Returns a list of key-value pairs from a dictionary.

**Parameters:**
- `dictionary`: The dictionary

**Returns:** `list` of tuples

**Example:**
```javascript
var d = {"a": 1, "b": 2}
var i = items(d)  # [("a", 1), ("b", 2)]
```

### `get(dictionary, key, default?)`
Returns the value for a key, or a default value if the key doesn't exist.

**Parameters:**
- `dictionary`: The dictionary
- `key`: The key to look up
- `default`: Default value if key doesn't exist (optional)

**Returns:** Value or default

**Example:**
```javascript
var d = {"a": 1, "b": 2}
var val = get(d, "a")        # 1
var missing = get(d, "c", 0) # 0
```

## File Operations

### `file.read(path)`
Reads the contents of a file.

**Parameters:**
- `path`: Path to the file

**Returns:** `string`

**Example:**
```javascript
var content = file.read("data.txt")
```

### `file.write(path, content)`
Writes content to a file.

**Parameters:**
- `path`: Path to the file
- `content`: Content to write

**Returns:** `null`

**Example:**
```javascript
file.write("output.txt", "Hello, File!")
```

## Network Functions

### `net.http_get(url, headers?, params?)`
Makes an HTTP GET request.

**Parameters:**
- `url`: URL to request
- `headers`: Request headers (optional)
- `params`: Query parameters (optional)

**Returns:** Response object

**Example:**
```javascript
var response = net.http_get("https://api.example.com/data")
```

### `net.http_post(url, data, headers?)`
Makes an HTTP POST request.

**Parameters:**
- `url`: URL to request
- `data`: Data to send
- `headers`: Request headers (optional)

**Returns:** Response object

**Example:**
```javascript
var response = net.http_post("https://api.example.com/users", {"name": "John"})
```

## Cryptographic Functions

### `crypto.sha256(data)`
Computes the SHA-256 hash of data.

**Parameters:**
- `data`: Data to hash

**Returns:** Hash string

**Example:**
```javascript
var hash = crypto.sha256("hello world")
```

## Date and Time

### `time.now()`
Returns the current timestamp.

**Parameters:** None

**Returns:** `number`

**Example:**
```javascript
var timestamp = time.now()
```

### `time.sleep(seconds)`
Pauses execution for the specified number of seconds.

**Parameters:**
- `seconds`: Number of seconds to pause

**Returns:** `null`

**Example:**
```javascript
time.sleep(1)  # Pause for 1 second
```

## System Functions

### `os.get_cwd()`
Returns the current working directory.

**Parameters:** None

**Returns:** `string`

**Example:**
```javascript
var cwd = os.get_cwd()
```

### `os.exists(path)`
Checks if a file or directory exists.

**Parameters:**
- `path`: Path to check

**Returns:** `boolean`

**Example:**
```javascript
var exists = os.exists("some_file.txt")
```

### `os.list_dir(path)`
Lists the contents of a directory.

**Parameters:**
- `path`: Directory path

**Returns:** `list`

**Example:**
```javascript
var files = os.list_dir(".")
```

## Advanced Data Structures

### `Set(initial_elements?)`
Creates a new Set.

**Parameters:**
- `initial_elements`: Initial elements (optional)

**Returns:** Set instance

**Example:**
```javascript
var mySet = Set([1, 2, 3])
mySet.add(4)
```

### `Queue()`
Creates a new Queue.

**Parameters:** None

**Returns:** Queue instance

**Example:**
```javascript
var queue = Queue()
queue.enqueue("first")
queue.enqueue("second")
var item = queue.dequeue()  # "first"
```

### `Stack()`
Creates a new Stack.

**Parameters:** None

**Returns:** Stack instance

**Example:**
```javascript
var stack = Stack()
stack.push("top")
stack.push("bottom")
var item = stack.pop()  # "top"
```

### `PriorityQueue()`
Creates a new Priority Queue.

**Parameters:** None

**Returns:** Priority Queue instance

**Example:**
```javascript
var pq = PriorityQueue()
pq.enqueue("low", 1)
pq.enqueue("high", 10)
var item = pq.dequeue()  # "high"
```

## Web Development

### `web.create_web_server(port)`
Creates a new web server.

**Parameters:**
- `port`: Port number

**Returns:** Server instance

**Example:**
```javascript
var server = web.create_web_server(8080)
```

### `web.add_route(server, path, method, handler)`
Adds a route to a web server.

**Parameters:**
- `server`: Server instance
- `path`: Route path
- `method`: HTTP method
- `handler`: Handler function

**Returns:** Server instance

**Example:**
```javascript
web.add_route(server, "/api/users", "GET", handler_function)
```

### `web.create_api_response(status, data, message?)`
Creates an API response.

**Parameters:**
- `status`: Response status
- `data`: Response data
- `message`: Response message (optional)

**Returns:** Response object

**Example:**
```javascript
var response = web.create_api_response("success", {"users": []})
```

### `web.jwt_encode(payload, secret)`
Encodes a JWT token.

**Parameters:**
- `payload`: Data to encode
- `secret`: Secret key

**Returns:** Encoded token

**Example:**
```javascript
var token = web.jwt_encode({"user_id": 123}, "secret_key")
```

### `web.jwt_decode(token, secret)`
Decodes a JWT token.

**Parameters:**
- `token`: Encoded token
- `secret`: Secret key

**Returns:** Decoded payload or null

**Example:**
```javascript
var payload = web.jwt_decode(token, "secret_key")
```

## Database Functions

### `create_database(path)`
Creates a database connection.

**Parameters:**
- `path`: Database path

**Returns:** Database instance

**Example:**
```javascript
var db = create_database(":memory:")
```

### `create_model(db, table_name, schema)`
Creates a model for database operations.

**Parameters:**
- `db`: Database instance
- `table_name`: Name of the table
- `schema`: Schema definition

**Returns:** Model instance

**Example:**
```javascript
var User = create_model(db, "users", {
    "id": "INTEGER PRIMARY KEY",
    "name": "TEXT NOT NULL"
})
```

## Error Handling

### `try_catch(try_func, catch_func?, finally_func?)`
Executes a function with error handling.

**Parameters:**
- `try_func`: Function to try
- `catch_func`: Function to call on error (optional)
- `finally_func`: Function to call finally (optional)

**Returns:** Result of try function or caught error

**Example:**
```javascript
try_catch(
    func() { return risky_operation() },
    func(error) { print("Error: " + error) }
)
```

### `assert(condition, message?)`
Asserts that a condition is true.

**Parameters:**
- `condition`: Condition to test
- `message`: Error message if assertion fails (optional)

**Returns:** `null`

**Example:**
```javascript
assert(x > 0, "x must be positive")
```

## Logging and Monitoring

### `create_logger(name, level?)`
Creates a logger instance.

**Parameters:**
- `name`: Logger name
- `level`: Log level (optional, default "INFO")

**Returns:** Logger instance

**Example:**
```javascript
var logger = create_logger("MyApp", "DEBUG")
```

### `log_debug(message)`
Logs a debug message.

**Parameters:**
- `message`: Message to log

**Returns:** `null`

**Example:**
```javascript
log_debug("Debugging information")
```

### `log_info(message)`
Logs an info message.

**Parameters:**
- `message`: Message to log

**Returns:** `null`

**Example:**
```javascript
log_info("Application started")
```

### `log_warn(message)`
Logs a warning message.

**Parameters:**
- `message`: Message to log

**Returns:** `null`

**Example:**
```javascript
log_warn("Deprecated function called")
```

### `log_error(message)`
Logs an error message.

**Parameters:**
- `message`: Message to log

**Returns:** `null`

**Example:**
```javascript
log_error("An error occurred")
```

### `metric_increment(name, value?)`
Increments a metric.

**Parameters:**
- `name`: Metric name
- `value`: Value to increment by (optional, default 1)

**Returns:** New metric value

**Example:**
```javascript
metric_increment("requests_processed")
```

### `metric_get(name, default?)`
Gets a metric value.

**Parameters:**
- `name`: Metric name
- `default`: Default value if metric doesn't exist (optional)

**Returns:** Metric value

**Example:**
```javascript
var count = metric_get("requests_processed", 0)
```
