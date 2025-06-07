"""
Sentiment analysis and thematic analysis module
"""

import pandas as pd
import numpy as np
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter
import re
import logging
from typing import Dict, List, Tuple
import os

from .config import DATA_PATHS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Comprehensive sentiment analysis using multiple approaches"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize sentiment analyzers
        try:
            self.transformer_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                return_all_scores=True
            )
        except Exception as e:
            self.logger.warning(f"Could not load transformer model: {e}")
            self.transformer_analyzer = None
            
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            self.logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def analyze_sentiment_transformer(self, text: str) -> Dict:
        """Analyze sentiment using transformer model"""
        if not self.transformer_analyzer:
            return {'label': 'NEUTRAL', 'score': 0.5}
            
        try:
            result = self.transformer_analyzer(text[:512])  # Limit text length
            scores = {item['label']: item['score'] for item in result[0]}
            
            if 'POSITIVE' in scores and 'NEGATIVE' in scores:
                if scores['POSITIVE'] > scores['NEGATIVE']:
                    return {'label': 'POSITIVE', 'score': scores['POSITIVE']}
                else:
                    return {'label': 'NEGATIVE', 'score': scores['NEGATIVE']}
            else:
                return {'label': 'NEUTRAL', 'score': 0.5}
                
        except Exception as e:
            self.logger.error(f"Transformer sentiment analysis error: {e}")
            return {'label': 'NEUTRAL', 'score': 0.5}
    
    def analyze_sentiment_vader(self, text: str) -> Dict:
        """Analyze sentiment using VADER"""
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            compound = scores['compound']
            
            if compound >= 0.05:
                label = 'POSITIVE'
            elif compound <= -0.05:
                label = 'NEGATIVE'
            else:
                label = 'NEUTRAL'
                
            return {
                'label': label,
                'score': abs(compound),
                'compound': compound,
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu']
            }
        except Exception as e:
            self.logger.error(f"VADER sentiment analysis error: {e}")
            return {'label': 'NEUTRAL', 'score': 0.5}
    
    def analyze_sentiment_textblob(self, text: str) -> Dict:
        """Analyze sentiment using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                label = 'POSITIVE'
            elif polarity < -0.1:
                label = 'NEGATIVE'
            else:
                label = 'NEUTRAL'
                
            return {
                'label': label,
                'score': abs(polarity),
                'polarity': polarity
            }
        except Exception as e:
            self.logger.error(f"TextBlob sentiment analysis error: {e}")
            return {'label': 'NEUTRAL', 'score': 0.5}