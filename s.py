from colorama import init, Fore, Back, Style
from datetime import datetime

init(autoreset=True)

class Logger:
    LEVELS = {
        "DEBUG": 0,
        "INFO": 1,
        "WARNING": 2,
        "ERROR": 3,
        "SUCCESS": 1
    }

    def __init__(self, use_color=True, log_file="app.log", level="INFO"):
        self.use_color = use_color
        self.log_file = log_file
        self.level = level.upper()
        self.min_level_val = self.LEVELS.get(self.level, 1)

    def _get_timestamp(self, for_file=False):

        ts = datetime.now().strftime("%H:%M:%S")

        if not for_file and self.use_color:
            return f"{Fore.WHITE}{Style.DIM}[{ts}] "
        
        return f"[{ts}] "
    
    def _format(self, text, color=""):
        return f"{color}{text}{Style.RESET_ALL}" if self.use_color else text

    def _write_to_file(self, prefix, message):
        with open(self.log_file, "a", encoding="utf-8") as f:
            timestamp = self._get_timestamp(for_file=True)
            f.write(f"{timestamp}{prefix}{message}\n")

    def _should_log(self, level_name):
        return self.LEVELS.get(level_name, 1) >= self.min_level_val

    def log_info(self, message):
        if self._should_log("INFO"):
            prefix = "[INFO] "
            print(f"{self._get_timestamp()}{self._format(prefix, Fore.BLUE)}{message}")
            self._write_to_file(prefix, message)

    def log_warning(self, message):
        if self._should_log("WARNING"):
            prefix = "[WARN] "
            print(f"{self._get_timestamp()}{self._format(prefix, Fore.YELLOW)}{message}")
            self._write_to_file(prefix, message)

    def log_error(self, message):
        if self._should_log("ERROR"):
            prefix = "[ERROR] "
            print(f"{self._get_timestamp()}{self._format(prefix, Back.RED + Fore.WHITE)}{message}")
            self._write_to_file(prefix, message)

    def log_success(self, message):
        if self._should_log("SUCCESS"):
            prefix = "[OK] "
            print(f"{self._get_timestamp()}{self._format(prefix, Fore.GREEN + Style.BRIGHT)}{message}")
            self._write_to_file(prefix, message)

def test():
    logger = Logger(use_color=True, level="INFO")
    
    logger.log_info("Starting installation of 'super-app'...")
    logger.log_warning("Older version detected, overwriting files.")

    try:
        raise Exception("Permission denied for /usr/local/bin")
    except Exception as e:
        logger.log_error(f"Installation aborted: {e}")
        
    logger.log_success("Installation completed successfully (after fixes).")
    
if __name__ == "__main__":
    test()