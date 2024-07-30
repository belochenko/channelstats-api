import polars as pl
import numpy as np
from app.config import settings

from typing import Optional, List
from datetime import datetime

class DataService:
    """
    DataService is responsible for loading and managing the dataset,
    and providing methods to retrieve channel information and calculate statistics.
    """
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        """
        Load data from a parquet file, convert it to a Pandas DataFrame, and then to an xarray Dataset.

        Returns:
            xarray.Dataset: The loaded dataset with a timestamp index.
        """
        df = pl.read_parquet(settings.DATA_FILE) \
                    .with_columns(
                        pl.col("t").cast(pl.Datetime, strict=False).alias("timestamp")
                    )

        return df.sort("timestamp")


    def get_channels(self, channel_type: Optional[str] = None) -> List[str]:
        """
        Retrieve the list of available channels in the dataset, optionally filtered by type.

        Args:
            channel_type (str, optional): A substring to filter the channels by type (e.g., 'vel').

        Returns:
            list[str]: A list of channel names.
        """
        try:
            if channel_type:
                return [col for col in self.data.columns if channel_type in col and col not in ["t", "timestamp"]]
            else:
                return [col for col in self.data.columns if col not in ["t", "timestamp"]]
        except Exception as e:
            raise

    def get_stats(self, channels: Optional[List[str]] = None,
        start_date: Optional[str] = None, end_date: Optional[str] = None) -> dict:
        """
        Calculate statistics for the specified channels and date range.

        Args:
            channels (list[str], optional): List of channel names to calculate stats for. If None, stats for all channels are calculated.
            start_date (str, optional): Start date for the stats calculation (format: YYYY-MM-DD HH:MM:SS). If None, the entire time series is used.
            end_date (str, optional): End date for the stats calculation (format: YYYY-MM-DD HH:MM:SS). If None, the entire time series is used.

        Returns:
            dict: A dictionary containing the statistics (mean, std, min, max, count) for each channel.
        """
        try:
            data = self.data

            if channels:
                data = data.select(["timestamp"] + channels)
            else:
                data = data.select([col for col in data.columns if col not in ["t", "timestamp"]] + ["timestamp"])

            if start_date:
                start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                data = data.filter(pl.col("timestamp") >= pl.lit(start_date_dt).cast(pl.Datetime))
            if end_date:
                end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                data = data.filter(pl.col("timestamp") <= pl.lit(end_date_dt).cast(pl.Datetime))

            if data.height == 0:
                return {}

            stats = {}
            for col in data.columns:
                if col in ["t", "timestamp"]:
                    continue

                col_stats = data.select([
                    pl.col(col).mean().alias("mean"),
                    pl.col(col).std().alias("std"),
                    pl.col(col).min().alias("min"),
                    pl.col(col).max().alias("max"),
                    pl.col(col).count().alias("count")
                ]).to_dict(as_series=False)

                stats[col] = {
                    stat: float(col_stats[stat][0])
                    if stat != "count" else int(col_stats[stat][0])
                    for stat in ["mean", "std", "min", "max", "count"]
                }

            return stats
        except Exception as e:
            raise
