# ShiboScript Beginner Tutorial

Welcome to ShiboScript! This tutorial will guide you through the basics of the language.

## Table of Contents
1. [Hello World](#hello-world)
2. [Variables and Data Types](#variables-and-data-types)
3. [Operators](#operators)
4. [Control Structures](#control-structures)
5. [Functions](#functions)
6. [Collections](#collections)
7. [Object-Oriented Programming](#object-oriented-programming)
8. [Standard Library](#standard-library)

## Hello World

Let's start with the classic "Hello, World!" program:

```javascript
# hello.shibo
print("Hello, World!")
```

Run it:
```bash
shiboscript hello.shibo
```

## Variables and Data Types

In ShiboScript, variables are declared with the `var` keyword:

```javascript
# variables.shibo
var name = "ShiboScript"      # String
var age = 3                   # Integer
var pi = 3.14159             # Float
var isActive = true           # Boolean
var nothing = null            # Null value
```

### Data Types

- **String**: Text enclosed in double quotes
- **Number**: Integer or floating-point numbers
- **Boolean**: true or false
- **Null**: Represents no value
- **List**: Ordered collection of values
- **Dictionary**: Key-value pairs
- **Set**: Unique collection of values

## Operators

### Arithmetic Operators
```javascript
var sum = 5 + 3      # 8
var diff = 5 - 3     # 2
var product = 5 * 3  # 15
var quotient = 5 / 3 # 1.666...
var remainder = 5 % 3 # 2
var power = 5 ** 3   # 125 (if supported)
```

### Comparison Operators
```javascript
var isEqual = (5 == 3)     # false
var isNotEqual = (5 != 3)  # true
var isGreater = (5 > 3)    # true
var isLess = (5 < 3)       # false
```

### Logical Operators
```javascript
var andResult = (true && false)  # false
var orResult = (true || false)   # true
var notResult = !true            # false
```

## Control Structures

### Conditional Statements
```javascript
# conditionals.shibo
var score = 85

if (score >= 90) {
    print("Grade: A")
} else if (score >= 80) {
    print("Grade: B")
} else if (score >= 70) {
    print("Grade: C")
} else {
    print("Grade: D")
}
```

### Loops

#### For Loop
```javascript
# for_loop.shibo
for (var i = 0; i < 5; i++) {
    print("Count: " + i)
}
```

#### For-In Loop
```javascript
# for_in_loop.shibo
var fruits = ["apple", "banana", "orange"]

for (fruit in fruits) {
    print("I like " + fruit)
}

var person = {"name": "John", "age": 30}
for (key in person) {
    print(key + ": " + person[key])
}
```

#### While Loop
```javascript
# while_loop.shibo
var count = 0
while (count < 3) {
    print("Count: " + count)
    count = count + 1
}
```

## Functions

Define and use functions:

```javascript
# functions.shibo

# Simple function
func greet(name) {
    print("Hello, " + name + "!")
}

# Function with return value
func add(a, b) {
    return a + b
}

# Function with multiple parameters
func calculateArea(length, width) {
    return length * width
}

# Call functions
greet("World")
var sum = add(5, 3)
print("Sum: " + sum)
var area = calculateArea(10, 5)
print("Area: " + area)
```

## Collections

### Lists
```javascript
# lists.shibo
var numbers = [1, 2, 3, 4, 5]
var mixed = [1, "hello", true, 3.14]

# List operations
numbers.append(6)
var first = numbers[0]
var length = len(numbers)

print("First number: " + first)
print("Length: " + length)
```

### Dictionaries
```javascript
# dictionaries.shibo
var person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Access values
print("Name: " + person["name"])
print("Age: " + person["age"])

# Add new key-value pair
person["country"] = "USA"
```

### Sets
```javascript
# sets.shibo
var uniqueNumbers = set(1, 2, 3, 2, 1)  # {1, 2, 3}
uniqueNumbers.add(4)
var hasNumber = uniqueNumbers.contains(2)
```

## Object-Oriented Programming

### Classes
```javascript
# classes.shibo

class Animal {
    var name
    var species
    
    func init(self, name, species) {
        self.name = name
        self.species = species
    }
    
    func speak(self) {
        print(self.name + " makes a sound")
    }
    
    func getInfo(self) {
        return self.name + " is a " + self.species
    }
}

# Create an instance
var dog = Animal("Buddy", "Dog")
dog.speak()           # Output: Buddy makes a sound
print(dog.getInfo())  # Output: Buddy is a Dog
```

### Inheritance
```javascript
# inheritance.shibo

class Dog(Animal) {
    var breed
    
    func init(self, name, breed) {
        Animal.init(self, name, "Dog")
        self.breed = breed
    }
    
    func speak(self) {
        print(self.name + " barks: Woof!")
    }
    
    func fetch(self) {
        print(self.name + " fetches the ball!")
    }
}

var goldenRetriever = Dog("Max", "Golden Retriever")
goldenRetriever.speak()   # Output: Max barks: Woof!
goldenRetriever.fetch()   # Output: Max fetches the ball!
print(goldenRetriever.getInfo())  # Output: Max is a Dog
```

## Standard Library

ShiboScript comes with a rich standard library:

### Math Functions
```javascript
var sqrt = math.sqrt(16)    # 4
var power = math.pow(2, 3)  # 8
var pi = math.pi            # 3.14159...
```

### File Operations
```javascript
# Read file
var content = file.read("data.txt")

# Write file
file.write("output.txt", "Hello, File!")
```

### String Operations
```javascript
var text = "Hello, World!"
var upperText = upper(text)     # "HELLO, WORLD!"
var lowerText = lower(text)     # "hello, world!"
var words = split(text, " ")    # ["Hello,", "World!"]
```

## Next Steps

Now that you've learned the basics, try:

1. Experimenting with the examples in the [examples](../examples/) directory
2. Creating your own simple programs
3. Reading the [API documentation](../api_docs/)
4. Exploring advanced features like web development and database operations

Happy coding with ShiboScript!
