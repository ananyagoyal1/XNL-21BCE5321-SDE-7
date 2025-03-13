import logging
import json
import os
import time
from logging.handlers import RotatingFileHandler

class AdvancedLogger:
    def __init__(self, app_name, log_dir="logs"):
        self.app_name = app_name
        self.log_dir = log_dir
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Set up formatter
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s, "service": "' + app_name + '"}'
        )
        
        # Create logger
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            f"{log_dir}/{app_name}.log", 
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Error file handler
        error_handler = RotatingFileHandler(
            f"{log_dir}/{app_name}-error.log", 
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
    
    def info(self, message, **kwargs):
        self.logger.info(json.dumps({"content": message, **kwargs}))
    
    def error(self, message, **kwargs):
        self.logger.error(json.dumps({"content": message, **kwargs}))
    
    def warn(self, message, **kwargs):
        self.logger.warning(json.dumps({"content": message, **kwargs}))
    
    def debug(self, message, **kwargs):
        self.logger.debug(json.dumps({"content": message, **kwargs}))