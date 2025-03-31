
![ShiboScript ](./icon/ShiboScript.png)


# ShiboScript v0.1.0
### Developed by ShiboShreeRoy

## Introduction
ShiboScript is a lightweight, beginner-friendly scripting language designed for educational purposes and small-scale automation tasks. It provides an intuitive syntax to help users learn programming concepts while supporting practical features such as variables, functions, control structures, and built-in operations for math, file handling, and image manipulation.

## Features
- **Simple syntax** for easy learning
- **Support for variables, functions, and control structures**
- **Built-in math operations**
- **File I/O support** (read/write files)
- **Image handling with PIL**
- **Interactive REPL for testing code**

## Getting Started
### Prerequisites
Ensure you have Python installed on your system.

### Installation
Clone this repository and navigate into it:
```sh
$ git clone https://github.com/ShiboShreeRoy/ShiboScript.git
$ cd ShiboScript
```

### Running ShiboScript
Run the interpreter:
```sh
$ python shiboscript.py
```
This starts the REPL (Read-Eval-Print Loop). To exit, type `exit`.

## Language Syntax
```bash
function function_Name(Argument or Without Argument) {
    # function body
        return "Your Info, " + Argument or Without Argument;
}
    #call function
    print(function_Name("Value"));
```
## Print Hello World !
```ShiboScript 
print("Hello World !");
```
### Variables
```shiboscript 
var x = 10;
var name = "Alice";
var flag = true;
```

### Control Structures
#### If-Else
```shiboscript
if (x > 0) {
    print("Positive");
} else {
    print("Non-positive");
}
```
#### Loops
```shiboscript
var i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}
```

### Functions
```shiboscript
func add(a, b) {
    return a + b;
}
var sum = add(3, 4);
print(sum);  // Output: 7
```

## Built-in Functions
- **Math:** `math.sqrt(n)`, `math.pow(x, y)`, `math.pi`
- **File I/O:** `read_file("file.txt")`, `write_file("file.txt", "content")`
- **String Manipulation:** `str_upper("hello")`, `str_split("a,b", ",")`
- **Image Handling:** `load_image("img.png")`, `show_image(img)`

## Example Programs
### Factorial Calculation
```shiboscript
func factorial(n) {
    if (n == 0) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
print(factorial(5));  // Output: 120
```
### File Operations
```shiboscript
var text = "Hello, ShiboScript!";
write_file("test.txt", text);
print(read_file("test.txt"));
```

## How It Works
ShiboScript is powered by three core components:
1. **Lexer** – Converts source code into tokens.
2. **Parser** – Builds an Abstract Syntax Tree (AST) from tokens.
3. **Evaluator** – Executes the AST and evaluates expressions.

## Contributing
Contributions are welcome! Feel free to submit issues and pull requests.

## License
ShiboScript is licensed under the MIT [License](LICENSE).

---

_Developed with ❤️ by ShiboShreeRoy_

