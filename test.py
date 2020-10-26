try:
    from main import app
    import unittest
    import pprint
    import json
    from dictor import dictor
except Exception as e:
    print("Some Modules are Missing".format(e))

try:

    class funcionality_check(unittest.TestCase):
        # ? Check for response 200
        def test_status_code(self):
            tester = app.test_client(self)
            response = tester.get("/name/%s/%s")
            statuscode = response.status_code

            print("Status Code = ", statuscode)

            self.assertEqual(statuscode, 200)

        # ? Check if response type is JSON
        def test_response_type_is_json(self):
            tester = app.test_client(self)
            response = tester.get("/name/%s/%s")
            content_type = response.content_type
            print("Content Type = ", content_type)

            self.assertEqual(response.content_type, "application/json")

    class name_matching_test(unittest.TestCase):
        global pass_test_name_1, pass_test_name_2, fail_test_name_1, fail_test_name_2
        pass_test_name_1 = "John"
        pass_test_name_2 = "J1Ohm"
        fail_test_name_1 = "John"
        fail_test_name_2 = "Jacob"

        # ? Check if levenshtein passes test cases
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

        # ? Check if levenshtein fails test case
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
                "[Failed]levenshtein distance [%d] between '%s' and '%s'"
                % (levenshtein_distance, fail_test_name_1, fail_test_name_2)
            )

            self.assertEqual(assertion_levenshtein_distance, 0)

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
                "[Success] Soundex representation is '%s'[%s] and '%s'[%s]"
                % (soundex_name_1, pass_test_name_1, soundex_name_2, pass_test_name_2)
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
                "[Failed] Soundex representation is '%s'[%s] and '%s'[%s]"
                % (soundex_name_1, fail_test_name_1, soundex_name_2, fail_test_name_2)
            )
            self.assertEqual(assertioin_soundex_represent, 0)


except Exception as e:
    print("Something went wrong!!".format(e))


if __name__ == "__main__":
    unittest.main()
