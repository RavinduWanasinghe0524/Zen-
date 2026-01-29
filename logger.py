"""
Zen Voice Assistant - Centralized Logging Module
Provides structured logging with file rotation and multiple log levels.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime


class ZenLogger:
    """Centralized logging configuration for Zen."""
    
    _initialized = False
    _loggers = {}
    
    @classmethod
    def initialize(cls, log_level="INFO", log_to_file=True, debug_mode=False):
        """
        Initialize the logging system.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: Whether to log to file
            debug_mode: Enable debug mode with verbose output
        """
        if cls._initialized:
            return
        
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Set log level
        level = logging.DEBUG if debug_mode else getattr(logging, log_level.upper())
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # Console handler (simple format)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(simple_formatter)
        
        handlers = [console_handler]
        
        # File handler (detailed format with rotation)
        if log_to_file:
            log_file = log_dir / f"zen_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)  # Always log everything to file
            file_handler.setFormatter(detailed_formatter)
            handlers.append(file_handler)
            
            # Separate error log
            error_log_file = log_dir / f"zen_errors_{datetime.now().strftime('%Y%m%d')}.log"
            error_handler = RotatingFileHandler(
                error_log_file,
                maxBytes=10*1024*1024,
                backupCount=3,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(detailed_formatter)
            handlers.append(error_handler)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        # Remove existing handlers
        root_logger.handlers.clear()
        
        # Add our handlers
        for handler in handlers:
            root_logger.addHandler(handler)
        
        cls._initialized = True
        
        # Log initialization
        logger = cls.get_logger("ZenLogger")
        logger.info(f"Logging system initialized - Level: {log_level}, File logging: {log_to_file}")
    
    @classmethod
    def get_logger(cls, name):
        """
        Get a logger instance for a module.
        
        Args:
            name: Name of the module/logger
            
        Returns:
            Logger instance
        """
        if name not in cls._loggers:
            cls._loggers[name] = logging.getLogger(name)
        return cls._loggers[name]
    
    @classmethod
    def log_exception(cls, logger, message, exc_info=True):
        """
        Log an exception with full traceback.
        
        Args:
            logger: Logger instance
            message: Error message
            exc_info: Whether to include exception info
        """
        logger.error(message, exc_info=exc_info)
    
    @classmethod
    def cleanup_old_logs(cls, days_to_keep=7):
        """
        Clean up log files older than specified days.
        
        Args:
            days_to_keep: Number of days to retain logs
        """
        log_dir = Path("logs")
        if not log_dir.exists():
            return
        
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        deleted_count = 0
        for log_file in log_dir.glob("*.log*"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                try:
                    log_file.unlink()
                    deleted_count += 1
                except Exception as e:
                    logging.error(f"Failed to delete old log file {log_file}: {e}")
        
        if deleted_count > 0:
            logging.info(f"Cleaned up {deleted_count} old log files")


# Convenience function
def get_logger(name):
    """Get a logger instance."""
    return ZenLogger.get_logger(name)


# Initialize with default settings when imported
if not ZenLogger._initialized:
    try:
        from config import Config
        ZenLogger.initialize(
            log_level=Config.LOG_LEVEL,
            log_to_file=getattr(Config, 'LOG_TO_FILE', True),
            debug_mode=getattr(Config, 'DEBUG_MODE', False)
        )
    except ImportError:
        # Config not available, use defaults
        ZenLogger.initialize()


# Standalone test
if __name__ == "__main__":
    print("=== Zen Logger Test ===\n")
    
    ZenLogger.initialize(log_level="DEBUG", debug_mode=True)
    
    logger = get_logger("TestModule")
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    try:
        raise ValueError("Test exception")
    except Exception as e:
        ZenLogger.log_exception(logger, "Caught an exception")
    
    print("\n✓ Logger test complete! Check logs/ directory for log files.")
