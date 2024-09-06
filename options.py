def options(args, question):
    while True:
        userinput = input(question)
        try:
            userinput = int(userinput) - 1
            if 0 <= userinput < len(args):
                return args[userinput]
            else:
                print("Invalid option, Please try again.")
        except ValueError:
            print("Invalid option, Please try again.")

op = options(["Option 1", "Option 2"], "Choose an option:\n>> ")
print(op)
