from locust import HttpUser, task, SequentialTaskSet, between, tag
import logging


class TasksRequests(SequentialTaskSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_post_statuscode = 201
        self.expected_post2_statuscode = 400
        self.expected_get_statuscode = 200
        self.expected_get3_statuscode = 404
        self.expected_delete_statuscode = 204
        self.expected_patch_statuscode = 200
        self.expected_get_response_text = "janet.weaver@reqres.in"
        self.expected_patch_response_text = "updatedAt"
        self.expected_post_response_text = "id"
        self.expected_post2_response_text = "Missing email or username"
        self.response_id = ""

    @task
    @tag('POSITIVE_TEST')
    def get_user1(self):

        with self.client.get("/api/users/2", catch_response=True) as response:
            if self.expected_get_statuscode == response.status_code and self.expected_get_response_text in response.text:
                logging.info("GET REQUEST1 PASSED")
                response.success()
            else:
                logging.error("GET REQUEST1 FAILED")
                response.failure()

    @task
    @tag('NEGATIVE_TEST')
    def get_user2(self):
        expected_response_code = 404

        with self.client.get("/api/users/23", catch_response=True) as response:
            if expected_response_code == response.status_code:
                logging.info("GET REQUEST2 PASSED")
                response.success()
            else:
                logging.error("GET REQUEST2 FAILED")
                response.failure()

    @task
    @tag('POSITIVE_TEST')
    def post_user1(self):

        with self.client.post("/api/users/2", catch_response=True, data='''{
        "name": "morpheus",
        "job": "leader"
        }''') as response:

            json_var = response.json()
            response_id = json_var['id']
            self.response_id = response_id

            if self.expected_post_response_text in response.text and self.expected_post_statuscode == response.status_code:
                logging.info("POST REQUEST1 PASSED")
                response.success()
            else:
                logging.error("POST REQUEST1 FAILED")
                response.failure()

    @task
    @tag('NEGATIVE_TEST')
    def get_user3(self):

        with self.client.get("/api/users/"+self.response_id+"", catch_response=True) as response:

            if self.expected_get3_statuscode == response.status_code:
                logging.info("GET REQUEST3 PASSED")
                response.success()
            else:
                logging.error("GET REQUEST3 FAILED")
                response.failure()

    @task
    @tag('NEGATIVE_TEST')
    def post_user2(self):

        with self.client.post("/api/login", catch_response=True, data='''{
        "email": "peter@klaven"
        }''') as response:

            json_var = response.json()
            response_text = json_var['error']

            if self.expected_post2_response_text == response_text and self.expected_post2_statuscode == response.status_code:
                logging.info("POST REQUEST2 PASSED")
                response.success()
            else:
                logging.error("POST REQUEST2 FAILED")
                response.failure()

    @task
    @tag('POSITIVE_TEST')
    def patch_user(self):

        with self.client.patch("/api/users/2", catch_response=True, data='''{
       "name": "morpheus",
       "job": "zion resident"
       }''') as response:

            if self.expected_patch_response_text in response.text and self.expected_patch_statuscode == response.status_code:
                logging.info("PATCH REQUEST PASSED")
                response.success()
            else:
                logging.error("PATCH REQUEST FAILED")
                response.failure()

    @task
    @tag('POSITIVE_TEST')
    def delete_user(self):
        with self.client.delete("/api/users/2", catch_response=True) as response:
            if self.expected_delete_statuscode == response.status_code:
                logging.info("DELETE REQUEST PASSED")
                response.success()
            else:
                logging.error("DELETE REQUEST FAILED")
                response.failure()


class TestsRequests1(HttpUser):
    tasks = [TasksRequests]
    wait_time = between(2, 5)
