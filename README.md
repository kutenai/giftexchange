# Gift Exchange

Read in a list of people. Each line can contain a single person, or a couple
Couples are identified by:

    Jane and Bob
    Jack and Jill
    
The couples are then eliminated from drawing for each other.

A single person is added with a simple:

    Ellen
    Janie
    
    
These can be mixed

    Jane and Bob
    Ellen
    Jack and Jill
    Janie
    
# History files

History file contain the previous year's draw, as a Name: Name pair

    Jack: Jane
    Bob: Jill
    Ellen: Janie
    
You can include 0 or more history files. And files included will exclude the pair from being drawn again.
Note that if you are too restrictive, you won't be able to easily find a set of possible combinations.


# Running the program

Run the program like this

    python giftexchange.py peeps.txt --history file1 [file2]

Example

    python giftexchange.py peeps.txt --history 2017_draw.txt 2018_draw.txt | tee 2019_draw.txt


    
    
    