from src import load_response

prompt = input("Welcome to NLP. Seed! Your! Prompt! And see what you get back! \nYour Prompt: ")
response = load_response(prompt)

print(f'\nChat Bot says, \n"{response}"')
