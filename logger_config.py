import logging
import os
import csv
from datetime import datetime
from colorlog import ColoredFormatter
from airtest.core.api import snapshot

class CSVFormatter(logging.Formatter):
    def format(self, record):
        msg= f"{datetime.fromtimestamp(record.created).strftime('%H:%M:%S')},{record.levelname},{record.name},{record.getMessage()}"
        if hasattr(record, 'screenshot'):
            msg += f",{record.screenshot}"
        return msg
class CSVLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.csv_file = open(csv_file_path, mode='w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(['Time', 'Level', 'Module', 'Message','Screenshot'])  # CSV header
    def emit(self, record):
        try:
            self.writer.writerow([
                datetime.fromtimestamp(record.created).strftime('%H:%M:%S'),
                record.levelname,
                record.name,
                record.getMessage(),
                getattr(record, 'screenshot', '')
            ])
            self.csv_file.flush()
        except Exception:
            self.handleError(record)
    def close(self):
        self.csv_file.close()
        super().close()

class ScreenshotLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        # self.screenshots_dir = os.path.join(LOG_DIR, "screenshots")
        # os.makedirs(self.screenshots_dir, exist_ok=True)
    def emit(self, record):
        if record.levelno >= logging.WARNING:  # WARNING, ERROR, or CRITICAL
            try:
                timestamp = datetime.now().strftime('%Y-%m-%d_%Hh%M')
                screenshot_name = f"{timestamp}.png"
                screenshot_path = os.path.join(SCREENSHOT_FOLDER, screenshot_name)
                snapshot(screenshot_path)
                # Add screenshot path to the log record
                hyperlink = f'=HYPERLINK("file:///{screenshot_path.replace("\\", "/")}", "View")' if screenshot_path else ''
                record.screenshot = hyperlink
            except Exception as e:
                print(f"Failed to take screenshot: {e}")

class ExtendedFormatter(logging.Formatter):
    def format(self, record):
        formatted_msg = super().format(record)
        if hasattr(record, 'screenshot'):
            formatted_msg += f" | Screenshot: {record.screenshot}"
        return formatted_msg

# === File paths ===
# LOG_DIR = "LogFiles"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(CURRENT_DIR, "LogFiles")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FOLDER = os.path.join(LOG_DIR, "log")
CSV_FOLDER = os.path.join(LOG_DIR, "csv")
SCREENSHOT_FOLDER = os.path.join(LOG_DIR, "screenshot")
# Create all required directories
os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(CSV_FOLDER, exist_ok=True)
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
# Create log, csv, and screenshot file paths
time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_path = os.path.join(LOG_FOLDER, f"log_{time_str}.log")
csv_file_path = os.path.join(CSV_FOLDER, f"log_{time_str}.csv")
# Initialize handlers after directory creation
screenshot_handler = ScreenshotLogHandler()
file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
csv_handler = CSVLogHandler()  # Your existing CSVLogHandler class
console_handler = logging.StreamHandler()

file_formatter = ExtendedFormatter(
    '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt='%H:%M:%S')
file_handler.setFormatter(file_formatter)
screenshot_handler.setLevel(logging.WARNING)
color_formatter = ColoredFormatter(
    fmt="%(log_color)s[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'bold_yellow',
        'ERROR':    'bold_purple',
        'CRITICAL': 'bg_purple',
    }
)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(color_formatter)

def get_logger(name=None, custom_format=None):
    if name is None:
        import inspect
        frame = inspect.currentframe()
        try:
            while frame:
                if frame.f_code.co_name.startswith('test_'):
                    # Get the class name if it exists
                    if 'self' in frame.f_locals:
                        cls = frame.f_locals['self'].__class__
                        module = inspect.getmodule(cls)
                        module_path = module.__file__.replace('\\', '/').split('/')
                        test_path = ':'.join(module_path[-2:])  # Get last 2 parts of path
                        name = f"{test_path}:{cls.__name__}:{frame.f_code.co_name}"
                        break
                frame = frame.f_back
        finally:
            del frame

    logger = logging.getLogger(name or "unknown")

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(screenshot_handler)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(csv_handler)
        logger.propagate = False
        # apply custom format if provided
        if custom_format:
            for handler in logger.handlers:
                handler.setFormatter(logging.Formatter(custom_format))


    return logger

# Store original info method
_orig_info = logging.Logger.info

def _print_style_info(self, msg, *args, **kwargs):
    # if user passed args but msg has no %-placeholder, treat it like print()
    if args and "%" not in msg:
        # coerce everything to str and join with spaces
        msg = " ".join([str(msg)] + [str(a) for a in args])
        args = ()
    return _orig_info(self, msg, *args, **kwargs)



# Replace the original info method with our custom one
logging.Logger.info = _print_style_info
