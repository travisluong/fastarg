#Run hello world:
    
python3 main.py hello_world foo

#Show help text for todo subcommand:
    
python3 main.py todo -h
    
#Show help text for a subcommand:

python3 main.py todo update_todo -h

#Run create_todo subcommand:

python3 main.py todo create_todo "drink water"

#Run create_todo with optional completed flag:

python3 main.py todo create_todo "drink water" --completed
python3 main.py todo create_todo "drink water" --no-completed

#Run the nested create_address command:

python3 main.py user address create_address 123 "456 main st" --city bellevue --state wa --zip 98004