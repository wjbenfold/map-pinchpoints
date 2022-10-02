import getdata
from read_config import get_config
import xml_to_pinchpoint_csv
from generate_outputs import generate_phone_csv, generate_wkt
from generate_html import generate_html

print("Loading config")

config = get_config()

print("Getting data")

getdata.main(config)

print("Finding pinchpoints")

xml_to_pinchpoint_csv.main(config)

print("Writing csv for phone")

generate_phone_csv(config)

print("Writing csv of wkts for google")

generate_wkt(config)

print("Writing html for phone")

generate_html(config)
