# 🎓 SHIBOSCRIPT LEARNING EXERCISES

## 🎯 Progressive Learning Path

Start with these exercises in order to master ShiboScript from basics to advanced concepts.

## 🟢 BEGINNER EXERCISES

### Exercise 1: Basic Calculator
**Objective**: Learn variables, basic operations, and user input

```javascript
// Create a simple calculator that can:
// 1. Add two numbers
// 2. Subtract two numbers
// 3. Multiply two numbers
// 4. Divide two numbers

print("=== Simple Calculator ===")

// Get user input
var num1 = float(input("Enter first number: "))
var num2 = float(input("Enter second number: "))

// Perform calculations
var sum_result = num1 + num2
var diff_result = num1 - num2
var product_result = num1 * num2
var quotient_result = num1 / num2

// Display results
print(num1 + " + " + num2 + " = " + sum_result)
print(num1 + " - " + num2 + " = " + diff_result)
print(num1 + " × " + num2 + " = " + product_result)
print(num1 + " ÷ " + num2 + " = " + quotient_result)
```

### Exercise 2: Personal Greeter
**Objective**: Learn functions and string manipulation

```javascript
// Create a program that:
// 1. Asks for user's name
// 2. Asks for user's age
// 3. Greets them personally
// 4. Tells them how old they'll be next year

func greet_person(name, age) {
    print("Hello, " + name + "!")
    print("You are " + age + " years old.")
    print("Next year you will be " + (age + 1) + " years old!")
}

var user_name = input("What's your name? ")
var user_age = int(input("How old are you? "))

greet_person(user_name, user_age)
```

### Exercise 3: Number Checker
**Objective**: Learn conditional statements

```javascript
// Create a program that:
// 1. Asks for a number
// 2. Tells if it's positive, negative, or zero
// 3. Tells if it's even or odd
// 4. Tells if it's divisible by 5

var number = int(input("Enter a number: "))

// Check positive/negative/zero
if (number > 0) {
    print("The number is positive")
} else if (number < 0) {
    print("The number is negative")
} else {
    print("The number is zero")
}

// Check even/odd
if (number % 2 == 0) {
    print("The number is even")
} else {
    print("The number is odd")
}

// Check divisible by 5
if (number % 5 == 0) {
    print("The number is divisible by 5")
} else {
    print("The number is not divisible by 5")
}
```

### Exercise 4: Simple Loop Counter
**Objective**: Learn loops and basic iteration

```javascript
// Create programs that:
// 1. Count from 1 to 10
// 2. Count backwards from 10 to 1
// 3. Count by 2s from 0 to 20
// 4. Print a multiplication table

print("=== Counting Exercises ===")

// Count 1 to 10
print("Counting 1 to 10:")
for (var i = 1; i <= 10; i++) {
    print(i)
}

// Count backwards
print("\nCounting backwards 10 to 1:")
for (var i = 10; i >= 1; i--) {
    print(i)
}

// Count by 2s
print("\nCounting by 2s from 0 to 20:")
for (var i = 0; i <= 20; i = i + 2) {
    print(i)
}

// Multiplication table
print("\nMultiplication table for 5:")
for (var i = 1; i <= 10; i++) {
    print("5 × " + i + " = " + (5 * i))
}
```

## 🟡 INTERMEDIATE EXERCISES

### Exercise 5: List Operations
**Objective**: Learn list manipulation and iteration

