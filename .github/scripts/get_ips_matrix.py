import yaml
import json


def main():
    test_set_yaml = ".github/ip_set.yaml"
    output_matrix = {"ips": []}
    test_set_stream = open(test_set_yaml)
    data = yaml.load(test_set_stream, Loader=yaml.Loader)
    for item in data:
        name = item["name"]
        repo = item["repo"]
        fw = item.get("fw", "true")
        docs = item.get("fw", "true")
        bus_wrapper = item.get("bus_wrapper", "true")
        output_matrix["ips"].append(
            {
                "name": name,
                "repo": repo,
                "fw": fw,
                "docs": docs,
                "bus_wrapper": bus_wrapper,
            }
        )

    print(json.dumps(output_matrix))
    test_set_stream.close()


if __name__ == "__main__":
    main()
