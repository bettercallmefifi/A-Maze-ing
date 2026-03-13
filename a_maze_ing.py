import sys


def parse_config(file_config: str) -> dict:
    config = {}
    try:
        with open(file_config, "r") as file:
            for line in file:
                if not line.strip() or line.strip().startswith("#"):
                    continue
                part = line.split("=")
                key = part[0].strip()
                value = part[1].strip()
                config[key] = value
        for key in config:
            if key == "WIDTH":
                config[key] = int(config[key])
            elif key == "HEIGHT":
                config[key] = int(config[key])
            elif key == "ENTRY":
                parts = config[key].split(",")
                config[key] = (int(parts[0]), int(parts[1]))
            elif key == "EXIT":
                parts = config[key].split(",")
                config[key] = (int(parts[0]), int(parts[1]))
            elif key == "PERFECT":
                config[key] = config[key].lower() in ("true", "1", "yes")
            elif key == "SEED":
                config[key] = int(config[key])
        return config
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    config_file = sys.argv[1]
    config = parse_config(config_file)
    print(config)
