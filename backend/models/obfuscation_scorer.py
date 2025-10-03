import numpy as np
from scipy import stats

class ObfuscationScorer:
    def __init__(self):
        self.thresholds = {
            'high_suspicion': 0.7,
            'medium_suspicion': 0.5,
            'low_suspicion': 0.3
        }
    
    def calculate_obfuscation_score(self, segment_features):
        """
        Calculate overall obfuscation likelihood
        Returns score 0-1 and detailed breakdown
        """
        scores = {
            'lexical_inconsistency': self._lexical_inconsistency(segment_features),
            'syntactic_inconsistency': self._syntactic_inconsistency(segment_features),
            'stylistic_shift': self._stylistic_shift(segment_features),
            'unnatural_variation': self._unnatural_variation(segment_features)
        }
        
        weights = {
            'lexical_inconsistency': 0.25,
            'syntactic_inconsistency': 0.30,
            'stylistic_shift': 0.25,
            'unnatural_variation': 0.20
        }
        
        overall_score = sum(scores[k] * weights[k] for k in scores)
        
        return {
            'overall_score': overall_score,
            'risk_level': self._get_risk_level(overall_score),
            'component_scores': scores,
            'suspicious_segments': self._identify_suspicious_segments(segment_features, scores)
        }
    
    def _lexical_inconsistency(self, segment_features):
        """Detect unusual variation in lexical sophistication"""
        word_lengths = [f['avg_word_length'] for f in segment_features]
        ttr = [f['type_token_ratio'] for f in segment_features]
        
        word_length_cv = np.std(word_lengths) / np.mean(word_lengths) #variation coefficient
        ttr_cv = np.std(ttr) / np.mean(ttr)

        score = 0
        if word_length_cv > 0.20:
            score += 0.5
        if ttr_cv > 0.25:
            score += 0.5
        
        return min(score, 1.0)
    
    def _syntactic_inconsistency(self, segment_features):
        """Detect inconsistent sentence structure patterns"""
        sentence_lengths = [f['avg_sentence_length'] for f in segment_features]
        sentence_variances = [f['sentence_length_variance'] for f in segment_features]
        
        length_jumps = [abs(sentence_lengths[i] - sentence_lengths[i-1]) 
                       for i in range(1, len(sentence_lengths))]
        
        abnormal_jumps = sum(1 for jump in length_jumps if jump > 10) / len(length_jumps)
        
        return min(abnormal_jumps * 2, 1.0)
    
    def _stylistic_shift(self, segment_features):
        """Detect shifts in formality and style"""
        function_word_ratios = [f['function_word_ratio'] for f in segment_features]
        
        shifts = [abs(function_word_ratios[i] - function_word_ratios[i-1])
                 for i in range(1, len(function_word_ratios))]
        
        significant_shifts = sum(1 for s in shifts if s > 0.08) / len(shifts)
        
        return min(significant_shifts * 1.5, 1.0)
    
    def _unnatural_variation(self, segment_features):
        """Detect statistically improbable variation patterns"""
        #collect all feature vectors
        all_features = []
        for f in segment_features:
            feature_vector = [
                f['avg_word_length'],
                f['type_token_ratio'],
                f['avg_sentence_length'],
                f['noun_ratio'],
                f['verb_ratio']
            ]
            all_features.append(feature_vector)
        
        all_features = np.array(all_features)
        
        # calculate Mahalanobis distance for each segment
        # outliers suggest manipulation
        mean = np.mean(all_features, axis=0)
        cov = np.cov(all_features.T)
        
        try:
            inv_cov = np.linalg.inv(cov)
            distances = [self._mahalanobis(x, mean, inv_cov) for x in all_features]
            
            outliers = sum(1 for d in distances if d > 3.0) / len(distances)
            return min(outliers * 2, 1.0)
        except:
            return 0.0
    
    def _mahalanobis(self, x, mean, inv_cov):
        """Calculate Mahalanobis distance"""
        diff = x - mean
        return np.sqrt(diff @ inv_cov @ diff.T)
    
    def _get_risk_level(self, score):
        """Convert score to risk level"""
        if score >= self.thresholds['high_suspicion']:
            return 'HIGH'
        elif score >= self.thresholds['medium_suspicion']:
            return 'MEDIUM'
        elif score >= self.thresholds['low_suspicion']:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def _identify_suspicious_segments(self, segment_features, scores):
        """Identify which specific segments are most suspicious"""
        suspicious = []
        
        for i, features in enumerate(segment_features):
            segment_score = self._calculate_segment_score(features, segment_features)
            if segment_score > 0.6:
                suspicious.append({
                    'segment_index': i,
                    'score': segment_score,
                    'features': features
                })
        
        return sorted(suspicious, key=lambda x: x['score'], reverse=True)
    
    def _calculate_segment_score(self, segment, all_segments):
        """Score individual segment against the corpus"""
        others = [s for s in all_segments if s != segment]
        
        if not others:
            return 0.0
        
        deviations = []
        for key in ['avg_word_length', 'avg_sentence_length', 'type_token_ratio']:
            segment_val = segment[key]
            others_mean = np.mean([s[key] for s in others])
            others_std = np.std([s[key] for s in others])
            
            if others_std > 0:
                z_score = abs((segment_val - others_mean) / others_std)
                deviations.append(z_score)
        
        return min(np.mean(deviations) / 3, 1.0)  