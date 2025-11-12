"""
LEARNVIA Core Module
AI-Powered Content Review System for Calculus Educational Materials
"""

__version__ = "2.0.0"
__author__ = "LEARNVIA Team"

from .config_loader import ConfigLoader
from .xml_parser import XMLParser
from .consensus import ConsensusAggregator

__all__ = ['ConfigLoader', 'XMLParser', 'ConsensusAggregator']