try:
    from main import app
    import unittest
    import pprint
    import json
    from dictor import dictor
    from mock import patch
    import requests
except Exception as e:
    print("Some Modules are Missing".format(e))

try:
    global pass_test_name_1, pass_test_name_2, fail_test_name_1, fail_test_name_2, empty_input_1, empty_input_2
    pass_test_name_1 = "John"
    pass_test_name_2 = "J1Ohm"
    fail_test_name_1 = "John"
    fail_test_name_2 = "Jacob"
    empty_input_1 = ""
    empty_input_2 = ""

    class url_funcionality_check(unittest.TestCase):
        # ? Check for response 200
        def test_status_code_get(self):
            tester = app.test_client(self)
            response = tester.get("/name/%s/%s")
            statuscode = response.status_code
            print("[Success]Status " + str(statuscode))
            self.assertEqual(statuscode, 200)

        # ? Response for POST requests
        def test_status_code_post(self):
            tester = app.test_client(self)
            response = tester.post("/name/%s/%s")
            statuscode = response.status_code
            print("[Success]POST method not allowed-" + str(statuscode))
            self.assertEqual(statuscode, 405)

        # ? Response for DELETE requests
        def test_status_code_post_delete(self):
            tester = app.test_client(self)
            response = tester.delete("/name/%s/%s")
            statuscode = response.status_code
            print("[Success]DELETE method not allowed-" + str(statuscode))
            self.assertEqual(statuscode, 405)

        # ? Check if response type is JSON
        def test_response_type_is_json(self):
            tester = app.test_client(self)
            response = tester.get("/name/%s/%s")
            content_type = response.content_type
            print("[Success]Content Type ", content_type)
            self.assertEqual(response.content_type, "application/json")

        # ? Check if the URL exists
        def test_returns_false_if_url_doesnt_exist(self):
            tester = app.test_client(self)
            url = "/"
            response = tester.get(url)
            statuscode = response.status_code
            print("[Success]URL doesn't exist!")
            self.assertEqual(statuscode, 404)

        # ? Check if URL has less than the required params
        def test_returns_false_if_url_not_found(self):
            tester = app.test_client(self)
            url = "/name/"
            response = tester.get(url)
            statuscode = response.status_code
            print("[Success]URL has less/no params!")
            self.assertEqual(statuscode, 404)

        # ? Check if URL has more than one params
        def test_returns_false_if_url_has_many_inputs(self):
            tester = app.test_client(self)
            url = "/name/" + fail_test_name_1
            response = tester.get(
                "/name/" + fail_test_name_1 + "/" + fail_test_name_2 + "/"
            )
            statuscode = response.status_code
            print("[Success]URL has too many params!")
            self.assertEqual(statuscode, 404)

    # ? Check test cases for levenshtein distance
    class test_levenshtein_diatance(unittest.TestCase):

        # ? Check if levenshtein distance works!
        def test_levenshtein_representation_success(self):
            tester = app.test_client(self)
            response = tester.get("/name/" + pass_test_name_1 + "/" + pass_test_name_2)
            data = json.loads(response.get_data(as_text=True))
            levenshtein_distance = data["levenshtein_distance"]
            message = data["message"]
            assertion_levenshtein_distance = 0
            if levenshtein_distance <= 2 and message == "The names match":
                assertion_levenshtein_distance = 1
            print(
                "[Success]levenshtein distance [%d] between '%s' and '%s'"
                % (levenshtein_distance, pass_test_name_1, pass_test_name_2)
            )
            self.assertEqual(assertion_levenshtein_distance, 1)

        # ? Check if levenshtein distance fails test case
        def test_levenshtein_representation_failure(self):
            tester = app.test_client(self)
            response = tester.get("/name/" + fail_test_name_1 + "/" + fail_test_name_2)
            data = json.loads(response.get_data(as_text=True))
            levenshtein_distance = data["levenshtein_distance"]
            message = data["message"]
            assertion_levenshtein_distance = 1
            if levenshtein_distance > 2 and message == "The names do not match":
                assertion_levenshtein_distance = 0
            print(
                "[Success]levenshtein distance [%d] between '%s' and '%s'"
                % (levenshtein_distance, fail_test_name_1, fail_test_name_2)
            )

            self.assertEqual(assertion_levenshtein_distance, 0)

        # ? Check if the levenshtein params are empty
        def test_levenshtein_representation_failure_no_params(self):
            tester = app.test_client(self)
            response = tester.get("/name/" + empty_input_1 + "/" + empty_input_2)
            assertion_levenshtein_distance = 1
            if empty_input_1 == "" or empty_input_2 == "":
                assertion_levenshtein_distance = 0
            print("[Success]Both Params are empty for levenshtein distance")
            self.assertEqual(assertion_levenshtein_distance, 0)

        # ? Check if the levenshtein first param is empty
        def test_levenshtein_distance_failure_empty_first_param(self):
            tester = app.test_client(self)
            response = tester.get("/name/" + empty_input_1 + "/" + pass_test_name_1)
            assertioin_soundex_represent = 1
            if empty_input_1 == "" or pass_test_name_1 == "":
                assertioin_soundex_represent = 0
            print("[Success]First Param is empty for levenshtein distance")
            self.assertEqual(assertioin_soundex_represent, 0)

        # ? Check if the levenshtein second param is empty
        def test_levenshtein_distance_failure_empty_second_param(self):
            tester = app.test_client(self)
            response = tester.get("/name/" + pass_test_name_2 + "/" + empty_input_2)
            assertioin_soundex_represent = 1
            if pass_test_name_2 == "" or empty_input_2 == "":
                assertioin_soundex_represent = 0
            print("[Success]Second Param is empty for levenshtein distance")
            self.assertEqual(assertioin_soundex_represent, 0)

    # ? Check test cases for soundex
    class test_soundex_representation(unittest.TestCase):
        # ? Test if Soundex passes the test case
        def test_soundex_representation_success(self):
            tester = app.test_client(self)
            response = tester.get("/name/" + pass_test_name_1 + "/" + pass_test_name_2)
            data = json.loads(response.get_data(as_text=True))
            soundex_name_1 = dictor(data, "soundex_representaion.name_1")
            soundex_name_2 = dictor(data, "soundex_representaion.name_2")
            message = data["message"]
            assertioin_soundex_represent = 0
            if soundex_name_1 == soundex_name_2 and message == "The names match":
                assertioin_soundex_represent = 1

            print(
                "[Success]Soundex representation is '%s'[%s] and '%s'[%s]"
                % (
                    soundex_name_1,
                    pass_test_name_1,
                    soundex_name_2,
                    pass_test_name_2,
                )
            )

            self.assertEqual(assertioin_soundex_represent, 1)

        # ? Check if Soundex fails the test case
        def test_soundex_representation_failure(self):
            tester = app.test_client(self)
            response = tester.get("/name/" + fail_test_name_1 + "/" + fail_test_name_2)
            data = json.loads(response.get_data(as_text=True))
            soundex_name_1 = dictor(data, "soundex_representaion.name_1")
            soundex_name_2 = dictor(data, "soundex_representaion.name_2")
            message = data["message"]
            assertioin_soundex_represent = 1
            if soundex_name_1 != soundex_name_2 and message == "The names do not match":
                assertioin_soundex_represent = 0
            print(
                "[Success]Soundex representation is '%s'[%s] and '%s'[%s]"
                % (
                    soundex_name_1,
                    fail_test_name_1,
                    soundex_name_2,
                    fail_test_name_2,
                )
            )
            self.assertEqual(assertioin_soundex_represent, 0)

        # ? Check is soundex params are empty!
        def test_soundex_representation_failure_empty_params(self):
            tester = app.test_client(self)
            response = tester.get("/name/" + empty_input_1 + "/" + empty_input_2)
            assertioin_soundex_represent = 1
            if empty_input_1 == "" or empty_input_2 == "":
                assertioin_soundex_represent = 0
            print("[Success]Both Params are empty for soundex representation")
            self.assertEqual(assertioin_soundex_represent, 0)

        # ? Check if first soundex param is empty
        def test_soundex_representation_failure_empty_first_param(self):
            tester = app.test_client(self)
            response = tester.get("/name/" + empty_input_1 + "/" + pass_test_name_1)
            assertioin_soundex_represent = 1
            if empty_input_1 == "":
                assertioin_soundex_represent = 0
            print("[Success]First Param is empty for soundex representation")
            self.assertEqual(assertioin_soundex_represent, 0)

        # ? Check is second soundex param is empty
        def test_soundex_representation_failure_empty_second_param(self):
            tester = app.test_client(self)
            response = tester.get("/name/" + pass_test_name_2 + "/" + empty_input_2)
            assertioin_soundex_represent = 1
            if empty_input_2 == "":
                assertioin_soundex_represent = 0
            print("[Success]Second Param is empty for soundex representation")
            self.assertEqual(assertioin_soundex_represent, 0)


except Exception as e:
    print("Something went wrong!!".format(e))


if __name__ == "__main__":
    unittest.main()
