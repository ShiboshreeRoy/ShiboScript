# 🚀 SHIBOSCRIPT QUICK REFERENCE GUIDE

## 📋 Essential Syntax at a Glance

### Basic Operations
```javascript
// Variables
var name = "Alice"
var age = 25
var is_student = true

// Printing
print("Hello, " + name + "!")

// Comments
// This is a single-line comment
/* This is a 
   multi-line comment */
```

### Control Flow Quick Reference

#### If Statements
```javascript
if (condition) {
    // code
} else if (other_condition) {
    // code
} else {
    // code
}
```

#### Loops
```javascript
// For loop
for (var i = 0; i < 10; i++) {
    print(i)
}

// While loop
var count = 0
while (count < 5) {
    print(count)
    count++
}

// Loop through list
var items = ["a", "b", "c"]
for (var item in items) {
    print(item)
}
```

### Functions
```javascript
// Function definition
func greet(name) {
    return "Hello, " + name + "!"
}

// Function call
var message = greet("Alice")
print(message)
```

### Classes
```javascript
// Class definition
class Person {
    var name
    var age
    
    func init(name, age) {
        self.name = name
        self.age = age
    }
    
    func introduce() {
        print("I'm " + self.name + ", " + self.age + " years old")
    }
}

// Class usage
var person = Person("Alice", 25)
person.introduce()
```

## 📚 DATA STRUCTURES CHEAT SHEET

### Lists (Arrays)
```javascript
// Creation
var empty_list = []
var numbers = [1, 2, 3, 4, 5]
var mixed = [1, "hello", true]

// Operations
append(list, item)        // Add item
remove_item(list, item)   // Remove item
len(list)                 // Get length
list[index]               // Access element
list[start:end]           // Slice
sort(list)                // Sort
reverse(list)             // Reverse
```

### Dictionaries (Objects)
```javascript
// Creation
var empty_dict = {}
var person = {"name": "Alice", "age": 25}

// Operations
dict["key"]               // Access value
dict["key"] = value       // Set value
"key" in dict             // Check existence
keys(dict)                // Get all keys
values(dict)              // Get all values
len(dict)                 // Get size
```

## 🔧 BUILT-IN FUNCTIONS REFERENCE

### String Functions
```javascript
len(string)               // Length
upper(string)             // Uppercase
lower(string)             // Lowercase
split(string, separator)  // Split into list
join(separator, list)     // Join list into string
replace(string, old, new) // Replace text
strip(string)             // Remove whitespace
```

### Mathematical Functions
```javascript
sqrt(number)              // Square root
pow(base, exponent)       // Power
abs(number)               // Absolute value
round(number, decimals)   // Round
min(list)                 // Minimum
max(list)                 // Maximum
sum(list)                 // Sum all elements
```

### List Functions
```javascript
len(list)                 // Length
append(list, item)        // Add item
remove_item(list, item)   // Remove item
insert(list, index, item) // Insert at position
pop(list, index)          // Remove and return item
index(list, item)         // Find item index
sort(list)                // Sort
reverse(list)             // Reverse
```

### File Operations
```javascript
file.read(filename)       // Read file
file.write(filename, content)  // Write file
file.append(filename, content) // Append to file
exists(filename)          // Check if exists
is_file(filename)         // Check if file
is_dir(dirname)           // Check if directory
list_dir(dirname)         // List directory
mkdir(dirname)            // Create directory
```

## ⚡ QUICK EXAMPLES

### 1. Hello World Program
```javascript
print("Hello, World!")
```

### 2. Simple Calculator
```javascript
func add(a, b) {
    return a + b
}

func multiply(a, b) {
    return a * b
}

var result1 = add(5, 3)      // 8
var result2 = multiply(4, 6)  // 24
print("5 + 3 = " + result1)
print("4 × 6 = " + result2)
```

### 3. Number Guesser Game
```javascript
var secret_number = random_int(1, 10)
var guess = 0

print("Guess a number between 1 and 10!")

while (guess != secret_number) {
    guess = int(input("Your guess: "))
    if (guess < secret_number) {
        print("Too low!")
    } else if (guess > secret_number) {
        print("Too high!")
    } else {
        print("Correct! You guessed it!")
    }
}
```

