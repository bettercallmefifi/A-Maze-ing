from typing import Any, Dict, Tuple


class ConfigParser:
    """Parse and validate the maze configuration file."""

    REQUIRED_KEYS = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }
<<<<<<< HEAD
    OPTIONAL_KEY = {"SEED"}
=======
    OPTIONAL_KEY = {"SEED", "ALGORITHM"}
>>>>>>> 4ee574e (fixe all)

    def __init__(self, config_file: str) -> None:
        """Store the configuration file path."""
        self.config_file = config_file

    def validate_int(self, key: str, value: str) -> int:
        """Validate that a string is a non-negative integer."""
        try:
            value = int(value)
        except ValueError:
<<<<<<< HEAD
            raise ValueError(
                f"Invalid valid value for {key} (use integer value)")
=======
            raise ValueError(f"Invalid value for {key} (use integer value)")
>>>>>>> 4ee574e (fixe all)
        if value < 0:
            raise ValueError(f"Invalid value for {key} (use non-negative value)")
        return value

<<<<<<< HEAD
    def parse_cordinate(self, key: str, value: str) -> Tuple[int, int]:
=======
    def parse_coordinate(self, key: str, value: str) -> Tuple[int, int]:
>>>>>>> 4ee574e (fixe all)
        """Parse and validate coordinate values formatted as 'x,y'."""
        coordinates = value.split(",")
        if len(coordinates) != 2:
            raise ValueError(f"Invalid value for {key} (use x,y)")
        try:
<<<<<<< HEAD
            x = int(cordinates[0].strip())
            y = int(cordinates[1].strip())
        except ValueError:
            raise ValueError(
                f"Invalid value for {key} use integer values for (x,y)")
        if x < 0 or y < 0:
            raise ValueError(f"Invalid value for {key} use positive values")
=======
            x = int(coordinates[0].strip())
            y = int(coordinates[1].strip())
        except ValueError:
            raise ValueError(f"Invalid value for {key} (use integer values for x,y)")
        if x < 0 or y < 0:
            raise ValueError(f"Invalid value for {key} (use non-negative values)")
>>>>>>> 4ee574e (fixe all)
        return x, y

    def parse(self) -> Dict[str, Any]:
        """Read config file and return validated key/value data."""
        parsed_data: Dict[str, Any] = {}
        all_keys = self.REQUIRED_KEYS | self.OPTIONAL_KEY
        with open(self.config_file, "r") as file:
            for index, line in enumerate(file):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
<<<<<<< HEAD
                    raise ValueError(
                        f"invalid config line ({index + 1} ({line}))")
=======
                    raise ValueError(f"Invalid config line {index + 1}: {line}")
>>>>>>> 4ee574e (fixe all)
                key, value = line.split("=", 1)
                key = key.upper().strip()
                value = value.strip()
                if key not in all_keys:
<<<<<<< HEAD
                    raise ValueError(f"Invalid key value ({key})")
=======
                    raise ValueError(f"Invalid key ({key})")
                if key in parsed_data:
                    raise ValueError(f"Duplicate key ({key})")

>>>>>>> 4ee574e (fixe all)
                if key == "PERFECT":
                    cleaned_key = value.lower()
                    if cleaned_key in ["true", "false"]:
                        parsed_data[key] = cleaned_key == "true"
                    else:
                        raise ValueError("Invalid value for PERFECT key")
<<<<<<< HEAD
                elif key in ["WIDTH", "HEIGHT", "SEED"]:
                    parsed_data[key] = self.validate_int(key, value)
                elif key in {"ENTRY", "EXIT"}:
                    parsed_data[key] = self.parse_cordinate(key, value)
=======
                elif key == "ALGORITHM":
                    cleaned_algorithm = value.upper()
                    if cleaned_algorithm not in {"DFS", "PRIM"}:
                        raise ValueError("Invalid value for ALGORITHM key (use DFS or PRIM)")
                    parsed_data[key] = cleaned_algorithm
                elif key in ["WIDTH", "HEIGHT", "SEED"]:
                    parsed_data[key] = self.validate_int(key, value)
                elif key in {"ENTRY", "EXIT"}:
                    parsed_data[key] = self.parse_coordinate(key, value)
>>>>>>> 4ee574e (fixe all)
                else:
                    if not value:
                        raise ValueError("Invalid value for OUTPUT_FILE (cannot be empty)")
                    parsed_data[key] = value

            for required in self.REQUIRED_KEYS:
                if required not in parsed_data:
                    raise ValueError(f"Missing key {required}")

            width = parsed_data["WIDTH"]
            height = parsed_data["HEIGHT"]
            entry = parsed_data["ENTRY"]
            exit = parsed_data["EXIT"]

            if width <= 0 or height <= 0:
                raise ValueError("WIDTH and HEIGHT must be greater than 0")

            if entry[0] >= width or entry[1] >= height:
<<<<<<< HEAD
                raise ValueError("Entry point out of bound")
            if exit[0] >= width or exit[1] >= height:
                raise ValueError("Exit point out of bound")
            if entry == exit:
                raise ValueError
            ("Invalid config for entry and exit (shouldn't be the same )")
=======
                raise ValueError("Entry point out of bounds")
            if exit[0] >= width or exit[1] >= height:
                raise ValueError("Exit point out of bounds")
            if entry == exit:
                raise ValueError("Invalid config for entry and exit (must be different)")
>>>>>>> 4ee574e (fixe all)

            return parsed_data
