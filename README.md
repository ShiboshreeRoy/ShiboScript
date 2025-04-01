
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
```bash
python shiboscript.py
```
### Running ShiboScript
Run the interpreter with file:
```bash
python shiboscript.py filename.sp
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
## Input 
```ShiboScript
var x = input("Enter a number: ");
Enter a number: 25
print(math.sqrt(x));
5.0
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
#### 3 Type of Loops in ShiboScript
## Like Them For, While, Do-While

### For Loop
```shiboscript
var lst = [1, 2, 3];
for (x in lst) {
     print(x);
 }
#Output : 1, 2, 3
```
## Or 
## For Loop with Range
```shiboscript
 for (i in range(1, 4)) { 
    print(i); 
}
```
### While Loop
```shiboscript
var i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}
```
### Do-While Loop
```shiboscript
var i = 0;
do {
    print(i);
    i = i + 1;
} while (i < 3);
#Output: 1,2,3 
```
### Functions
```shiboscript
func add(a, b) {
    return a + b;
}
var sum = add(3, 4);
print(sum);  // Output: 7
```
### Arrays
```shiboscript
var arr = [1, 2, 3];
arr[0] = 10;
append(arr, 4); //append 4 to the end of the array
print(arr);  // Output: [10, 2, 3, 4,];
remove(arr, 2); // remmove  element from array
[10, 3, 4] //output
pop(arr, 0) // remove first element from array
[3, 4] //output

```
### Array Example 
```shiboscript
# Create a list of fruits
var fruits = ["apple", "banana", "cherry"];

# Print the original list
print("Original list:");
print(fruits);

# Add a new fruit to the end
append(fruits, "date");
print("After append:");
print(fruits);

# Change the second fruit
fruits[1] = "blueberry";
print("After modification:");
print(fruits);

# Get a sublist with slicing
var subFruits = fruits[1:3];
print("Sublist:");
print(subFruits);

# Remove a specific fruit
remove(fruits, "cherry");
print("After remove:");
print(fruits);

# Remove and discard the last fruit
pop(fruits);
print("After pop:");
print(fruits);
```
### Output
```shiboscript
Original list:
['apple', 'banana', 'cherry']
After append:
['apple', 'banana', 'cherry', 'date']
After modification:
['apple', 'blueberry', 'cherry', 'date']
Sublist:
['blueberry', 'cherry']
After remove:
['apple', 'blueberry', 'date']
After pop:
['apple', 'blueberry']
```
### Dictionary
```shiboscript
var d = {"a": 1, "b": 2}
d["a"]
1 //output
d["c"] = 3 // add new key-value pair
d["c"] //output 3
keys(d) //output ["a", "b", "c"]
```

###  Types and Functions
```shiboscript
var b = true;
print(b);
True // Output
print(type(b));
bool //Output
var n = null;
print(n);
None //Output
print(str(123));
123//Output
```
## Type Casting
```shiboscript
var num = 123;
print(str(num));        # "123"
print(int("456"));      # 456
print(float("5.5"));    # 5.5

```
## String methods
```shiboscript
var s = "hello world";
print(s.upper());       # "HELLO WORLD"
print(s.lower());       # "hello world"
print(s.capitalize());  # "Hello world"
print(s.split(" "));    # ["hello", "world"]
print(" ".join(s.split(" ")));  # "hello world"
```
## List methods(some)
```shiboscript
var lst = [1, 2, 3];
lst.append(4);
lst.sort();
print(lst);
```

# Dictionary access
```shiboscript 
print(math.sqrt(16));   # 4.0
var d = {"a": 1};
d.b = 2;
print(d);               # {'a': 1, 'b': 2}
print(d.keys());        # ['a', 'b']
```

# Length
```shiboscript
print(len(s));          # 11
```
## Built-in Functions
- **Math:** `math.sqrt(n)`, `math.pow(x, y)`, `math.pi`
- **File I/O:** `read_file("file.txt")`, `write_file("file.txt", "content")`
- **String Manipulation:** `str_upper("hello")`, `str_split("a,b", ",")`
- **Image Handling:** `load_image("img.png")`, `show_image(img)`

## Error Hendling
```shiboscript
try { 
    print(1 / 0); 
    } catch (e) {
         print("Error: " + e); 
}
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

