# ShiboScript 🐕

A lightweight, educational scripting language designed for learning programming concepts and automation tasks.

## Features

- **Simple Syntax**: Easy-to-learn syntax inspired by popular programming languages
- **Object-Oriented**: Full support for classes, inheritance, and interfaces
- **Built-in Libraries**: Rich set of built-in functions for file I/O, networking, cryptography, and more
- **Interactive REPL**: Built-in read-eval-print loop for experimentation
- **Cross-Platform**: Runs on Windows, macOS, and Linux
- **Advanced Data Structures**: Includes sets, queues, stacks, and priority queues
- **Web Development**: Built-in web server capabilities and HTTP functions
- **Database ORM**: Object-relational mapping for SQLite databases
- **Functional Programming**: Map, filter, reduce, and other functional utilities
- **Error Handling**: Comprehensive exception handling with try/catch
- **Logging and Monitoring**: Built-in logging and metrics collection

## Installation

```bash
pip install shiboscript-pro
```

## Quick Start

### Using the REPL

```bash
shiboscript
```

```
🐕 Welcome to ShiboScript v1.0.0 REPL! Type 'exit' to quit, 'help' for help.
shiboscript>>> print("Hello, World!")
Hello, World!
shiboscript>>> var x = 42
shiboscript>>> print(x)
42
```

### Running Scripts

Create a file `hello.shibo`:

```javascript
func greet(name) {
    print("Hello, " + name + "!")
}

greet("ShiboScript")
```

Run it:

```bash
shiboscript hello.shibo
```

## Language Features

### Variables and Data Types
```javascript
var name = "ShiboScript"
var age = 3
var isAwesome = true
var numbers = [1, 2, 3, 4, 5]
var person = {"name": "Shibo", "type": "Script"}
```

### Functions
```javascript
func add(a, b) {
    return a + b
}

func factorial(n) {
    if (n <= 1) {
        return 1
    }
    return n * factorial(n - 1)
}
```

### Control Flow
```javascript
// If statements
if (x > 10) {
    print("Greater than 10")
} else if (x == 10) {
    print("Equal to 10")
} else {
    print("Less than 10")
}

// Loops
for (var i = 0; i < 10; i++) {
    print(i)
}

for (item in items) {
    print(item)
}

while (condition) {
    // do something
}
```

### Classes and OOP
```javascript
class Animal {
    var name
    
    func init(name) {
        self.name = name
    }
    
    func speak() {
        print("Animal sound")
    }
}

class Dog(Animal) {
    func speak() {
        print(self.name + " says woof!")
    }
}

var dog = Dog("Buddy")
dog.speak()  // Buddy says woof!
```

### Error Handling
```javascript
try {
    // risky code
    var result = 10 / 0
} catch (error) {
    print("Error occurred: " + error)
}
```

## Built-in Libraries

### Math Operations
```javascript
var sqrt = math.sqrt(16)  // 4
var pi = math.pi          // 3.14159...
```

### File Operations
```javascript
var content = file.read("data.txt")
file.write("output.txt", "Hello World")
```

### Network Operations
```javascript
var response = net.http_get("https://api.example.com")
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

## Command Line Options

- `shiboscript` - Start interactive REPL
- `shiboscript file.shibo` - Run a script file
- `shiboscript run file.shibo` - Alternative way to run a script file
- `shiboscript --version` - Show version information
- `shiboscript --help` - Show help information

## License

MIT License - see LICENSE file for details

## Author

ShiboShreeRoy

---

*Made with 🐕 for education and fun!*
