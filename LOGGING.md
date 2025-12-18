# Logging System Documentation

## Overview

This project uses a centralized logging system that automatically logs all operations to both console and file outputs. The logging module is located at `main/utils/logger.py`.

## Features

- **Dual File Logging**: 
  - Daily log files (e.g., `2025-12-18.log`) containing all logs from all modules
  - Module-specific log files (e.g., `retreival.log`, `cleaning.log`) for easier debugging

- **Console Output**: Important information is also displayed in the console for real-time monitoring

- **Automatic Directory Creation**: The `logs/` folder is created automatically when the first logger is initialized

- **Detailed Formatting**: Log entries include:
  - Timestamp
  - Module name
  - Log level (INFO, DEBUG, WARNING, ERROR)
  - Function name and line number
  - Log message

## Log Levels

- **DEBUG**: Detailed information for diagnosing problems
- **INFO**: General informational messages about program execution
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error messages with full stack traces

## Usage

### In Your Module

```python
from utils import LoggerSetup

class YourClass:
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info("YourClass instance initialized")
    
    def your_method(self):
        try:
            self.logger.info("Starting operation")
            # Your code here
            self.logger.debug("Operation detail")
            self.logger.info("Operation completed")
        except Exception as e:
            self.logger.error(f"Error occurred: {str(e)}", exc_info=True)
            raise
```

## Log File Locations

All log files are stored in the `logs/` directory at the project root:

```
langraphLearning/
├── logs/
│   ├── 2025-12-18.log          # Daily log (all modules)
│   ├── retreival.log            # Module-specific logs
│   ├── cleaning.log
│   ├── processing.log
│   └── generation.log
├── main/
│   └── utils/
│       └── logger.py            # Logging configuration
```

## Log Format Examples

### File Log Format
```
2025-12-18 14:08:12 - main.retreival - INFO - run:57 - Starting file retrieval - Type: pdf, Path: ../files/pdf/cvpfe.pdf
2025-12-18 14:08:13 - main.retreival - INFO - __load_pdf:41 - Loading PDF file from: ../files/pdf/cvpfe.pdf
2025-12-18 14:08:15 - main.retreival - INFO - __load_pdf:41 - Successfully loaded PDF file. Content length: 12345 characters
```

### Console Log Format
```
INFO - main.retreival - Starting file retrieval - Type: pdf, Path: ../files/pdf/cvpfe.pdf
INFO - main.retreival - Successfully loaded PDF file. Content length: 12345 characters
```

## Modules with Logging

The following modules have been configured with logging:

- `main/retreival.py` - File retrieval operations
- `main/generation.py` - Content generation
- `main/cv/cleaning.py` - CV cleaning operations
- `main/cv/processing.py` - CV data extraction
- `main/jobDescription/cleaning.py` - Job description cleaning
- `main/jobDescription/processing.py` - Job description data extraction

## Best Practices

1. **Use appropriate log levels**:
   - `DEBUG` for detailed diagnostic information
   - `INFO` for general operational messages
   - `WARNING` for potentially harmful situations
   - `ERROR` for error events with stack traces

2. **Include context in log messages**:
   ```python
   self.logger.info(f"Processing file: {filename}, size: {file_size} bytes")
   ```

3. **Always log exceptions with stack traces**:
   ```python
   except Exception as e:
       self.logger.error(f"Failed to process: {str(e)}", exc_info=True)
       raise
   ```

4. **Log entry and exit of important operations**:
   ```python
   self.logger.info("Starting data processing")
   # ... processing code ...
   self.logger.info("Data processing completed successfully")
   ```

## Maintenance

- Log files are not automatically rotated or deleted
- Consider implementing log rotation for production environments
- The `logs/` directory is excluded from version control via `.gitignore`
- Review and clean old log files periodically to manage disk space
