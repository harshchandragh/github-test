"""
Enhanced Sprint Delay Prediction Module
Implements comprehensive delay prediction with task completion rates and blocker trends
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class DelayPredictor:
    """
    Predicts sprint delays by analyzing:
    1. Sprint progress vs time elapsed
    2. Task completion rates (velocity trends)
    3. Blocker trends and impact
    """
    
    def __init__(self):
        self.risk_thresholds = {
            'critical': 0.75,  # >75% chance of delay
            'high': 0.50,      # 50-75% chance
            'medium': 0.25,    # 25-50% chance
            'low': 0.0         # <25% chance
        }
    
    def predict_delay(self, sprint_data: pd.DataFrame, sprint_name: str) -> Dict:
        """
        Main delay prediction function
        
        Returns:
        {
            'will_delay': bool,
            'delay_probability': float,
            'risk_level': str,
            'factors': {
                'progress_risk': float,
                'completion_rate_risk': float,
                'blocker_risk': float
            },
            'recommendations': List[str],
            'early_warning': bool
        }
        """
        sprint_df = sprint_data[sprint_data['Assigned Sprint'] == sprint_name]
        
        if len(sprint_df) == 0:
            return None
        
        # Factor 1: Progress vs Time Analysis
        progress_risk = self._analyze_progress_vs_time(sprint_df)
        
        # Factor 2: Task Completion Rate
        completion_risk = self._analyze_completion_rate(sprint_df)
        
        # Factor 3: Blocker Trend Analysis
        blocker_risk = self._analyze_blocker_trends(sprint_df)
        
        # Combined delay probability (weighted average)
        delay_probability = (
            progress_risk * 0.4 +      # 40% weight on progress
            completion_risk * 0.35 +   # 35% weight on completion rate
            blocker_risk * 0.25        # 25% weight on blockers
        )
        
        # Determine risk level
        risk_level = self._get_risk_level(delay_probability)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            progress_risk, completion_risk, blocker_risk, sprint_df
        )
        
        # Early warning (predict delay 3+ days before sprint end)
        days_remaining = self._get_days_remaining(sprint_df)
        early_warning = days_remaining >= 3 and delay_probability > 0.5
        
        return {
            'sprint_name': sprint_name,
            'will_delay': delay_probability > 0.5,
            'delay_probability': round(delay_probability, 2),
            'risk_level': risk_level,
            'days_remaining': days_remaining,
            'factors': {
                'progress_risk': round(progress_risk, 2),
                'completion_rate_risk': round(completion_risk, 2),
                'blocker_risk': round(blocker_risk, 2)
            },
            'recommendations': recommendations,
            'early_warning': early_warning,
            'metrics': self._get_detailed_metrics(sprint_df)
        }
    
    def _analyze_progress_vs_time(self, sprint_df: pd.DataFrame) -> float:
        """
        Analyze if progress is on track with time elapsed
        
        Logic: If 50% of time has passed, we should have 50% completion
        Returns risk score 0-1
        """
        try:
            start_date = pd.to_datetime(sprint_df['Assigned Sprint\nStart date'].iloc[0])
            end_date = pd.to_datetime(sprint_df['Assigned Sprint\nEnd date'].iloc[0])
            now = pd.Timestamp.now()
            
            total_duration = (end_date - start_date).days
            time_elapsed = (now - start_date).days
            
            if total_duration <= 0:
                return 0.5
            
            time_progress = min(time_elapsed / total_duration, 1.0)
            
            # Calculate work progress
            total_points = sprint_df['Story Points'].sum()
            completed_points = sprint_df[sprint_df['Status'] == 'Done']['Story Points'].sum()
            work_progress = completed_points / total_points if total_points > 0 else 0
            
            # Calculate gap
            progress_gap = time_progress - work_progress
            
            # Convert gap to risk score
            if progress_gap <= 0:
                return 0.0  # Ahead of schedule
            elif progress_gap < 0.2:
                return 0.2  # Slightly behind
            elif progress_gap < 0.4:
                return 0.5  # Moderately behind
            elif progress_gap < 0.6:
                return 0.75  # Significantly behind
            else:
                return 1.0  # Critically behind
                
        except:
            return 0.5  # Default medium risk if dates unavailable
    
    def _analyze_completion_rate(self, sprint_df: pd.DataFrame) -> float:
        """
        Analyze task completion rate trends
        
        Looks at:
        - How many issues completed vs total
        - Distribution of work across sprint
        - Velocity compared to historical
        """
        total_issues = len(sprint_df)
        completed_issues = len(sprint_df[sprint_df['Status'] == 'Done'])
        in_progress = len(sprint_df[sprint_df['Status'] == 'In Progress'])
        todo = len(sprint_df[sprint_df['Status'] == 'To Do'])
        
        completion_rate = completed_issues / total_issues if total_issues > 0 else 0
        
        # Calculate risk based on completion rate
        if completion_rate >= 0.8:
            base_risk = 0.0
        elif completion_rate >= 0.6:
            base_risk = 0.2
        elif completion_rate >= 0.4:
            base_risk = 0.5
        elif completion_rate >= 0.2:
            base_risk = 0.75
        else:
            base_risk = 1.0
        
        # Adjust for work distribution
        # Risk increases if too many items in "To Do"
        todo_ratio = todo / total_issues if total_issues > 0 else 0
        if todo_ratio > 0.5:
            base_risk += 0.2
        
        return min(base_risk, 1.0)
    
    def _analyze_blocker_trends(self, sprint_df: pd.DataFrame) -> float:
        """
        Analyze impact of blockers on sprint
        
        Considers:
        - Number of blocked issues
        - Story points blocked
        - Blocker age (if available)
        """
        total_issues = len(sprint_df)
        blocked_issues = len(sprint_df[sprint_df['Status'] == 'Blocked'])
        
        if blocked_issues == 0:
            return 0.0
        
        # Calculate blocker ratio
        blocker_ratio = blocked_issues / total_issues
        
        # Calculate blocked story points
        total_points = sprint_df['Story Points'].sum()
        blocked_points = sprint_df[sprint_df['Status'] == 'Blocked']['Story Points'].sum()
        blocked_points_ratio = blocked_points / total_points if total_points > 0 else 0
        
        # Risk scoring
        if blocker_ratio < 0.1 and blocked_points_ratio < 0.1:
            return 0.2  # Minor blockers
        elif blocker_ratio < 0.2 and blocked_points_ratio < 0.2:
            return 0.5  # Moderate blockers
        elif blocker_ratio < 0.3 and blocked_points_ratio < 0.3:
            return 0.75  # Significant blockers
        else:
            return 1.0  # Critical blocker situation
    
    def _get_days_remaining(self, sprint_df: pd.DataFrame) -> int:
        """Get days remaining in sprint"""
        try:
            end_date = pd.to_datetime(sprint_df['Assigned Sprint\nEnd date'].iloc[0])
            now = pd.Timestamp.now()
            days = (end_date - now).days
            return max(days, 0)
        except:
            return 0
    
    def _get_risk_level(self, probability: float) -> str:
        """Convert probability to risk level"""
        if probability >= self.risk_thresholds['critical']:
            return 'critical'
        elif probability >= self.risk_thresholds['high']:
            return 'high'
        elif probability >= self.risk_thresholds['medium']:
            return 'medium'
        else:
            return 'low'
    
    def _generate_recommendations(
        self, 
        progress_risk: float, 
        completion_risk: float, 
        blocker_risk: float,
        sprint_df: pd.DataFrame
    ) -> List[str]:
        """Generate actionable recommendations based on risk factors"""
        recommendations = []
        
        # Progress-based recommendations
        if progress_risk > 0.7:
            total_points = sprint_df['Story Points'].sum()
            completed = sprint_df[sprint_df['Status'] == 'Done']['Story Points'].sum()
            remaining = total_points - completed
            recommendations.append(
                f"⚠️ URGENT: {remaining:.0f} story points remaining. "
                f"Consider moving low-priority items to next sprint."
            )
        elif progress_risk > 0.4:
            recommendations.append(
                "⚡ Sprint is behind schedule. Focus on completing in-progress items "
                "before starting new work."
            )
        
        # Completion rate recommendations
        if completion_risk > 0.7:
            in_progress = len(sprint_df[sprint_df['Status'] == 'In Progress'])
            recommendations.append(
                f"📊 Low completion rate detected. {in_progress} items in progress. "
                f"Reduce WIP (Work In Progress) to improve flow."
            )
        
        # Blocker recommendations
        if blocker_risk > 0.5:
            blocked_issues = sprint_df[sprint_df['Status'] == 'Blocked']
            blocked_count = len(blocked_issues)
            blocked_points = blocked_issues['Story Points'].sum()
            recommendations.append(
                f"🚧 {blocked_count} issues blocked ({blocked_points:.0f} pts). "
                f"Priority: Unblock these immediately to maintain velocity."
            )
            
            # List specific blocked items
            if blocked_count <= 5:
                for _, issue in blocked_issues.iterrows():
                    recommendations.append(
                        f"  → Blocked: {issue['Jira ID']} - {issue['Summary'][:50]}"
                    )
        
        # General recommendations
        if not recommendations:
            recommendations.append(
                "✅ Sprint is on track. Continue current pace to meet commitments."
            )
        
        return recommendations
    
    def _get_detailed_metrics(self, sprint_df: pd.DataFrame) -> Dict:
        """Get detailed metrics for analysis"""
        total_issues = len(sprint_df)
        total_points = sprint_df['Story Points'].sum()
        
        status_counts = sprint_df['Status'].value_counts().to_dict()
        
        return {
            'total_issues': total_issues,
            'total_story_points': float(total_points),
            'completed_issues': status_counts.get('Done', 0),
            'completed_points': float(sprint_df[sprint_df['Status'] == 'Done']['Story Points'].sum()),
            'in_progress_issues': status_counts.get('In Progress', 0),
            'in_progress_points': float(sprint_df[sprint_df['Status'] == 'In Progress']['Story Points'].sum()),
            'blocked_issues': status_counts.get('Blocked', 0),
            'blocked_points': float(sprint_df[sprint_df['Status'] == 'Blocked']['Story Points'].sum()),
            'todo_issues': status_counts.get('To Do', 0),
            'todo_points': float(sprint_df[sprint_df['Status'] == 'To Do']['Story Points'].sum()),
            'completion_percentage': float(
                sprint_df[sprint_df['Status'] == 'Done']['Story Points'].sum() / total_points * 100
            ) if total_points > 0 else 0
        }
    
    def analyze_all_sprints(self, df: pd.DataFrame) -> List[Dict]:
        """Analyze all sprints and return predictions"""
        sprints = df['Assigned Sprint'].dropna().unique()
        predictions = []
        
        for sprint in sprints:
            if sprint == 'None( Backlog)':
                continue
            
            prediction = self.predict_delay(df, sprint)
            if prediction:
                predictions.append(prediction)
        
        # Sort by risk level (critical first)
        risk_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        predictions.sort(key=lambda x: (risk_order.get(x['risk_level'], 4), -x['delay_probability']))
        
        return predictions


# Example usage
if __name__ == "__main__":
    import pandas as pd
    
    # Load data
    df = pd.read_excel('../Raw.xlsx')
    
    # Initialize predictor
    predictor = DelayPredictor()
    
    # Analyze all sprints
    predictions = predictor.analyze_all_sprints(df)
    
    print("="*80)
    print("SPRINT DELAY PREDICTIONS")
    print("="*80)
    
    for pred in predictions[:5]:  # Show top 5 at-risk sprints
        print(f"\n{'='*80}")
        print(f"Sprint: {pred['sprint_name']}")
        print(f"Risk Level: {pred['risk_level'].upper()}")
        print(f"Delay Probability: {pred['delay_probability']:.0%}")
        print(f"Days Remaining: {pred['days_remaining']}")
        
        if pred['early_warning']:
            print("⚠️ EARLY WARNING: Delay predicted with time to act!")
        
        print(f"\nRisk Factors:")
        print(f"  • Progress Risk: {pred['factors']['progress_risk']:.0%}")
        print(f"  • Completion Rate Risk: {pred['factors']['completion_rate_risk']:.0%}")
        print(f"  • Blocker Risk: {pred['factors']['blocker_risk']:.0%}")
        
        print(f"\nMetrics:")
        metrics = pred['metrics']
        print(f"  • Completion: {metrics['completed_issues']}/{metrics['total_issues']} issues")
        print(f"  • Story Points: {metrics['completed_points']:.0f}/{metrics['total_story_points']:.0f} pts")
        print(f"  • Blocked: {metrics['blocked_issues']} issues ({metrics['blocked_points']:.0f} pts)")
        
        print(f"\nRecommendations:")
        for rec in pred['recommendations']:
            print(f"  {rec}")
    
    print(f"\n{'='*80}")
    print(f"Total Sprints Analyzed: {len(predictions)}")
    print(f"Critical Risk: {sum(1 for p in predictions if p['risk_level'] == 'critical')}")
    print(f"High Risk: {sum(1 for p in predictions if p['risk_level'] == 'high')}")
    print(f"Medium Risk: {sum(1 for p in predictions if p['risk_level'] == 'medium')}")
    print(f"Low Risk: {sum(1 for p in predictions if p['risk_level'] == 'low')}")
