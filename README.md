# ShiboScript 🐕 - Professional Edition

A powerful, Python-like scripting language with advanced features designed for learning programming concepts, rapid prototyping, and real-world applications. Features a complete compiler architecture with bytecode generation and optimization.

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Language Features](#language-features)
5. [Development](#development)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)
9. [Author](#author)

## Features

- **Real-World Compiler**: Complete compiler with bytecode generation and optimization passes
- **Python-like Syntax**: Familiar syntax with advanced language constructs
- **Object-Oriented**: Full support for classes, inheritance, and interfaces
- **Built-in Libraries**: Rich set of built-in functions for file I/O, networking, cryptography, and more
- **Interactive REPL**: Built-in read-eval-print loop for experimentation
- **Cross-Platform**: Runs on Windows, macOS, and Linux
- **Advanced Data Structures**: Includes sets, queues, stacks, and priority queues
- **Web Development**: Built-in web server capabilities and HTTP functions
- **Database ORM**: Object-relational mapping for SQLite databases
- **Functional Programming**: Map, filter, reduce, and other functional utilities
- **Asynchronous Programming**: Support for async/await patterns
- **Error Handling**: Comprehensive exception handling with try/catch
- **Logging and Monitoring**: Built-in logging and metrics collection
- **Standard Library**: Extensive standard library with web, crypto, date/time, JSON, and regex functions
- **Command-Line Compiler**: Dedicated compiler tool (`shiboc`) for compilation to Python or bytecode

## Installation

### Prerequisites

- Python 3.8+ (required)
- Pip package manager
- Pillow (for image processing)

### Installing on Different Platforms

#### Linux/macOS

```bash
# Clone the repository
git clone https://github.com/ShiboShreeRoy/ShiboScript.git
cd ShiboScript

# Install dependencies
pip install -e .
```

#### Windows

```cmd
# Clone the repository
git clone https://github.com/ShiboShreeRoy/ShiboScript.git
cd ShiboScript

# Install dependencies
pip install -e .
```

#### Termux (Android)

```bash
# Update package list
pkg update && pkg upgrade

# Install Python and Git
pkg install python git

# Clone the repository
git clone https://github.com/ShiboShreeRoy/ShiboScript.git
cd ShiboScript

# Install dependencies
pip install -e .
```

### Quick Installation Methods

#### Using pip directly from GitHub

```bash
pip install git+https://github.com/ShiboShreeRoy/ShiboScript.git
```

#### Using Python's venv (recommended)

```bash
# Create virtual environment
python -m venv shiboscript-env

# Activate virtual environment
# On Linux/macOS:
source shiboscript-env/bin/activate
# On Windows:
shiboscript-env\Scripts\activate

# Install ShiboScript
cd ShiboScript
pip install -e .
```

### Running ShiboScript (Updated Instructions)

#### Method 1: Using the Python Runner (Recommended for this project structure)

Start the interactive REPL:
```bash
python3 run_shiboscript.py
```

Run a script file:
```bash
python3 run_shiboscript.py script.shibo
```

#### Method 2: Using the Installed Version (if installed via pip)

Start the interactive REPL:
```bash
shiboscript
```

Run a script file:
```bash
shiboscript script.shibo
# or
shiboscript run script.shibo
```

#### Command Line Options

- `python3 run_shiboscript.py` - Start interactive REPL (using runner script)
- `python3 run_shiboscript.py file.shibo` - Run a script file (using runner script)
- `shiboscript` - Start interactive REPL (if installed via pip)
- `shiboscript file.shibo` - Run a script file (if installed via pip)
- `shiboscript run file.shibo` - Alternative way to run a script file (if installed via pip)
- `shiboscript --version` - Show version information (if installed via pip)
- `shiboscript --help` - Show help information (if installed via pip)
- `shiboc script.shibo` - Compile script to Python (.py)
- `shiboc -c script.shibo` - Compile to Python (.py)
- `shiboc -b script.shibo` - Compile to bytecode (.sbc)
- `shiboc -r script.shibo` - Run the file directly
- `shiboc -o output.py script.shibo` - Compile to specific output file
- `shiboc --help` - Show help information

### Quick Test

To quickly test if ShiboScript is working, try running the example:

```bash
python3 run_shiboscript.py hello_world.shibo
```

Or start the interactive REPL:

```bash
python3 run_shiboscript.py
```

In the REPL, you can type commands directly:
```
🐕 Welcome to ShiboScript v0.3.0 REPL! Type 'exit' to quit, 'help' for help.
shiboscript>>> print("Hello, World!")
Hello, World!
shiboscript>>> var x = 42
shiboscript>>> print(x)
42
shiboscript>>> exit
```

### Verifying Installation

After installation via pip, you can verify ShiboScript is properly installed by running:

```bash
shiboscript --version
# or
python -c "import shiboscript; print('ShiboScript installed successfully')"
```

If using the project structure without pip installation, simply run:

```bash
python3 run_shiboscript.py
```

## Quick Start

### Using the REPL

Using the Python runner (recommended for this project structure):

```bash
python3 run_shiboscript.py
```

```
🐕 Welcome to ShiboScript v1.0.0 REPL! Type 'exit' to quit, 'help' for help.
shiboscript>>> print("Hello, World!")
Hello, World!
shiboscript>>> var x = 42
shiboscript>>> print(x)
42
```

### Using the Compiler

ShiboScript comes with a dedicated compiler (`shiboc`) that can:
- Compile to Python code
- Generate optimized bytecode
- Run scripts directly

```bash
# Compile to Python
shiboc -c hello.shibo

# Compile to bytecode
shiboc -b hello.shibo

# Run directly
shiboc -r hello.shibo
```

Alternatively, if installed via pip:

```bash
shiboscript
```

### Running Scripts

Create a file `hello.shibo`:

```javascript
func greet(name) {
    print("Hello, " + name + "!")
}

greet("ShiboScript")
```

Run it with the Python runner (recommended for this project structure):

```bash
python3 run_shiboscript.py hello.shibo
```

Or if installed via pip:

```bash
shiboscript hello.shibo
# or
shiboscript run hello.shibo
```

Or compile and run with the dedicated compiler:

```bash
# Compile to Python and run
shiboc -c hello.shibo
python hello.py

# Compile to bytecode
shiboc -b hello.shibo

# Or run directly
shiboc -r hello.shibo
```

## Language Features

### Comments
Comments in ShiboScript start with the `#` symbol:
```javascript
# This is a comment
var x = 42  # This is also a comment
```

### Identifiers
Identifiers must start with a letter or underscore, followed by letters, digits, or underscores:
- Valid: `myVariable`, `_private`, `variable123`
- Invalid: `123var`, `my-variable`, `my variable`

## Data Types

ShiboScript supports several built-in data types:

### Primitive Types
- **Numbers**: Integer and floating-point numbers
  ```javascript
  var integer = 42
  var decimal = 3.14
  ```
  
- **Strings**: Text enclosed in double quotes
  ```javascript
  var greeting = "Hello, World!"
  ```
  
- **Booleans**: Logical values
  ```javascript
  var isTrue = true
  var isFalse = false
  ```
  
- **Null**: Represents no value
  ```javascript
  var nothing = null
  ```

### Collection Types
- **Lists**: Ordered, mutable sequences
  ```javascript
  var numbers = [1, 2, 3, 4, 5]
  var mixed = [1, "hello", true, 3.14]
  ```
  
- **Dictionaries**: Key-value mappings
  ```javascript
  var person = {"name": "Shibo", "type": "Script", "age": 3}
  ```
  
- **Sets**: Unordered collections of unique values
  ```javascript
  var uniqueNumbers = set(1, 2, 3, 2, 1)  # Results in {1, 2, 3}
  ```

## Variables

Variables in ShiboScript are declared using the `var` keyword:

```javascript
var name = "ShiboScript"
var age = 3
var isAwesome = true
var numbers = [1, 2, 3, 4, 5]
var person = {"name": "Shibo", "type": "Script"}
```

Variables are dynamically typed and can hold any value.

## Operators

### Arithmetic Operators
| Operator | Description |
|----------|-------------|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `//` | Floor division |
| `%` | Modulo |
| `++` | Increment |
| `--` | Decrement |

### Comparison Operators
| Operator | Description |
|----------|-------------|
| `==` | Equal to |
| `!=` | Not equal to |
| `<` | Less than |
| `>` | Greater than |
| `<=` | Less than or equal to |
| `>=` | Greater than or equal to |

### Logical Operators
| Operator | Description |
|----------|-------------|
| `&&` | Logical AND |
| `||` | Logical OR |
| `!` | Logical NOT |

### Bitwise Operators
| Operator | Description |
|----------|-------------|
| `&` | Bitwise AND |
| `|` | Bitwise OR |
| `^` | Bitwise XOR |
| `~` | Bitwise NOT |
| `<<` | Left shift |
| `>>` | Right shift |
| `>>>` | Unsigned right shift |

### Assignment Operators
| Operator | Description |
|----------|-------------|
| `=` | Assignment |
| `+=` | Addition assignment |
| `-=` | Subtraction assignment |
| `*=` | Multiplication assignment |
| `/=` | Division assignment |
| `%=` | Modulo assignment |

### Other Operators
- `instanceof`: Check if an object is an instance of a class
- `?:`: Ternary conditional operator

## Control Structures

### Conditional Statements
```javascript
if (x > 10) {
    print("Greater than 10")
} else if (x == 10) {
    print("Equal to 10")
} else {
    print("Less than 10")
}
```

### Loops
#### For Loop (C-style)
```javascript
for (var i = 0; i < 10; i++) {
    print(i)
}
```

#### For-In Loop
```javascript
for (item in items) {
    print(item)
}

for (key in dictionary) {
    print(key + ": " + dictionary[key])
}
```

#### While Loop
```javascript
while (condition) {
    # do something
    condition = false  # to avoid infinite loop
}
```

#### Do-While Loop
```javascript
do {
    print("This runs at least once")
} while (false)
```

### Loop Control
- `break`: Exit the loop immediately
- `continue`: Skip the rest of the current iteration

### Exception Handling
```javascript
try {
    # risky code
    var result = 10 / 0
} catch (error) {
    print("Error occurred: " + error)
}
```

## Functions

Functions are defined using the `func` keyword:

```javascript
func greet(name) {
    print("Hello, " + name + "!")
}

func add(a, b) {
    return a + b
}

# Function call
greet("World")
var sum = add(5, 3)
```

### Recursive Functions
```javascript
func factorial(n) {
    if (n <= 1) {
        return 1
    }
    return n * factorial(n - 1)
}
```

## Classes and OOP

ShiboScript supports full object-oriented programming with classes, inheritance, and interfaces.

### Basic Class Definition
```javascript
class Animal {
    var name
    
    func init(self, name) {
        self.name = name
    }
    
    func speak(self) {
        print("Animal sound")
    }
}
```

### Inheritance
```javascript
class Dog(Animal) {
    func speak(self) {
        print(self.name + " says woof!")
    }
}

var dog = Dog("Buddy")
dog.speak()  # Buddy says woof!
```

### Interfaces
```javascript
interface Drawable {
    func draw()
    func resize(width, height)
}

class Circle implements Drawable {
    var radius
    
    func init(self, radius) {
        self.radius = radius
    }
    
    func draw(self) {
        print("Drawing a circle with radius " + self.radius)
    }
    
    func resize(self, width, height) {
        print("Resizing circle to " + width + "x" + height)
    }
}
```

### Method Access
Methods can access instance properties using `self.property_name`.

## Modules and Imports

### Import Entire Module
```javascript
import math
var result = math.sqrt(16)
```

### Import Specific Items
```javascript
from math import sqrt, pi
var result = sqrt(16)  # Direct access
```

### Import All
```javascript
from math import *
var result = sqrt(16)  # Direct access to all exports
```

## Built-in Functions

### Basic Functions
- `print(value)`: Output a value
- `len(container)`: Get the length of a container
- `type(value)`: Get the type of a value
- `str(value)`: Convert value to string
- `int(value)`: Convert value to integer
- `float(value)`: Convert value to float
- `range(start, stop)`: Create a range of numbers
- `input()`: Read user input

### List Functions
- `append(list, value)`: Add value to end of list
- `remove(list, value)`: Remove value from list
- `pop(list, index?)`: Remove and return element at index
- `sort(list)`: Sort the list
- `reverse(list)`: Reverse the list

### Dictionary Functions
- `keys(dict)`: Get list of keys
- `values(dict)`: Get list of values
- `items(dict)`: Get list of key-value pairs
- `get(dict, key, default?)`: Get value with optional default

### Mathematical Functions
- `min(values...)`: Get minimum value
- `max(values...)`: Get maximum value
- `sum(numbers...)`: Sum all numbers
- `abs(number)`: Absolute value
- `round(number)`: Round to nearest integer

## Standard Library

### Math Module
```javascript
var sqrt = math.sqrt(16)  # 4
var pi = math.pi          # 3.14159...
var result = math.pow(2, 3)  # 8
```

### File Operations
```javascript
var content = file.read("data.txt")
file.write("output.txt", "Hello World")
```

### Network Operations
```javascript
var response = net.http_get("https://api.example.com")
var post_response = net.http_post("https://api.example.com", {"key": "value"})
```

### Cryptography
```javascript
var hash = crypto.sha256("secret")
```

### Image Processing
```javascript
var img = image.load("photo.png")
image.show(img)
```

### Operating System Functions
```javascript
var current_dir = os.get_cwd()
var files = os.list_dir(".")
var exists = os.exists("some_file.txt")
var env_var = os.get_env("HOME")
```

### Random Functions
```javascript
var random_num = random.int(1, 10)
var random_str = random.string(10)
```

### URL and Encoding
```javascript
var encoded = url.encode("hello world")
var decoded = url.decode("hello%20world")
var parsed = url.parse("https://example.com/path?query=value")
```

### Base64 Encoding
```javascript
var encoded = base64.encode("hello")
var decoded = base64.decode(encoded)
```

### JSON Handling
```javascript
var json_str = json.encode({"name": "Shibo", "age": 3})
var obj = json.decode(json_str)
```

### Time Functions
```javascript
var timestamp = time.now()
time.sleep(1)  # Sleep for 1 second
```

### Regular Expressions
```javascript
var matches = re.findall("\\d+", "There are 123 apples and 456 oranges")
```

### Date and Time
```javascript
var now = datetime.now()
var formatted = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
```

## Advanced Features

### Data Structures
ShiboScript includes advanced data structures:

#### Sets
```javascript
var mySet = Set([1, 2, 3, 4])
mySet.add(5)
mySet.remove(2)
var isPresent = mySet.contains(3)
```

#### Queues
```javascript
var queue = Queue()
queue.enqueue("first")
queue.enqueue("second")
var item = queue.dequeue()  # "first"
```

#### Stacks
```javascript
var stack = Stack()
stack.push("top")
stack.push("bottom")
var item = stack.pop()  # "top"
```

#### Priority Queues
```javascript
var pq = PriorityQueue()
pq.enqueue("low", 1)
pq.enqueue("high", 10)
var item = pq.dequeue()  # "high" (higher priority)
```

### Functional Programming
```javascript
var numbers = [1, 2, 3, 4, 5]
var doubled = map(n => n * 2, numbers)
var evens = filter(n => n % 2 == 0, numbers)
var sum = reduce((acc, n) => acc + n, numbers, 0)
```

### Advanced Algorithms
```javascript
var sorted = quick_sort([3, 1, 4, 1, 5, 9, 2, 6])
var index = binary_search([1, 2, 3, 4, 5], 3)  # Returns index or -1
```

### Web Development
```javascript
var server = web.create_web_server(8080)
web.add_route(server, "/api/users", "GET", handler_function)
var response = web.create_api_response("success", {"users": []})
```

### Database ORM
```javascript
var db = create_database(":memory:")
var User = create_model(db, "users", {
    "id": "INTEGER PRIMARY KEY",
    "name": "TEXT NOT NULL",
    "email": "TEXT UNIQUE"
})

var user = User.create({"name": "John", "email": "john@example.com"})
var users = User.find()
```

### Error Handling
```javascript
try {
    # risky operations
} catch (error) {
    log_error("Operation failed: " + error)
}
```

### Logging and Monitoring
```javascript
var logger = create_logger("MyApp", "INFO")
logger.info("Application started")
logger.error("Something went wrong")

# Metrics
metric_increment("requests_processed", 1)
var current_count = metric_get("requests_processed")
```

### JWT Authentication
```javascript
var payload = {"user_id": 123, "exp": time.now() + 3600}
var token = web.jwt_encode(payload, "secret_key")
var decoded = web.jwt_decode(token, "secret_key")
```

## Development

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/ShiboShreeRoy/ShiboScript.git
   cd shiboscript_project
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # or
   venv\Scripts\activate  # On Windows
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   # Install development dependencies
   pip install pytest flake8 black mypy
   ```

### Running Tests

```bash
# Run all tests
make test
# or
python -m pytest tests/

# Run tests with verbose output
make test-unit
# or
python -m pytest tests/unit/ -v

# Run specific test file
python -m pytest tests/unit/test_basic.py
```

### Running Examples

```bash
# Run example scripts
shiboscript examples/hello.shibo
shiboscript examples/calculator.shibo
shiboscript examples/class.shibo
```

### Building from Source

To build ShiboScript from source:

```bash
# After cloning and setting up environment
python setup.py build
python setup.py install
```

Or using pip:

```bash
pip install .
```

### Creating Executable (Optional)

If you want to create an executable version:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile src/cli/__init__.py --name shiboscript
```

The executable will be created in the `dist/` directory.

## Testing

### Test Structure

Tests are organized in the `tests/` directory:
- `tests/unit/` - Unit tests for individual components
- `tests/integration/` - Integration tests for component interactions

### Running Tests

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests only
python -m pytest tests/integration/
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

MIT License - see [LICENSE](LICENSE) file for details

## Author

ShiboShreeRoy

---

*Made with 🐕 for education and fun!*

## Quick Start Summary

For immediate use without installation, you can run ShiboScript directly:

1. **Start the interactive REPL:**
   ```bash
   python3 run_shiboscript.py
   ```
   
   The REPL features syntax highlighting with colored keywords, operators, and values for a better coding experience.

2. **Run a ShiboScript file:**
   ```bash
   python3 run_shiboscript.py path/to/your/script.shibo
   ```

3. **Try the example:**
   ```bash
   python3 run_shiboscript.py hello_world.shibo
   ```

4. **Use the dedicated compiler:**
   ```bash
   # Compile to Python
   shiboc -c script.shibo
   
   # Compile to bytecode
   shiboc -b script.shibo
   
   # Run directly
   shiboc -r script.shibo
   ```

The `run_shiboscript.py` script handles all the path setup and imports needed to run ShiboScript from this project structure. This is the easiest way to get started with ShiboScript without needing to install it via pip.

For a permanent installation, you can install via pip:
```bash
pip install -e .
```

Then you can use the `shiboscript` and `shiboc` commands directly.

