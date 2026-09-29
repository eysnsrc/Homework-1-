from pathlib import Path

LOG = Path(__file__).parents[1] / "datasets" / "auth.log"


def parse_line(line: str) -> dict:
    parts = line.strip().split()

    data = {
        "timestamp": parts[0]
    }

    for item in parts[1:]:
        key, value = item.split("=", 1)
        data[key] = value

    return data


def main():
    status_counts = {
        "SUCCESS": 0,
        "FAILED": 0
    }

    failed_ips = {}

    with open(LOG, "r", encoding="utf-8") as file:
        for line in file:

            if not line.strip():
                continue

            record = parse_line(line)

            status = record["status"]
            status_counts[status] += 1

            if status == "FAILED":
                ip = record["src_ip"]

                if ip in failed_ips:
                    failed_ips[ip] += 1
                else:
                    failed_ips[ip] = 1

    if failed_ips:
        top_failed_ip = max(failed_ips.items(), key=lambda x: x[1])
    else:
        top_failed_ip = None

    print("Status counts:", status_counts)
    print("Top failed IP:", top_failed_ip)


if __name__ == "__main__":
    main()
    