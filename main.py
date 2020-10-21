from unicodedata import normalize
from flask import Flask, request, jsonify
from flask.json import htmlsafe_dump
from flask_restful import Api, Resource, reqparse, abort
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import enchant
import re
import unicodedata
import jellyfish
import json

app = Flask(__name__)
api = Api(app)

names_put_args = reqparse.RequestParser()
names_put_args.add_argument("raw_input_name1", type=str, required=True)
names_put_args.add_argument("raw_input_name2", type=str, required=True)

# ? Clean the name by removing all special characters and other unicode symbols
def filter_unicode_characters(data):
    name_in_ascii = unicodedata.normalize("NFKD", data).encode("ASCII", "ignore")
    filtered_name = name_in_ascii.decode("utf-8")
    filtered_name = filtered_name.lower()
    filtered_name = re.sub("[^A-Za-z]+", "", filtered_name)
    filtered_name = re.sub(" +", "", filtered_name)
    return filtered_name


# ? Sort the first name and last name alphabetically
def sort_words(input_name):
    input_name = input_name.split(" ")
    input_name.sort()
    sorted_name = " ".join(input_name)
    return sorted_name


# ? Find the soundex value for the cleaned word
def soundex(filtered_name: str):
    soundex_representation = jellyfish.soundex(filtered_name)
    return soundex_representation


class name_matching(Resource):
    def get(self, raw_input_name1, raw_input_name2):
        try:
            raw_input_name1 = sort_words(raw_input_name1)
            raw_input_name2 = sort_words(raw_input_name2)
            filtered_name_1 = filter_unicode_characters(raw_input_name1)
            filtered_name_2 = filter_unicode_characters(raw_input_name2)
            soundex_representation_name1 = soundex(filtered_name_1)
            soundex_representation_name2 = soundex(filtered_name_2)
            levenshtein_distance = enchant.utils.levenshtein(
                filtered_name_1.lower(), filtered_name_2.lower()
            )
            if (
                levenshtein_distance <= 2
                or soundex_representation_name1 == soundex_representation_name2
            ):
                status = True
                message = "The names match"
            else:
                status = False
                message = "The names do not match"
            json_response = {
                "raw_input": {"name_1": raw_input_name1, "name_2": raw_input_name2},
                "filtered_input": {
                    "name_1": filtered_name_1,
                    "name_2": filtered_name_2,
                },
                "levenshtein_distance": levenshtein_distance,
                "soundex_representaion": {
                    "name_1": soundex_representation_name1,
                    "name_2": soundex_representation_name2,
                },
                "status": status,
                "message": message,
            }
            return jsonify(json_response)

        except Exception as e:
            print(e)
            return Response(
                response=json.dumps(
                    {"message": "Check Your URL Please!!"}, default=str
                ),
                status=404,
                mimetype="application/json",
            )


api.add_resource(
    name_matching, "/name/<string:raw_input_name1>" + "/<string:raw_input_name2>"
)
if __name__ == "__main__":
    app.run(debug=True)
