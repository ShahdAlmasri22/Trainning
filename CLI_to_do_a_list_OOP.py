import PythonFundamentals

while True:
    print("\n------------------- Menu -------------------")
    print("Choose the topics that you need to know about")
    print("""
            1. Input / Output
            2. Data Types
            3. Casting
            4. String
            5. Conditional
            6. Loop
            7. OOP
            8. Context Managers
            9. Lambda
            10. Decorates
            11. Exit
    """)

    choice = int(input("Enter your choice: "))


    match choice:
        case 1:
            name = input("What's your name?")
            PythonFundamentals.InOut(name)

        case 2:
            print("------ Python Data Types ------")
            print("""
            1. Int
            2. Float
            3. String
            4. List
            5. Tuple
            6. Dict
            7. Set
            8. exit
            """)

            choice = int(input("Choose a data type: "))

            PythonFundamentals.DataTypes(choice)

        case 3:
            x=input("Enter any value that you want: ")
            PythonFundamentals.Casting(x)

        case 4:
            word = input("Enter any statement: ")

            print("\n--- String Operations ---")
            print("Length:", len(word))

            print("Uppercase:", word.upper())
            print("Lowercase:", word.lower())

            old = input("Enter word to replace: ")
            new = input("Enter new word: ")
            word = word.replace(old, new)
            print("After replace:", word)
            print("The result:", word.title())

            print("Strip spaces:", word.strip())

            print("Split words:", word.split())

            print("Count of 'a' =", word.count("a"))

            print("Starts with 'H' =", word.startswith("H"))

            print("Ends with 'n' =", word.endswith("n"))

        case 5:
            print("------ Comparing between x1 and x2 ------")
            x1= input("x1: ")
            x2 = input("x2: ")
            print("x1==x2:", x1 == x2)
            print("x1!=x2:", x1 != x2)
            print("x1<x2:", x1 < x2)

        case 6:
            arr = []
            n = int(input("To fill the array how many values do you want to enter? "))

            for i in range(n):
                value = input(f"Enter value {i + 1}: ")
                arr.append(value)

            print("The array is:", arr)

        case 7:
            print("Inheritance & Polymorphism")
            obj = PythonFundamentals.Dog()
            obj.sound()
            obj._onlyFprAnimals() # encapsulation (protected)

            print("Abstract")
            obj2= PythonFundamentals.Franch()
            obj2.regards()

            print("Static")
            res = PythonFundamentals.Calc.add(2, 3)
            print(res)

        case 8:
            with PythonFundamentals.ContextManager() as manager:
             print('in the block')

        case 9:
            lam= lambda x,y: x+y
            print("Ex. for lambda concept 3+2=", lam(3,2))

        case 10:
            print("Decorates ex to change the cases")
            ex=input("Enter any statement: ")
            print("The result: ",PythonFundamentals.fun(ex))

        case 11:
            print("Goodbye 👋")
            break

        case _:
            print("Invalid choice ❌")