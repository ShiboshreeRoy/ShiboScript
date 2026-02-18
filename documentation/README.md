# ShiboScript Documentation

Welcome to the comprehensive documentation for ShiboScript, a lightweight scripting language designed for education and automation.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Language Reference](#language-reference)
3. [Tutorials](#tutorials)
4. [Examples](#examples)
5. [API Documentation](#api-documentation)
6. [Reference Guides](#reference-guides)
7. [Best Practices](#best-practices)

## Getting Started

### Installation

```bash
pip install shiboscript-pro
```

### Quick Start

```javascript
# hello.shibo
func greet(name) {
    print("Hello, " + name + "!")
}

greet("ShiboScript")
```

Run with:
```bash
shiboscript hello.shibo
```

### Interactive REPL

Start the interactive environment:
```bash
shiboscript
```

## Language Reference

### Data Types

ShiboScript supports the following data types:

- **Numbers**: `42`, `3.14`
- **Strings**: `"Hello"`
- **Booleans**: `true`, `false`
- **Null**: `null`
- **Lists**: `[1, 2, 3]`
- **Dictionaries**: `{"key": "value"}`
- **Sets**: `set(1, 2, 3)`

### Variables

```javascript
var name = "ShiboScript"
var age = 3
var isAwesome = true
```

### Operators

- Arithmetic: `+`, `-`, `*`, `/`, `//`, `%`, `++`, `--`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `&&`, `||`, `!`
- Bitwise: `&`, `|`, `^`, `~`, `<<`, `>>`, `>>>`

### Control Structures

#### Conditionals

```javascript
if (x > 10) {
    print("Greater than 10")
} else if (x == 10) {
    print("Equal to 10")
} else {
    print("Less than 10")
}
```

#### Loops

```javascript
# For loop
for (var i = 0; i < 10; i++) {
    print(i)
}

# For-in loop
for (item in items) {
    print(item)
}

# While loop
while (condition) {
    print("Looping...")
}
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

### Classes

```javascript
class Animal {
    var name
    
    func init(self, name) {
        self.name = name
    }
    
    func speak(self) {
        print(self.name + " makes a sound")
    }
}

class Dog(Animal) {
    func speak(self) {
        print(self.name + " says woof!")
    }
}

var myDog = Dog("Buddy")
myDog.speak()
```

## Tutorials

See the [tutorials](tutorials/) directory for step-by-step guides.

## Examples

Browse the [examples](examples/) directory for practical examples covering various use cases:

- [Basic Examples](examples/hello.shibo)
- [Calculator](examples/calculator.shibo)
- [Object-Oriented Programming](examples/classes.shibo)
- [Data Analysis](examples/data_analyzer.shibo)
- [Web Development](examples/web_api.shibo)
- [System Administration](examples/system_monitor.shibo)
- [File Operations](examples/file_organizer.shibo)
- [Advanced Features](examples/comprehensive_demo.shibo)

## API Documentation

See the [api_docs](api_docs/) directory for detailed API documentation.

## Reference Guides

See the [reference_guides](reference_guides/) directory for in-depth technical references.

## Best Practices

1. **Naming Conventions**: Use camelCase for variables and functions
2. **Code Organization**: Group related functions and classes together
3. **Documentation**: Comment complex logic and public APIs
4. **Error Handling**: Always handle potential errors in production code
5. **Resource Management**: Close files and connections properly
6. **Security**: Validate inputs and sanitize outputs when dealing with external data

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details on how to contribute to ShiboScript.
