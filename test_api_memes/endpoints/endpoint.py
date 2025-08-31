import allure


class Endpoint:
    url = 'http://memesapi.course.qa-practice.com/'
    response = None
    json = None
    headers = {'Content-Type': 'application/json'}

    @allure.step('Check that response is 200')
    def check_that_status_is_200(self):
        assert self.response.status_code == 200, '200 is not 200'

    @allure.step('Check that response is 401')
    def check_that_status_is_401(self):
         assert self.response.status_code == 401, '401 is not 401'

    @allure.step('Check that response is 400')
    def check_that_status_is_400(self):
        assert self.response.status_code == 400, '400 is not 400'

    @allure.step('Check that response is 403')
    def check_that_status_is_403(self):
        assert self.response.status_code == 403, '403 is not 403'

    @allure.step('Check that response is 404')
    def check_that_status_is_404(self):
        assert self.response.status_code == 404, '404 is not 404'
