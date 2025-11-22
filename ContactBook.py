# ---------------------------------------------------------
# This Contact Book allows users to:
# - Add and save contacts to CSV
# - Display contacts in tabular form
# - Search, update, delete contacts
# - Export contacts to JSON & load them back
# - Log errors into error_log.txt
# ---------------------------------------------------------

import csv
import json
from datetime import datetime

CSV_FILE = "contacts.csv"
JSON_FILE = "contacts.json"
ERROR_FILE = "error_log.txt"

# ------------ Error Logger ----------------
def log_error(message):
    with open(ERROR_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

# ------------ TASK 1: Intro Message ----------------
def welcome_message():
    print("Welcome to the Contact Book Manager!")
    print("You can add, view, search, update and delete contacts.\n")

# ------------ TASK 2: Add & Save Contacts ----------------
def add_contact():
    try:
        name = input("Enter the Name: ")
        phone = input("Enter the Phone Number: ")
        email = input("Enter the Email: ")

        contact = {"name": name, "phone": phone, "email": email}

        # Append contact to CSV
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "phone", "email"])
            if file.tell() == 0:     # write header only if file empty
                writer.writeheader()
            writer.writerow(contact)

        print("Contact saved successfully!\n")

    except Exception as e:
        log_error(f"Add Contact Error: {e}")
        print("Error saving contact.")

# ------------ TASK 3: Read & Display Contacts ----------------
def display_contacts():
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.DictReader(file)
            contacts = list(reader)

            if not contacts:
                print("No contacts found!\n")
                return

            print("\nName\t\tPhone\t\tEmail")
            print("-" * 50)

            for c in contacts:
                print(f"{c['name']:<10}\t{c['phone']:<12}\t{c['email']}")

            print()

    except FileNotFoundError:
        log_error("Display Error: contacts.csv missing")
        print("No contacts found. File missing.\n")

    except Exception as e:
        log_error(f"Display Error: {e}")
        print("Error reading contacts.\n")

# ------------ TASK 4: Search Contact ----------------
def search_contact():
    name = input("Enter name to search: ")

    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.DictReader(file)

            for c in reader:
                if c["name"].lower() == name.lower():
                    print("\nContact Found:")
                    print(f"Name: {c['name']}")
                    print(f"Phone: {c['phone']}")
                    print(f"Email: {c['email']}\n")
                    return

            print("Contact not found.\n")

    except Exception as e:
        log_error(f"Search Error: {e}")
        print("Error searching contact.\n")

# ------------ Update Contact ----------------
def update_contact():
    name = input("Enter name to update: ")

    try:
        contacts = []
        found = False

        with open(CSV_FILE, "r") as file:
            reader = csv.DictReader(file)
            contacts = list(reader)

        for c in contacts:
            if c["name"].lower() == name.lower():
                found = True
                print("Leave field empty to keep old value.")
                new_phone = input("New Phone: ")
                new_email = input("New Email: ")

                if new_phone:
                    c["phone"] = new_phone
                if new_email:
                    c["email"] = new_email
                break

        if not found:
            print("Contact not found.\n")
            return

        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "phone", "email"])
            writer.writeheader()
            writer.writerows(contacts)

        print("Contact updated successfully!\n")

    except Exception as e:
        log_error(f"Update Error: {e}")
        print("Error updating contact.\n")

# ------------ Delete Contact ----------------
def delete_contact():
    name = input("Enter name to delete: ")

    try:
        contacts = []

        with open(CSV_FILE, "r") as file:
            reader = csv.DictReader(file)
            contacts = list(reader)

        new_list = [c for c in contacts if c["name"].lower() != name.lower()]

        if len(new_list) == len(contacts):
            print("Contact not found.\n")
            return

        # Rewrite CSV
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "phone", "email"])
            writer.writeheader()
            writer.writerows(new_list)

        print("Contact deleted successfully!\n")

    except Exception as e:
        log_error(f"Delete Error: {e}")
        print("Error deleting contact.\n")

# ------------ TASK 5: Save contacts to JSON ----------------
def export_to_json():
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.DictReader(file)
            contacts = list(reader)

        with open(JSON_FILE, "w") as f:
            json.dump(contacts, f, indent=4)

        print("Contacts exported to JSON successfully!\n")

    except Exception as e:
        log_error(f"JSON Export Error: {e}")
        print("Error exporting to JSON.\n")

# ------------ Load contacts from JSON ----------------
def load_from_json():
    try:
        with open(JSON_FILE, "r") as f:
            contacts = json.load(f)

        print("\nContacts from JSON:")
        for c in contacts:
            print(f"{c['name']} - {c['phone']} - {c['email']}")
        print()

    except Exception as e:
        log_error(f"JSON Load Error: {e}")
        print("Error loading JSON file.\n")

# ------------ Main Menu ----------------
def menu():
    welcome_message()

    while True:
        print("1. Add Contact")
        print("2. Display Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Export to JSON")
        print("7. Load from JSON")
        print("8. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            display_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            export_to_json()
        elif choice == "7":
            load_from_json()
        elif choice == "8":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.\n")

# ------------ Run Program ----------------
menu()


