# JsonCsvConverter
A program to transform a json file into csv and vice versa.
Quellcode of this project can be found [here](https://github.com/Treach96/JsonCsvConverter)



## Setup
Tk is used to select file.
In order to use Tk, if not already installed use following code:
<br><br>
``
sudo apt-get install python3-tk
``

## Test files
I used www.mockaroo.com to create json and csc files.

# Description
The program will ask the user for a file, either json or csv.<br>
Then it will check the filetype and parse the filepath to either **jsonHandler** or **csvHandler**.<br><br>
Both handler will ask the user for certain choices how to proceed with the file.<br>
After adjusting the value of a key, he gets asked how to save the file.<br>
He can choose **json** or **csv**. After that, he will be stuck in a loop to make further adjustments to the file. <br>
The user can exit the loops by typing **exit**.<br>

<hr>

### Notice
If saving the file in another format like json to csv or csv to json,<br> the filename gets **from_json** or **from_csv** appended!