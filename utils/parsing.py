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
    OPTIONAL_KEY = {"SEED", "ALGORITHM"}

    def __init__(self, config_file: str) -> None:
        """Store the configuration file path."""
        self.config_file = config_file

    def validate_int(self, key: str, value: str) -> int:
        """Validate that a string is a non-negative integer."""
        try:
            parsed_value = int(value)
        except ValueError:
            raise ValueError(
                f"Invalid value for {key} (use integer value)"
            )
        if parsed_value < 0:
            raise ValueError(
                f"Invalid value for {key} (use non-negative value)"
            )
        return parsed_value

    def parse_coordinate(self, key: str, value: str) -> Tuple[int, int]:
        """Parse and validate coordinate values formatted as 'x,y'."""
        coordinates = value.split(",")
        if len(coordinates) != 2:
            raise ValueError(f"Invalid value for {key} (use x,y)")
        try:
            x = int(coordinates[0].strip())
            y = int(coordinates[1].strip())
        except ValueError:
            raise ValueError(
                f"Invalid value for {key} "
                "(use integer values for x,y)"
            )
        if x < 0 or y < 0:
            raise ValueError(
                f"Invalid value for {key} (use non-negative values)"
            )
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
                    raise ValueError(
                        f"Invalid config line {index + 1}: {line}"
                    )

                key, value = line.split("=", 1)
                key = key.upper().strip()
                value = value.strip()

                if key not in all_keys:
                    raise ValueError(f"Invalid key ({key})")
                if key in parsed_data:
                    raise ValueError(f"Duplicate key ({key})")

                if key == "PERFECT":
                    cleaned_value = value.lower()
                    if cleaned_value not in {"true", "false"}:
                        raise ValueError("Invalid value for PERFECT key")
                    parsed_data[key] = cleaned_value == "true"
                elif key == "ALGORITHM":
                    cleaned_algorithm = value.upper()
                    if cleaned_algorithm not in {"DFS", "PRIM"}:
                        raise ValueError(
                            "Invalid value for ALGORITHM key "
                            "(use DFS or PRIM)"
                        )
                    parsed_data[key] = cleaned_algorithm
                elif key in {"WIDTH", "HEIGHT", "SEED"}:
                    parsed_data[key] = self.validate_int(key, value)
                elif key in {"ENTRY", "EXIT"}:
                    parsed_data[key] = self.parse_coordinate(key, value)
                else:
                    if not value:
                        raise ValueError(
                            "Invalid value for OUTPUT_FILE "
                            "(cannot be empty)"
                        )
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
            raise ValueError("Entry point out of bounds")
        if exit[0] >= width or exit[1] >= height:
            raise ValueError("Exit point out of bounds")
        if entry == exit:
            raise ValueError(
                "Invalid config for entry and exit "
                "(must be different)"
            )

        return parsed_data
