import json

from forms import LoginForm


class FileWriter:
    def formatJSON(self, form: LoginForm):
        data = {
            "login": form.login.data,
            "password": form.password.data,
            "e_number": form.e_number.data,
            "e_pin": form.e_pin.data,
            "e_year": form.e_year.data,
            "d_series": form.d_series.data,
            "d_number": form.d_number.data
        }
        return data

    def write_to_file(self, form: LoginForm):
        data = self.formatJSON(form)
        with open(form.login.data + '.json', 'w') as outfile:
            json.dump(data, outfile)
