import json

# Load Tatyana's career information
with open("career.json", "r", encoding="utf-8") as file:
    career_data = json.load(file)


def find_answer(question):
    question = question.lower()

    if "siemens" in question:
        return career_data[1]["answer"]

    if "background" in question or "career" in question:
        return career_data[0]["answer"]

    if "project" in question or "ownership" in question:
        return career_data[2]["answer"]

    if "skills" in question or "strengths" in question:
        return career_data[3]["answer"]

    if "ai" in question or "automation" in question:
        return career_data[4]["answer"]

    return "I don't have an answer to that question yet."


# Welcome screen
print("\n" + "=" * 55)
print("                 ASK TATYANA")
print("=" * 55)

print("\nGet to know Tatyana's experience beyond her CV.\n")

print("You can ask me about:\n")

print("1. Tatyana's professional background")
print("2. Her experience at Siemens Healthineers")
print("3. Projects she has worked on")
print("4. Her strongest skills")
print("5. Her interest in AI and automation")

print("\nYou can also type your own question.")
print("Type 'exit' to leave.")


while True:

    question = input("\nRecruiter's question: ")

    # Exit
    if question.lower() == "exit":
        print("\nThank you for your interest in Tatyana. Goodbye!")
        break

    # Number selections
    if question == "1":
        answer = career_data[0]["answer"]

    elif question == "2":
        answer = career_data[1]["answer"]

    elif question == "3":
        answer = career_data[2]["answer"]

    elif question == "4":
        answer = career_data[3]["answer"]

    elif question == "5":
        answer = career_data[4]["answer"]

    # Free-text question
    else:
        answer = find_answer(question)

    print("\n" + answer)