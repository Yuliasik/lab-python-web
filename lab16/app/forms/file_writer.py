import json

from .forms import Form


class FileWriter:
    def formatJSON(self, form: Form):
        data = {
            form.login.data: {
                "login": form.login.data,
                "password": form.password.data,
                "e_number": form.e_number.data,
                "e_pin": form.e_pin.data,
                "e_year": form.e_year.data,
                "d_series": form.d_series.data,
                "d_number": form.d_number.data
            },
        }
        return data

    def write_to_file(self, form: Form):
        data = self.formatJSON(form)
        try:
            with open('data.json') as f:
                data_from_file = json.load(f)
                data_from_file.update(data)

                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data_from_file, f, ensure_ascii=False, indent=4)
        except:
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
