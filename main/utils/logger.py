import logging
import os
from datetime import datetime
from pathlib import Path

class LoggerSetup:
    """
    Centralized logging configuration for the LangGraph Learning project.
    Provides consistent logging across all modules with file and console output.
    """
    
    _loggers = {}
    _logs_dir = None
    
    @classmethod
    def setup_logger(cls, name: str, level: int = logging.INFO) -> logging.Logger:
        """
        Set up and return a logger with the specified name.
        
        Args:
            name (str): Name of the logger (typically __name__ of the calling module)
            level (int): Logging level (default: logging.INFO)
            
        Returns:
            logging.Logger: Configured logger instance
        """
        # Return existing logger if already configured
        if name in cls._loggers:
            return cls._loggers[name]
        
        # Create logs directory if it doesn't exist
        if cls._logs_dir is None:
            project_root = Path(__file__).parent.parent.parent
            cls._logs_dir = project_root / "logs"
            cls._logs_dir.mkdir(exist_ok=True)
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Prevent duplicate handlers
        if logger.handlers:
            return logger
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = logging.Formatter(
            fmt='%(levelname)s - %(name)s - %(message)s'
        )
        
        # File handler - daily log file
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = cls._logs_dir / f"{today}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # File handler - module-specific log file
        module_name = name.split('.')[-1]
        module_log_file = cls._logs_dir / f"{module_name}.log"
        module_file_handler = logging.FileHandler(module_log_file, encoding='utf-8')
        module_file_handler.setLevel(logging.DEBUG)
        module_file_handler.setFormatter(detailed_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(module_file_handler)
        logger.addHandler(console_handler)
        
        # Cache the logger
        cls._loggers[name] = logger
        
        return logger
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get an existing logger or create a new one.
        
        Args:
            name (str): Name of the logger
            
        Returns:
            logging.Logger: Logger instance
        """
        return cls.setup_logger(name)