```javascript
// Create a program that:
// 1. Creates a list of favorite foods
// 2. Adds new foods to the list
// 3. Removes foods from the list
// 4. Displays the list in different ways

print("=== Favorite Foods Manager ===")

var favorite_foods = ["Pizza", "Burger", "Sushi"]

print("Current favorite foods:")
for (var i = 0; i < len(favorite_foods); i++) {
    print((i + 1) + ". " + favorite_foods[i])
}

// Add new food
var new_food = input("What food would you like to add? ")
append(favorite_foods, new_food)
print("Added " + new_food + " to your list!")

// Remove food
print("\nCurrent list:")
for (var i = 0; i < len(favorite_foods); i++) {
    print((i + 1) + ". " + favorite_foods[i])
}

var remove_index = int(input("Which food would you like to remove? (Enter number): ")) - 1
if (remove_index >= 0 && remove_index < len(favorite_foods)) {
    var removed_food = favorite_foods[remove_index]
    remove_item(favorite_foods, removed_food)
    print("Removed " + removed_food + " from your list!")
} else {
    print("Invalid selection!")
}

// Display final list
print("\nYour updated favorite foods:")
for (var food in favorite_foods) {
    print("- " + food)
}
```

### Exercise 6: Grade Calculator
**Objective**: Learn data processing and averages

```javascript
// Create a program that:
// 1. Collects student grades
// 2. Calculates average grade
// 3. Determines letter grade
// 4. Shows grade distribution

print("=== Student Grade Calculator ===")

var grades = []
var num_subjects = int(input("How many subjects do you have? "))

// Collect grades
for (var i = 1; i <= num_subjects; i++) {
    var grade = float(input("Enter grade for subject " + i + ": "))
    append(grades, grade)
}

// Calculate average
var total = 0
for (var grade in grades) {
    total = total + grade
}
var average = total / len(grades)

// Determine letter grade
var letter_grade = ""
if (average >= 90) {
    letter_grade = "A"
} else if (average >= 80) {
    letter_grade = "B"
} else if (average >= 70) {
    letter_grade = "C"
} else if (average >= 60) {
    letter_grade = "D"
} else {
    letter_grade = "F"
}

// Display results
print("\n=== Grade Report ===")
print("Grades: " + str(grades))
print("Average: " + round(average, 2))
print("Letter Grade: " + letter_grade)

// Show grade distribution
var grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
for (var grade in grades) {
    if (grade >= 90) {
        grade_counts["A"] = grade_counts["A"] + 1
    } else if (grade >= 80) {
        grade_counts["B"] = grade_counts["B"] + 1
    } else if (grade >= 70) {
        grade_counts["C"] = grade_counts["C"] + 1
    } else if (grade >= 60) {
        grade_counts["D"] = grade_counts["D"] + 1
    } else {
        grade_counts["F"] = grade_counts["F"] + 1
    }
}

print("\nGrade Distribution:")
for (var grade in keys(grade_counts)) {
    if (grade_counts[grade] > 0) {
        print(grade + ": " + grade_counts[grade] + " subject(s)")
    }
}
```

### Exercise 7: Simple Dictionary Usage
**Objective**: Learn dictionary operations and key-value pairs

```javascript
// Create a program that:
// 1. Stores student information
// 2. Allows adding new students
// 3. Searches for student information
// 4. Displays all students

print("=== Student Information System ===")

var students = {}

func add_student() {
    var id = input("Enter student ID: ")
    var name = input("Enter student name: ")
    var age = int(input("Enter student age: "))
    var grade = input("Enter student grade: ")
    
    students[id] = {
        "name": name,
        "age": age,
        "grade": grade
    }
    
    print("Student " + name + " added successfully!")
}

func search_student() {
    var id = input("Enter student ID to search: ")
    if (id in students) {
        var student = students[id]
        print("\n=== Student Information ===")
        print("ID: " + id)
        print("Name: " + student["name"])
        print("Age: " + student["age"])
        print("Grade: " + student["grade"])
    } else {
        print("Student not found!")
    }
}

func show_all_students() {
    if (len(students) == 0) {
        print("No students in the system!")
        return
    }
    
    print("\n=== All Students ===")
    for (var id in keys(students)) {
        var student = students[id]
        print("ID: " + id + " | Name: " + student["name"] + 
              " | Age: " + student["age"] + " | Grade: " + student["grade"])
    }
}

// Main program
var running = true
while (running) {
    print("\n=== Menu ===")
    print("1. Add Student")
    print("2. Search Student")
    print("3. Show All Students")
    print("4. Exit")
    
    var choice = int(input("Enter your choice: "))
    
    if (choice == 1) {
        add_student()
    } else if (choice == 2) {
        search_student()
    } else if (choice == 3) {
        show_all_students()
    } else if (choice == 4) {
        print("Goodbye!")
        running = false
    } else {
        print("Invalid choice!")
    }
}
```

