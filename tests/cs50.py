class Student:
    def __init__(self, name, house):
        if not name: # Check if name is empty
            raise ValueError("Missing name") # Raise an error if name is empty
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house") # Raise an error if house is not valid
        self.name= name
        self.house= house

def main():
    student= get_student()
    #tuple object does not support item assignment, it's immutable
    #student[0]= "John"
    #student['name']= "John"
    #print(f"studen {student[0]} from {student[1]}")
    print(f"student {student.name} from {student.house}")

    # print(f"student {student['name']} from {student['house']}")

def get_student():
    # name= input("Name: ")
    # house= input("House: ")
    #return (name, house) # Returning a tuple
    #return name, house # This is also a tuple
    # return [name, house] # This is a list, mutable
    # student= {} # This is a dictionary
    # student["name"]= input("name: ") #assign a value to a key
    # student["house"]= input("house: ") #assign a value to a key

    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)

    # return {
    #     "name":name,
    #     "house":house
    # } # Returning a dictionary, it's mutable

if __name__ == "__main__":
    main()