### 4. Todo List Manager
```javascript
var todos = []

func add_todo(task) {
    append(todos, task)
    print("Added: " + task)
}

func show_todos() {
    print("=== Todo List ===")
    for (var i = 0; i < len(todos); i++) {
        print((i + 1) + ". " + todos[i])
    }
    print("=================")
}

func remove_todo(index) {
    if (index >= 0 && index < len(todos)) {
        var removed = todos[index]
        remove_item(todos, removed)
        print("Removed: " + removed)
    } else {
        print("Invalid index!")
    }
}

// Usage
add_todo("Learn ShiboScript")
add_todo("Build a project")
add_todo("Write documentation")
show_todos()
remove_todo(1)
show_todos()
```

### 5. Grade Calculator
```javascript
func calculate_grade(scores) {
    var total = 0
    for (var score in scores) {
        total = total + score
    }
    var average = total / len(scores)
    
    if (average >= 90) {
        return "A"
    } else if (average >= 80) {
        return "B"
    } else if (average >= 70) {
        return "C"
    } else if (average >= 60) {
        return "D"
    } else {
        return "F"
    }
}

var student_scores = [85, 92, 78, 96, 88]
var grade = calculate_grade(student_scores)
print("Average grade: " + grade)
```

### 6. Contact Manager
```javascript
class Contact {
    var name
    var phone
    var email
    
    func init(name, phone, email) {
        self.name = name
        self.phone = phone
        self.email = email
    }
    
    func get_info() {
        return self.name + " - " + self.phone + " - " + self.email
    }
}

class ContactBook {
    var contacts = []
    
    func add_contact(name, phone, email) {
        var contact = Contact(name, phone, email)
        append(self.contacts, contact)
        print("Added: " + contact.get_info())
    }
    
    func search_contact(name) {
        for (var contact in self.contacts) {
            if (contact.name == name) {
                print("Found: " + contact.get_info())
                return contact
            }
        }
        print("Contact not found: " + name)
        return null
    }
    
    func show_all() {
        print("=== Contact Book ===")
        for (var contact in self.contacts) {
            print(contact.get_info())
        }
        print("===================")
    }
}

// Usage
var book = ContactBook()
book.add_contact("Alice", "123-456-7890", "alice@email.com")
book.add_contact("Bob", "098-765-4321", "bob@email.com")
book.show_all()
book.search_contact("Alice")
```

### 7. Simple Banking System
```javascript
class BankAccount {
    var account_number
    var holder_name
    var _balance
    
    func init(account_number, holder_name, initial_balance = 0) {
        self.account_number = account_number
        self.holder_name = holder_name
        self._balance = initial_balance
    }
    
    func deposit(amount) {
        if (amount > 0) {
            self._balance = self._balance + amount
            print("Deposited $" + amount)
            self.show_balance()
        }
    }
    
    func withdraw(amount) {
        if (amount > 0 && amount <= self._balance) {
            self._balance = self._balance - amount
            print("Withdrew $" + amount)
            self.show_balance()
        } else {
            print("Invalid withdrawal amount")
        }
    }
    
    func show_balance() {
        print("Account " + self.account_number + " balance: $" + self._balance)
    }
    
    func get_info() {
        return "Account: " + self.account_number + 
               ", Holder: " + self.holder_name + 
               ", Balance: $" + self._balance
    }
}

// Usage
var account = BankAccount("ACC001", "Alice Smith", 1000)
account.show_balance()
account.deposit(500)
account.withdraw(200)
account.withdraw(2000)  // Invalid
print(account.get_info())
```

### 8. Text Analyzer
```javascript
func analyze_text(text) {
    var words = split(text, " ")
    var word_count = len(words)
    
    var char_count = len(text)
    var sentence_count = len(split(text, "."))
    
    // Count vowels
    var vowels = "aeiouAEIOU"
    var vowel_count = 0
    for (var char in text) {
        if (vowels.find(char) != -1) {
            vowel_count = vowel_count + 1
        }
    }
    
    print("=== Text Analysis ===")
    print("Characters: " + char_count)
    print("Words: " + word_count)
    print("Sentences: " + sentence_count)
    print("Vowels: " + vowel_count)
    print("Average word length: " + (char_count / word_count))
    print("====================")
}

var sample_text = "Hello world. This is a sample text for analysis. It contains multiple sentences."
analyze_text(sample_text)
```

## 🎯 COMMON PATTERNS

### Input Validation
```javascript
func get_valid_number(prompt, min_val, max_val) {
    var valid = false
    var number = 0
    
    while (!valid) {
        var input_str = input(prompt)
        number = int(input_str)
        
        if (number >= min_val && number <= max_val) {
            valid = true
        } else {
            print("Please enter a number between " + min_val + " and " + max_val)
        }
    }
    
    return number
}

var age = get_valid_number("Enter your age (1-120): ", 1, 120)
```

