try:
    from main import app
    import unittest

except Exception as e:
    print("Some Modules are Missing {}".format(e))


class FlaskTest(unittest.TestCase):
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
        self.assertEqual(response.content_type, "application/json")


if __name__ == "__main__":
    unittest.main()
