import json

def build():
    try:
        with open("facilities.json", "r", encoding="utf-8") as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    try:
        with open("template.html", "r", encoding="utf-8") as f:
            template = f.read()
    except Exception as e:
        print(f"Error reading template: {e}")
        return

    try:
        with open("map_points.json", "r", encoding="utf-8") as f:
            map_data = f.read()
    except Exception as e:
        print(f"Error reading map points: {e}")
        map_data = "[]"

    injection = f"const facilitiesData = {data};\n        const mapPointsData = {map_data};"
    output = template.replace("// DATA_INJECTION_POINT", injection)

    output_filename = "Foundation Facilities - SCP Foundation.html"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Successfully generated {output_filename}")
    except Exception as e:
        print(f"Error writing output: {e}")

if __name__ == "__main__":
    build()
