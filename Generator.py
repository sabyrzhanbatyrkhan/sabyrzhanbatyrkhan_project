from random import randint

password_elements = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*"
isCreated = False

def main():
  ask_command = input("Write a command: ")
  while True: 
    if "exit" in ask_command:
      break
    elif "generate" in ask_command and "check" in ask_command:
      print("Write one specific command!")
    elif "generate" in ask_command:
      ask_length = input("White an length of password: ")
      while not ask_length.isdigit():
        print("Uncorrect value")
        ask_length = input("White an length of password: ")
      ask_length = int(ask_length)
      password = generate_password(ask_length)
      print("Your new password:",password)
    elif "check" in ask_command:
      if isCreated:
        check_password(password)
      else:
        print("Generate a password first!")
    else:
      print("Uncorrect command")
    ask_command = input("Write a command: ")

def generate_password(length):
  global isCreated
  new_password = ""
  for _ in range(length):
    random_element = randint(0,43)
    new_password += password_elements[random_element]
  isCreated = True
  return str(new_password)
    
def check_password(password):
  has_letter = any(char.isalpha() for char in password)
  has_digit = any(char.isdigit() for char in password)
  has_specific = any(char in "!@#$%^&*" for char in password)
  if password.isalpha() or len(password) < 8 or password.isdigit():
    print("Status: Weak")
  elif len(password) >= 10 and has_letter and has_digit and has_specific:
    print("Status: Strong")
  else:
    print("Status: Medium")


main()