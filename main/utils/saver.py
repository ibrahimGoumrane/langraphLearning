import pandas as pd
import json
from pydantic import BaseModel
from typing import Union, Any
from pathlib import Path


class Saver:
    """
    Utility class for saving data in various formats.
    Supports Pydantic models, dictionaries, and pandas DataFrames.
    """
    
    @staticmethod
    def _convert_to_dict(data: Any) -> Union[dict, list]:
        """
        Convert data to dictionary format.
        Handles Pydantic BaseModel instances.
        
        Args:
            data: Data to convert (BaseModel, dict, or list)
            
        Returns:
            Dictionary or list representation of the data
        """
        if isinstance(data, BaseModel):
            # Convert Pydantic model to dict, excluding None values
            return data.model_dump(exclude_none=True)
        elif isinstance(data, dict):
            return data
        elif isinstance(data, list):
            return [Saver._convert_to_dict(item) for item in data]
        else:
            return data
    
    @staticmethod
    def saveJson(data: Any, path: Union[str, Path]) -> None:
        """
        Save data as JSON file.
        
        Args:
            data: Data to save (BaseModel, DataFrame, dict, or list)
            path: File path to save to
        """
        path = Path(path)
        
        if isinstance(data, pd.DataFrame):
            data.to_json(path, orient='records', indent=4)
        else:
            # Convert Pydantic models to dict
            data_dict = Saver._convert_to_dict(data)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=4, ensure_ascii=False)

    @staticmethod
    def saveCsv(data: Any, path: Union[str, Path]) -> None:
        """
        Save data as CSV file.
        
        Args:
            data: Data to save (BaseModel, DataFrame, dict, or list)
            path: File path to save to
        """
        path = Path(path)
        
        if isinstance(data, pd.DataFrame):
            data.to_csv(path, index=False, encoding='utf-8')
        else:
            # Convert Pydantic models to dict first
            data_dict = Saver._convert_to_dict(data)
            
            # Flatten nested structure for CSV
            if isinstance(data_dict, dict):
                # For nested dict structures, we need to flatten lists
                flattened_data = []
                for key, value in data_dict.items():
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                # Add section identifier
                                item['section'] = key
                                flattened_data.append(item)
                            else:
                                flattened_data.append({'section': key, 'value': item})
                    else:
                        flattened_data.append({'section': key, 'value': value})
                
                df = pd.DataFrame(flattened_data)
            else:
                df = pd.DataFrame(data_dict)
            
            df.to_csv(path, index=False, encoding='utf-8')

    @staticmethod
    def run(data: Any, path: Union[str, Path], format: str) -> None:
        """
        Save data in the specified format.
        
        Args:
            data: Data to save (BaseModel, DataFrame, dict, or list)
            path: File path to save to
            format: Output format ('json' or 'csv')
            
        Raises:
            ValueError: If format is not supported
        """
        if format.lower() == 'json':
            Saver.saveJson(data, path)
        elif format.lower() == 'csv':
            Saver.saveCsv(data, path)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'json' or 'csv'.")