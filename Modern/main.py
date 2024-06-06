from input_from_file import process_input_from_file
from input_from_terminal import process_input_from_terminal
from write import Write

def main():
    option = input("Enter 'F' for input from file or 'T' for input from terminal: ")
    if option.upper() == 'F':
        Write(process_input_from_file())
    elif option.upper() == 'T':
        Write(process_input_from_terminal())
    else:
        print("Invalid option. Please enter 'F' or 'T'.")

if __name__ == "__main__":
    main()
