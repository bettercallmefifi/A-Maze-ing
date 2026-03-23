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
    OPTIONAL_KEY = {"SEED"}


    def __init__(self, config_file: str) -> None:
        """Store the configuration file path."""
        self.config_file = config_file
    
    def validate_int(self, key: str, value: str) -> int:
        """Validate that a string is a non-negative integer."""
        try:
            value = int(value)
        except ValueError:
            raise ValueError(f"Invalid valid value for {key} (use integer value)")
        if value < 0:
            raise ValueError(f"Invalid value for {key} (use positive value)")
        return value
    
    def parse_cordinate(self, key: str, value: str) -> Tuple[int, int]:
        """Parse and validate coordinate values formatted as 'x,y'."""
        cordinates = value.split(",")
        if len(cordinates) != 2:
            raise ValueError("Invalid value for {key}")
        try:
            x  = int(cordinates[0].strip())
            y  = int(cordinates[1].strip())
        except ValueError:
            raise ValueError(f"Invalid value for {key} use integer values for (x,y)")
        if x< 0 or y < 0:
            raise ValueError (f"Invalid value for {key} use positive values")
        return x,y
    
    
    def parse(self) -> Dict[str, Any]:
        """Read config file and return validated key/value data."""
        parsed_data: Dict[str, Any] = {}
        all_keys = self.REQUIRED_KEYS | self.OPTIONAL_KEY
        with open(self.config_file,"r") as file:
            for index ,line in enumerate(file) :
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"invalid config line ({index + 1} ({line}))")
                key,value = line.split("=",1)
                key = key.upper().strip()
                if key not in all_keys:
                    raise ValueError(f"Invalid key value ({key})")
                if key  == "PERFECT":
                    cleaned_key = value.lower()
                    if cleaned_key in ["true","false"]:
                        parsed_data[key] = cleaned_key == "true"
                    else:
                        raise ValueError("Invalid value for PERFECT key")
                elif key in ["WIDTH","HEIGHT","SEED"]:
                    parsed_data[key] = self.validate_int(key,value)
                elif key in {"ENTRY","EXIT"}:
                    parsed_data[key] = self.parse_cordinate(key,value)
                else:
                    parsed_data[key] = value
                # print(parsed_data)
            for required in self.REQUIRED_KEYS:
                if required not in parsed_data:
                    raise ValueError(f"Missing key {required}")
                    
            width = parsed_data["WIDTH"]
            height = parsed_data["HEIGHT"]
            entry = parsed_data["ENTRY"]
            exit = parsed_data["EXIT"]

            if entry[0] >= width or entry[1] >= height:
                raise ValueError(f"Entry point out of bound")
            if exit[0] >= width or exit[1] >= height:
                raise ValueError(f"Exit point out of bound")
            if entry == exit:
                raise ValueError(f"Invalid config for entry and exit (shouldn't be the same )")
            
            return parsed_data