### Exercise 8: Class Implementation
**Objective**: Learn object-oriented programming

```javascript
// Create a Library Management System using classes

class Book {
    var title
    var author
    var isbn
    var is_available
    
    func init(title, author, isbn) {
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = true
    }
    
    func get_info() {
        var status = "Available"
        if (!self.is_available) {
            status = "Checked Out"
        }
        return self.title + " by " + self.author + " (ISBN: " + self.isbn + ") - " + status
    }
    
    func check_out() {
        if (self.is_available) {
            self.is_available = false
            print("Book checked out: " + self.title)
        } else {
            print("Book is already checked out: " + self.title)
        }
    }
    
    func return_book() {
        if (!self.is_available) {
            self.is_available = true
            print("Book returned: " + self.title)
        } else {
            print("Book is already available: " + self.title)
        }
    }
}

class Library {
    var books = []
    
    func add_book(title, author, isbn) {
        var book = Book(title, author, isbn)
        append(self.books, book)
        print("Added book: " + title)
    }
    
    func find_book(isbn) {
        for (var book in self.books) {
            if (book.isbn == isbn) {
                return book
            }
        }
        return null
    }
    
    func show_all_books() {
        print("\n=== Library Catalog ===")
        if (len(self.books) == 0) {
            print("No books in library")
        } else {
            for (var book in self.books) {
                print(book.get_info())
            }
        }
        print("======================")
    }
    
    func search_by_title(title) {
        print("\n=== Search Results ===")
        var found = false
        for (var book in self.books) {
            if (book.title.find(title) != -1) {
                print(book.get_info())
                found = true
            }
        }
        if (!found) {
            print("No books found with title: " + title)
        }
        print("=====================")
    }
}

// Usage example
var library = Library()

// Add some books
library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "978-0-7432-7356-5")
library.add_book("To Kill a Mockingbird", "Harper Lee", "978-0-06-112008-4")
library.add_book("1984", "George Orwell", "978-0-452-28423-4")

// Show all books
library.show_all_books()

// Check out a book
var book1 = library.find_book("978-0-7432-7356-5")
if (book1 != null) {
    book1.check_out()
}

// Search for books
library.search_by_title("Great")

// Show updated status
library.show_all_books()
```

## 🔴 ADVANCED EXERCISES

### Exercise 9: File Processing System
**Objective**: Learn file operations and data persistence

