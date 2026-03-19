import json

def build():
    try:
        with open("scp_list.json", "r", encoding="utf-8") as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    try:
        with open("archives_template.html", "r", encoding="utf-8") as f:
            template = f.read()
    except Exception as e:
        print(f"Error reading template: {e}")
        return

    injection = f"const scpData = {data};"
    output = template.replace("// DATA_INJECTION_POINT", injection)

    output_filename = "archives.html"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Successfully generated {output_filename}")
    except Exception as e:
        print(f"Error writing output: {e}")

if __name__ == "__main__":
    build()
