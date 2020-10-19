# **Name Matching Rest API**
This a flask-RESTful API for name matching using fuzzyuzzy library and soundex
The entire AIP is contained in a single file called main.py python file

The requirements.txt contains the all the required library and files to be installed before running the api.

## **Installation of requirements**
The requirements file can be executed by using the command,
```
pip3 install -r requirements.txt
```
A local server can be started by running the main.py file by typing the command,
```
python3 main.py
```
# **The working of the REST API**

## Request
```
GET /name/raw_input_name1/raw_input_name2
```
## **Response**
```
{
    "filtered_input": {
        "name_1": "filtered_name_1",
        "name_2": "filtered_name_2"
    },
    "levenshtein_distance": value,
    "message": "string",
    "raw_input": {
        "name_1": "raw_input_name1",
        "name_2": "raw_input_name2"
    },
    "soundex_representaion": {
        "name_1": "soundex_1",
        "name_2": "Soundex_2"
    },
    "status": true/false
}
```