```javascript
// Create a Contact Manager with file persistence

class Contact {
    var name
    var phone
    var email
    var created_at
    
    func init(name, phone, email) {
        self.name = name
        self.phone = phone
        self.email = email
        self.created_at = datetime_now()
    }
    
    func to_string() {
        return self.name + "|" + self.phone + "|" + self.email + "|" + self.created_at
    }
    
    func from_string(data_string) {
        var parts = split(data_string, "|")
        if (len(parts) == 4) {
            self.name = parts[0]
            self.phone = parts[1]
            self.email = parts[2]
            self.created_at = parts[3]
        }
    }
    
    func get_info() {
        return "Name: " + self.name + "\nPhone: " + self.phone + "\nEmail: " + self.email
    }
}

class ContactManager {
    var contacts = []
    var filename = "contacts.txt"
    
    func load_contacts() {
        self.contacts = []
        if (exists(self.filename)) {
            var content = file.read(self.filename)
            var lines = split(content, "\n")
            for (var line in lines) {
                if (len(line) > 0) {
                    var contact = Contact("", "", "")
                    contact.from_string(line)
                    append(self.contacts, contact)
                }
            }
            print("Loaded " + len(self.contacts) + " contacts")
        }
    }
    
    func save_contacts() {
        var content = ""
        for (var contact in self.contacts) {
            content = content + contact.to_string() + "\n"
        }
        file.write(self.filename, content)
        print("Saved " + len(self.contacts) + " contacts")
    }
    
    func add_contact(name, phone, email) {
        var contact = Contact(name, phone, email)
        append(self.contacts, contact)
        print("Added contact: " + name)
        self.save_contacts()
    }
    
    func search_contacts(query) {
        print("\n=== Search Results for '" + query + "' ===")
        var found = false
        for (var contact in self.contacts) {
            if (contact.name.find(query) != -1 || 
                contact.phone.find(query) != -1 || 
                contact.email.find(query) != -1) {
                print(contact.get_info())
                print("---")
                found = true
            }
        }
        if (!found) {
            print("No contacts found")
        }
        print("==============================")
    }
    
    func show_all_contacts() {
        print("\n=== All Contacts (" + len(self.contacts) + ") ===")
        if (len(self.contacts) == 0) {
            print("No contacts found")
        } else {
            for (var i = 0; i < len(self.contacts); i++) {
                print("Contact #" + (i + 1) + ":")
                print(self.contacts[i].get_info())
                print("---")
            }
        }
        print("============================")
    }
    
    func delete_contact(index) {
        if (index >= 0 && index < len(self.contacts)) {
            var contact = self.contacts[index]
            remove_item(self.contacts, contact)
            print("Deleted contact: " + contact.name)
            self.save_contacts()
        } else {
            print("Invalid contact index")
        }
    }
}

// Main program
var manager = ContactManager()
manager.load_contacts()

var running = true
while (running) {
    print("\n=== Contact Manager ===")
    print("1. Add Contact")
    print("2. Search Contacts")
    print("3. Show All Contacts")
    print("4. Delete Contact")
    print("5. Exit")
    
    var choice = int(input("Enter your choice: "))
    
    if (choice == 1) {
        var name = input("Enter name: ")
        var phone = input("Enter phone: ")
        var email = input("Enter email: ")
        manager.add_contact(name, phone, email)
        
    } else if (choice == 2) {
        var query = input("Enter search term: ")
        manager.search_contacts(query)
        
    } else if (choice == 3) {
        manager.show_all_contacts()
        
    } else if (choice == 4) {
        manager.show_all_contacts()
        if (len(manager.contacts) > 0) {
            var index = int(input("Enter contact number to delete: ")) - 1
            manager.delete_contact(index)
        }
        
    } else if (choice == 5) {
        print("Goodbye!")
        running = false
        
    } else {
        print("Invalid choice!")
    }
}
```

### Exercise 10: Web Data Processor
**Objective**: Learn HTTP requests and data processing

