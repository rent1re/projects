# This script demonstrates basic Python concepts

# Variables and data types
name = "Alice"
age = 30
is_student = True

# Lists
fruits = ["apple", "banana", "cherry"]

# Dictionaries
person = {
    "name": "Bob",
    "age": 25,
    "city": "New York"
}

# Functions
def greet(name):
    return f"Hello, {name}!"

# Loops
for fruit in fruits:
    print(f"I like {fruit}")

# Conditional statements
if age > 18:
    print(f"{name} is an adult.")
else:
    print(f"{name} is a minor.")

# Function call
print(greet("Alice"))

# Working with dictionaries
# Print person's details
print(f"{person['name']} lives in {person['city']}.")

# Add a new key-value pair to the dictionary
person['occupation'] = 'Engineer'
print(f"{person['name']} works as an {person['occupation']}.")

# Update an existing value in the dictionary
person['age'] = 26
print(f"{person['name']} is now {person['age']} years old.")

# Remove a key-value pair from the dictionary
del person['city']
print(f"City information removed. Current dictionary: {person}")

# Iterate through dictionary keys and values
for key, value in person.items():
    print(f"{key}: {value}")

# Check if a key exists in the dictionary
if 'name' in person:
    print(f"Name is present in the dictionary: {person['name']}")

# Get a value with a default if the key doesn't exist
country = person.get('country', 'Unknown')
print(f"Country: {country}")

# Merge two dictionaries
additional_info = {'hobby': 'painting', 'pet': 'dog'}
person.update(additional_info)
print(f"Updated dictionary with additional info: {person}")

# Clear all items in the dictionary
person.clear()
print(f"Dictionary after clearing all items: {person}")