### Menu System
```javascript
func show_menu() {
    print("=== Main Menu ===")
    print("1. Add item")
    print("2. View items")
    print("3. Delete item")
    print("4. Exit")
    print("=================")
}

func handle_choice(choice) {
    if (choice == 1) {
        print("Adding item...")
    } else if (choice == 2) {
        print("Viewing items...")
    } else if (choice == 3) {
        print("Deleting item...")
    } else if (choice == 4) {
        print("Goodbye!")
        return false
    } else {
        print("Invalid choice!")
    }
    return true
}

// Main program loop
var running = true
while (running) {
    show_menu()
    var choice = int(input("Enter your choice: "))
    running = handle_choice(choice)
}
```

### Data Processing Pipeline
```javascript
func process_data(raw_data) {
    // Step 1: Clean data
    var clean_data = []
    for (var item in raw_data) {
        if (item != null && item != "") {
            append(clean_data, item)
        }
    }
    
    // Step 2: Transform data
    var processed_data = []
    for (var item in clean_data) {
        var processed = upper(item)
        append(processed_data, processed)
    }
    
    // Step 3: Analyze data
    var analysis = {
        "total": len(processed_data),
        "items": processed_data
    }
    
    return analysis
}

var raw = ["hello", "", "world", null, "shibo"]
var result = process_data(raw)
print("Processed " + result.total + " items")
```

## 🚨 ERROR HANDLING PATTERNS

### Safe File Operations
```javascript
func safe_read_file(filename) {
    if (exists(filename)) {
        if (is_file(filename)) {
            return file.read(filename)
        } else {
            print("Error: " + filename + " is not a file")
            return null
        }
    } else {
        print("Error: " + filename + " not found")
        return null
    }
}

var content = safe_read_file("data.txt")
if (content != null) {
    print("File content: " + content)
}
```

### Input Validation Pattern
```javascript
func get_valid_input(prompt, validator_func) {
    var valid = false
    var value = null
    
    while (!valid) {
        value = input(prompt)
        var validation_result = validator_func(value)
        
        if (validation_result.valid) {
            valid = true
        } else {
            print("Error: " + validation_result.message)
        }
    }
    
    return value
}

func validate_email(email) {
    if (email.find("@") != -1 && email.find(".") != -1) {
        return {"valid": true, "message": ""}
    } else {
        return {"valid": false, "message": "Invalid email format"}
    }
}

var email = get_valid_input("Enter email: ", validate_email)
```

## 🛠️ DEBUGGING TIPS

### Print Debugging
```javascript
func debug_function(data) {
    print("DEBUG: Input data = " + str(data))
    
    var result = process(data)
    print("DEBUG: Processing result = " + str(result))
    
    return result
}
```

### Step-by-Step Execution
```javascript
// Break down complex operations
var step1 = prepare_data(input_data)
print("Step 1 complete: " + str(step1))

var step2 = process_data(step1)
print("Step 2 complete: " + str(step2))

var final_result = finalize(step2)
print("Final result: " + str(final_result))
```

## 📈 PERFORMANCE TIPS

### Efficient List Operations
```javascript
// Good: Use built-in functions
var sorted_list = sort(unsorted_list)

// Good: Use appropriate data structures
var lookup_set = Set(items)  // O(1) lookup vs O(n) for lists

// Good: Avoid repeated calculations
var expensive_result = expensive_calculation()
// Use expensive_result multiple times
```

### Memory Management
```javascript
// Clear large data structures when done
var large_data = load_large_dataset()
process_data(large_data)
large_data = []  // Free memory
```

## 🎓 LEARNING RESOURCES

### Practice Projects
1. **Calculator** - Basic arithmetic operations
2. **Todo List** - CRUD operations with lists
3. **Contact Manager** - Class-based data management
4. **Simple Game** - User interaction and logic
5. **Data Analyzer** - File processing and statistics
6. **Web Scraper** - HTTP requests and data extraction
7. **Database App** - ORM and data persistence
8. **Web API** - Server creation and routing

### Next Steps
- Read the complete documentation
- Try the example projects
- Build your own applications
- Explore enterprise features
- Join the community

---

**Remember: Start simple and build complexity gradually. Happy coding!** 🐕✨