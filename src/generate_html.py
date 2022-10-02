from jinja2 import Environment, FileSystemLoader
from read_config import get_config


def generate_python(config):

    environment = Environment(loader=FileSystemLoader("./templates"))
    template = environment.get_template(config["phone_html"]["python_template"])

    with open(config["outputs"]["phone_csv"]["output_filename_csv"], "r+") as fh:
        csv_data = fh.read()

    return template.render(csv_data=csv_data)


def generate_html(config):

    generated_python = generate_python(config)

    environment = Environment(loader=FileSystemLoader("./templates"))
    template = environment.get_template(config["phone_html"]["html_template"])

    with open(config["phone_html"]["output_filename_html"], "w+") as fh:
        fh.write(template.render(python_code=generated_python))


def main(config):
    generate_html(config)


if __name__ == "__main__":
    config = get_config()
    main(config)
