# import logging
# import os
# import datetime
# import csv
# from typing import Optional, Dict
# from colorama import init, Fore, Style
#
# init(autoreset=True)
#
# COLOR_MAP = {
#     'DEBUG': Fore.WHITE,
#     'INFO': Fore.GREEN,
#     'WARNING': Fore.YELLOW,
#     'ERROR': Fore.RED,
#     'CRITICAL': Style.BRIGHT + Fore.RED
# }
#
# class ColorFormatter(logging.Formatter):
#     def format(self, record):
#         color = COLOR_MAP.get(record.levelname, '')
#         formatted_msg = super().format(record)
#         return f"{color}{formatted_msg}{Style.RESET_ALL}"
#
# class ContextLoggerAdapter(logging.LoggerAdapter):
#     def process(self, msg, kwargs):
#         level = kwargs.get('level', self.logger.level)
#         level_name = logging.getLevelName(level if isinstance(level, int) else self.logger.level)
#
#         structured_msg = (
#             f"[{self.extra.get('layer', '')}] "
#             f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} - "
#             f"{self.extra.get('suite', '')} | {self.extra.get('test_file', '')} | {self.extra.get('test_case', '')} - {msg}"
#         )
#
#         # Write to CSV file if specified
#         csv_writer = self.extra.get("csv_writer")
#         if csv_writer:
#             csv_writer.writerow([
#                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 self.extra.get('layer', ''),
#                 self.extra.get('suite', ''),
#                 self.extra.get('test_file', ''),
#                 self.extra.get('test_case', ''),
#                 level_name,
#                 msg
#             ])
#
#         return structured_msg, kwargs
#
# def setup_logger(log_filename: Optional[str] = None, context: Optional[Dict[str, str]] = None):
#     logger = logging.getLogger("structured")
#     logger.setLevel(logging.DEBUG)
#     log_file_path = None  # <-- Ensure it's always defined
#     if not logger.handlers:
#         log_dir = os.path.join(os.getcwd(), "logs")
#         os.makedirs(log_dir, exist_ok=True)
#
#         if not log_filename:
#             timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#             log_filename = f"test_log_{timestamp}"
#
#         log_file_path = os.path.join(log_dir, log_filename + ".log")
#         csv_file_path = os.path.join(log_dir, log_filename + ".csv")
#
#         fh = logging.FileHandler(log_file_path, encoding="utf-8")
#         fh.setLevel(logging.DEBUG)
#         fh.setFormatter(logging.Formatter('%(message)s'))
#
#         ch = logging.StreamHandler()
#         ch.setLevel(logging.DEBUG)
#         ch.setFormatter(ColorFormatter('%(message)s'))
#
#         logger.addHandler(fh)
#         logger.addHandler(ch)
#
#         # Prepare CSV writer
#         csv_file = open(csv_file_path, mode='w', newline='', encoding='utf-8')
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow(["Timestamp", "Layer", "Suite", "TestFile", "TestMethod", "Level", "Message"])
#
#         # Inject CSV writer into context for access in process
#         if context is None:
#             context = {}
#         context['csv_writer'] = csv_writer
#
#     return ContextLoggerAdapter(logger, context or {}), log_file_path