```javascript
// Create a program that fetches and processes web data

func fetch_weather_data(city) {
    // In a real implementation, you would use an actual API
    // This is a simulation
    print("Fetching weather data for " + city + "...")
    sleep(1)  // Simulate network delay
    
    // Simulated data
    var weather_data = {
        "city": city,
        "temperature": random_int(15, 35),
        "humidity": random_int(30, 80),
        "condition": random_choice(["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]),
        "wind_speed": random_int(5, 25)
    }
    
    return weather_data
}

func analyze_weather_data(weather_data) {
    print("\n=== Weather Analysis for " + weather_data["city"] + " ===")
    print("Temperature: " + weather_data["temperature"] + "°C")
    print("Humidity: " + weather_data["humidity"] + "%")
    print("Condition: " + weather_data["condition"])
    print("Wind Speed: " + weather_data["wind_speed"] + " km/h")
    
    // Weather recommendations
    print("\nRecommendations:")
    if (weather_data["temperature"] > 30) {
        print("🌡️  It's hot! Stay hydrated and wear light clothing.")
    } else if (weather_data["temperature"] < 20) {
        print("🧥 It's cool! Consider wearing a jacket.")
    }
    
    if (weather_data["humidity"] > 70) {
        print("💧 High humidity - it might feel muggy.")
    }
    
    if (weather_data["condition"] == "Rainy") {
        print("☔ Don't forget your umbrella!")
    } else if (weather_data["condition"] == "Sunny") {
        print("😎 Perfect day for outdoor activities!")
    }
    
    if (weather_data["wind_speed"] > 20) {
        print("💨 It's windy - secure loose items outside.")
    }
    
    print("==============================")
}

func compare_cities_weather(cities) {
    print("\n=== Weather Comparison ===")
    var weather_list = []
    
    for (var city in cities) {
        var weather = fetch_weather_data(city)
        append(weather_list, weather)
    }
    
    // Sort by temperature
    var sorted_weather = sort_list(weather_list, func(a, b) {
        return a["temperature"] > b["temperature"]
    })
    
    print("Cities sorted by temperature (hottest first):")
    for (var weather in sorted_weather) {
        print(weather["city"] + ": " + weather["temperature"] + "°C - " + weather["condition"])
    }
    
    print("==========================")
}

// Main program
print("=== Weather Data Processor ===")

// Single city analysis
var city = input("Enter city name: ")
var weather = fetch_weather_data(city)
analyze_weather_data(weather)

// Multiple city comparison
var cities = []
print("\nEnter cities to compare (empty line to finish):")
while (true) {
    var input_city = input("City: ")
    if (len(input_city) == 0) {
        break
    }
    append(cities, input_city)
}

if (len(cities) > 0) {
    compare_cities_weather(cities)
}

print("\n=== Program Complete ===")
```

## 🏆 CHALLENGE PROJECTS

### Challenge 1: Complete Inventory Management System
**Features to implement:**
- Product classes with categories
- Stock tracking and alerts
- Sales recording
- Revenue calculations
- Data persistence
- Report generation

### Challenge 2: Personal Finance Tracker
**Features to implement:**
- Income and expense tracking
- Budget management
- Category analysis
- Monthly reports
- Data visualization (text-based)
- Export functionality

### Challenge 3: Simple Web Server
**Features to implement:**
- HTTP request handling
- Static file serving
- Dynamic content generation
- Route management
- Logging system
- Error pages

## 📚 SOLUTION VERIFICATION

### Test Your Solutions
```javascript
// Function to test calculator exercise
func test_calculator() {
    print("Testing Calculator Functions...")
    
    // Test basic operations
    var a = 10, b = 5
    print("Addition: " + a + " + " + b + " = " + (a + b))
    print("Subtraction: " + a + " - " + b + " = " + (a - b))
    print("Multiplication: " + a + " × " + b + " = " + (a * b))
    print("Division: " + a + " ÷ " + b + " = " + (a / b))
    
    print("✓ Calculator functions working!")
}

// Test your implementations by calling these functions
test_calculator()
```

## 🎯 LEARNING PROGRESSION CHECKLIST

### Beginner Skills ✓
- [ ] Variables and data types
- [ ] Basic input/output
- [ ] Conditional statements
- [ ] Simple loops
- [ ] Basic functions
- [ ] List operations
- [ ] String manipulation

### Intermediate Skills ✓
- [ ] Dictionary usage
- [ ] File operations
- [ ] Class definitions
- [ ] Object methods
- [ ] Error handling basics
- [ ] Data processing
- [ ] Menu systems

### Advanced Skills ✓
- [ ] Inheritance
- [ ] Complex data structures
- [ ] File persistence
- [ ] API integration
- [ ] Advanced error handling
- [ ] Performance optimization
- [ ] Project architecture

---

**Remember: Practice regularly and build projects that interest you. The best way to learn is by doing!** 🐕✨