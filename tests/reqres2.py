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
    def get_user(self):

        with self.client.get("/api/users/2", catch_response=True) as response:

            if self.expected_get_statuscode == response.status_code and self.expected_get_response_text in response.text:
                logging.info("GET REQUEST FILE2 PASSED")
                response.success()
            else:
                logging.error("GET REQUEST FILE2 FAILED")
                response.failure()

    @task
    @tag('POSITIVE_TEST')
    def post_user(self):

        with self.client.post("/api/users/2", catch_response=True, data='''{
        "name": "morpheus",
        "job": "leader"
        }''') as response:

            if self.expected_post_response_text in response.text and self.expected_post_statuscode == response.status_code:
                logging.info("POST REQUEST FILE2 PASSED")
                response.success()
            else:
                logging.error("POST REQUEST FILE2 FAILED")
                response.failure()

    @task
    @tag('POSITIVE_TEST')
    def patch_user(self):

        with self.client.patch("/api/users/2", catch_response=True, data='''{
       "name": "morpheus",
       "job": "zion resident"
       }''') as response:

            if self.expected_patch_response_text in response.text and self.expected_patch_statuscode == response.status_code:
                logging.info("PATCH REQUEST FILE2 PASSED")
                response.success()
            else:
                logging.error("PATCH REQUEST FILE2 FAILED")
                response.failure()

    @task
    @tag('POSITIVE_TEST')
    def delete_user(self):

        with self.client.delete("/api/users/2", catch_response=True) as response:

            if self.expected_delete_statuscode == response.status_code:
                logging.info("DELETE REQUEST FILE2 PASSED")
                response.success()
            else:
                logging.error("DELETE REQUEST FILE2 FAILED")
                response.failure()


class TestsRequests2(HttpUser):
    tasks = [TasksRequests]
    wait_time = between(2, 5)
