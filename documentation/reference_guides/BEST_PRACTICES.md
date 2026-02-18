# ShiboScript Best Practices Guide

This guide outlines best practices for writing effective ShiboScript code.

## Table of Contents
1. [Code Organization](#code-organization)
2. [Naming Conventions](#naming-conventions)
3. [Code Style](#code-style)
4. [Performance Tips](#performance-tips)
5. [Security Practices](#security-practices)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)

## Code Organization

### File Structure
Organize your code into logical modules:

```
project/
├── main.shibo          # Main entry point
├── lib/
│   ├── utils.shibo     # Utility functions
│   ├── helpers.shibo   # Helper functions
│   └── constants.shibo # Constants
├── modules/
│   ├── auth.shibo      # Authentication module
│   └── data.shibo      # Data handling module
└── tests/
    ├── test_main.shibo
    └── test_utils.shibo
```

### Module Imports
Structure your imports logically:

```javascript
# Standard library imports first
import math
import os
import file

# Third-party imports
import net
import crypto

# Local application imports
import utils
import constants
```

### Class Organization
Group related functionality in classes:

```javascript
class DataManager {
    var data
    var filename
    
    func init(self, filename) {
        self.filename = filename
        self.data = []
    }
    
    func load(self) {
        # Load data from file
    }
    
    func save(self) {
        # Save data to file
    }
    
    func add_record(self, record) {
        # Add a record
    }
    
    func find_record(self, criteria) {
        # Find records matching criteria
    }
}
```

## Naming Conventions

### Variables and Functions
Use camelCase for variables and functions:

```javascript
# Good
var userName = "John"
var userAge = 30
func calculateTotal(items) { ... }

# Avoid
var user_name = "John"
func calculate_total(items) { ... }
```

### Constants
Use uppercase with underscores for constants:

```javascript
# Good
var MAX_CONNECTIONS = 100
var DEFAULT_TIMEOUT = 30
```

### Classes
Use PascalCase for class names:

```javascript
# Good
class UserManager { ... }
class DatabaseConnection { ... }

# Avoid
class userManager { ... }
class database_connection { ... }
```

### Private Members
Prefix private members with underscore:

```javascript
class MyClass {
    var _privateVar
    var publicVar
    
    func _privateMethod(self) { ... }
    func publicMethod(self) { ... }
}
```

## Code Style

### Indentation
Use consistent indentation (typically 4 spaces):

```javascript
# Good
if (condition) {
    if (anotherCondition) {
        doSomething()
    }
}

# Avoid
if (condition) {
  if (anotherCondition) {
     doSomething()
  }
}
```

### Line Length
Keep lines under 80 characters when possible:

```javascript
# Good
if (veryLongVariableName && anotherLongVariableName && 
    someOtherCondition) {
    doSomething()
}

# Also good - break complex expressions
var result = someFunction(
    veryLongParameter,
    anotherLongParameter,
    thirdParameter
)
```

### Comments
Write clear, helpful comments:

```javascript
# Good
# Calculate the total price including tax
func calculateTotalWithTax(price, taxRate) {
    var tax = price * taxRate
    return price + tax
}

# Avoid
# Do the thing
func doSomething() { ... }
```

### Function Length
Keep functions short and focused:

```javascript
# Good - focused function
func isValidEmail(email) {
    return email.contains("@") && email.contains(".")
}

# Avoid - function doing too much
func processUser(userData) {
    # Validate email
    # Hash password
    # Save to database
    # Send welcome email
    # Log activity
}
```

## Performance Tips

### Efficient Loops
Prefer for-in loops over index-based when possible:

```javascript
# Good
for (item in items) {
    process(item)
}

# Less efficient
for (var i = 0; i < len(items); i++) {
    process(items[i])
}
```

### Avoid Repeated Calculations
Cache expensive calculations:

```javascript
# Good
var expensiveResult = expensiveCalculation()
for (item in items) {
    item.setValue(expensiveResult)
}

# Avoid
for (item in items) {
    item.setValue(expensiveCalculation())  # Called repeatedly
}
```

### Use Built-in Functions
Leverage built-in functions for common operations:

```javascript
# Good - uses built-in
var total = sum(numbers)

# Avoid - manual implementation
var total = 0
for (num in numbers) {
    total = total + num
}
```

### Minimize Object Creation
Reuse objects when possible:

```javascript
# Good
var buffer = createBuffer()
for (data in dataList) {
    buffer.clear()
    buffer.write(data)
    process(buffer)
}

# Avoid
for (data in dataList) {
    var buffer = createBuffer()  # New object each time
    buffer.write(data)
    process(buffer)
}
```

## Security Practices

### Input Validation
Always validate external input:

```javascript
# Good
func processUserData(userData) {
    if (!isValidInput(userData)) {
        throw "Invalid input"
    }
    # Process validated data
}

func isValidInput(data) {
    # Implement validation logic
    return type(data) == "string" && len(data) > 0 && len(data) < 1000
}
```

### File Operations
Validate file paths to prevent directory traversal:

```javascript
# Good
func readFileSecure(filePath) {
    var normalizedPath = normalizePath(filePath)
    if (!allowedPath(normalizedPath)) {
        throw "Access denied"
    }
    return file.read(normalizedPath)
}

func normalizePath(path) {
    # Implement path normalization
}
```

### SQL Injection Prevention
Use parameterized queries:

```javascript
# Good - if DB supports parameterized queries
var result = db.query("SELECT * FROM users WHERE id = ?", userId)

# Avoid - direct string concatenation
var query = "SELECT * FROM users WHERE id = " + userId
var result = db.query(query)
```

### Password Handling
Hash passwords securely:

```javascript
# Good
func hashPassword(password, salt) {
    return crypto.sha256(password + salt)
}

func verifyPassword(input, hashed, salt) {
    return hashPassword(input, salt) == hashed
}
```

## Testing Guidelines

### Write Testable Code
Structure code to be easily testable:

```javascript
# Good - easily testable
func calculateDiscount(total, discountPercent) {
    return total * (discountPercent / 100)
}

# Can be tested with various inputs
```

### Test Edge Cases
Include tests for edge cases:

```javascript
# Test cases to consider
# Empty inputs
# Maximum values
# Minimum values
# Invalid inputs
# Boundary conditions
```

### Use Descriptive Test Names
Write clear test names:

```javascript
# Good
func testCalculateDiscountWithValidInputs() { ... }
func testCalculateDiscountWithZeroPercent() { ... }
func testCalculateDiscountWithNegativeTotal() { ... }

# Avoid
func test1() { ... }
func test2() { ... }
```

## Documentation

### Function Documentation
Document functions with purpose, parameters, and return values:

```javascript
# Calculate the factorial of a number
# 
# Parameters:
#   n - the number to calculate factorial for
#
# Returns:
#   The factorial of n, or 1 if n <= 1
func factorial(n) {
    if (n <= 1) {
        return 1
    }
    return n * factorial(n - 1)
}
```

### Class Documentation
Document classes and their methods:

```javascript
# Manages user accounts and authentication
class UserManager {
    var users
    
    # Initialize the user manager
    func init(self) {
        self.users = {}
    }
    
    # Add a new user
    # Parameters:
    #   username - the username
    #   password - the password
    func addUser(self, username, password) {
        self.users[username] = hashPassword(password)
    }
}
```

### Complex Logic
Comment complex algorithms:

```javascript
# Fast exponentiation algorithm
# Calculates base^exponent efficiently using binary exponentiation
func fastPower(base, exponent) {
    var result = 1
    var currentBase = base
    var remainingExp = exponent
    
    while (remainingExp > 0) {
        if (remainingExp % 2 == 1) {
            result = result * currentBase
        }
        currentBase = currentBase * currentBase
        remainingExp = remainingExp / 2
    }
    
    return result
}
```

## Error Handling

### Specific Error Types
Use specific error handling when possible:

```javascript
# Good
try {
    var data = parseJson(input)
} catch (error) {
    if (error.contains("JSON")) {
        # Handle JSON parsing error
    } else {
        # Handle other errors
    }
}
```

### Fail Fast
Check for errors early:

```javascript
# Good
func processFile(filename) {
    if (!os.exists(filename)) {
        throw "File does not exist: " + filename
    }
    
    var content = file.read(filename)
    # Continue processing
}
```

Following these best practices will help you write cleaner, more maintainable, and more efficient ShiboScript code.
