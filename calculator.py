from collections.abc import KeysView
from dataclasses import dataclass
from math import ceil
from pathlib import Path
import tomllib
from typing import ClassVar, Dict, Tuple

# Pre-loaded emission data
PATH_EMISSION_TABLE = "emission-data.toml"


@dataclass
class Calculator:
    transportation: str
    distance: float
    distance_unit: str = "km"
    ouptput_unit: str = "auto"

    # A lookup table for emission data
    _emission_data: ClassVar[Dict[str, int | float]] = None

    # Supported units for distance input
    _supported_distance_unit: ClassVar[Tuple[str]] = ("km", "m")

    # Supported units for emission output
    _supported_output_unit: ClassVar[Tuple[str]] = ("auto", "kg", "g")

    def __post_init__(self):
        """Load emission data and check if the input is valid"""

        # Load emission data
        self._emission_data = self._load_emission_data(Path(PATH_EMISSION_TABLE))

        # Sanity check
        self._check_distance_unit()
        self._check_output_unit()
        self._check_transportation()

    @property
    def emission_data(self) -> KeysView:
        return self._emission_data

    @property
    def supported_distance_unit(self) -> Tuple[str]:
        return self._supported_distance_unit

    @property
    def supported_output_unit(self) -> Tuple[str]:
        return self._supported_output_unit

    @staticmethod
    def _load_emission_data(data_path: Path) -> float:
        """Load emission data from file"""
        with data_path.open("rb") as f:
            return tomllib.load(f)

    def _check_distance_unit(self) -> None:
        """Check if unit of distance is valid"""
        if self.distance_unit not in self._supported_distance_unit:
            raise ValueError(
                f"Invalid unit of distance! Supported unit of distance are:\n{self._supported_distance_unit}"
            )

    def _check_output_unit(self) -> None:
        """Check if unit of output is valid"""
        if self.ouptput_unit not in self._supported_output_unit:
            raise ValueError(
                f"Invalid unit of output! Supported unit of output are:\n{self._supported_output_unit}"
            )

    def _check_transportation(self) -> None:
        """Check if transportation method is valid"""
        if self.transportation not in self._emission_data.keys():
            raise ValueError(
                f"Invalid transportation method! Supported transportation methods are:\n{tuple(i for i in self._emission_data.keys())}"
            )

    def _to_normalized_distance(self) -> float:
        """Convert from 'm' to 'km' if necessary"""
        if self.distance_unit == "m":
            # Convert: 'm->km'
            return self._to_larger_unit(self.distance)
        else:
            return self.distance

    @staticmethod
    def _to_larger_unit(n) -> float:
        """Convert 'm->km' or 'g->kg'"""
        return n / 1000

    def _calculate_raw_result(self) -> float:
        """Compute raw emission result in unit g"""
        distance = self._to_normalized_distance()

        # Retrive the emission per km by look-up-table
        emission_per_km = self._emission_data[self.transportation]
        return distance * emission_per_km

    @staticmethod
    def _round_up(n, decimals=1) -> float:
        """Round result"""
        if n < 0.1:
            multiplier = 10**decimals
            return ceil(n * multiplier) / multiplier
        else:
            return round(n, decimals)

    def calculate_emission(self) -> Tuple[float, str]:
        """Main calculation method. Return the carbon emission according to the unit given"""
        raw_result = self._calculate_raw_result()

        if (
            raw_result >= 1000 and self.ouptput_unit != "g"
        ) or self.ouptput_unit == "kg":
            # Convert: 'g->kg'
            result = self._to_larger_unit(raw_result)
            result_unit = "kg"

        else:  # by default, the result is in unit g
            result = raw_result
            result_unit = "g"

        return self._round_up(result), result_unit
