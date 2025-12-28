"""CrewAI Log Parser Module

This module provides classes and functions to parse CrewAI execution logs
and extract relevant information about agent interactions.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class CrewLogEntry:
    """Represents a single log entry from CrewAI execution."""
    timestamp: str
    task_name: str
    task: str
    agent: str
    status: str
    output: str = ""
    
    def get_task_summary(self, max_length: int = 200) -> str:
        """Get a truncated summary of the task."""
        if len(self.task) <= max_length:
            return self.task
        return self.task[:max_length] + '...'
    
    def get_agent_name(self) -> str:
        """Extract clean agent name from the description."""
        agent_clean = self.agent.strip()
        # Remove newlines and extra spaces
        agent_clean = ' '.join(agent_clean.split())
        
        # Extract the main role before 'who' if present
        if 'who' in agent_clean.lower():
            parts = agent_clean.split('who')
            if parts:
                return parts[0].strip()
        return agent_clean
    
    def get_agent_role(self) -> str:
        """Extract the role/description of the agent."""
        agent_clean = self.agent.strip()
        agent_clean = ' '.join(agent_clean.split())
        
        # If 'who' is present, get the description after it
        if 'who' in agent_clean.lower():
            parts = agent_clean.lower().split('who')
            if len(parts) > 1:
                return parts[1].strip()
        return "AI Agent"
    
    def get_datetime(self) -> Optional[datetime]:
        """Convert timestamp string to datetime object."""
        try:
            return datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S")
        except:
            return None
    
    def get_formatted_timestamp(self) -> str:
        """Get a nicely formatted timestamp."""
        dt = self.get_datetime()
        if dt:
            return dt.strftime("%b %d, %Y at %I:%M:%S %p")
        return self.timestamp
    
    def extract_key_actions(self) -> List[str]:
        """Extract key actions from the task or output."""
        actions = []
        
        # Look for action patterns in task description
        action_patterns = [
            r'- ([A-Z][^\n.]+)',  # Bullet points
            r'\d+\. ([A-Z][^\n.]+)',  # Numbered lists
            r'(?:must|should|will|need to) ([a-z]+[^.]+)',  # Action verbs
        ]
        
        text_to_search = self.task + "\n" + self.output
        
        for pattern in action_patterns:
            matches = re.findall(pattern, text_to_search, re.MULTILINE)
            actions.extend(matches[:3])  # Limit to 3 actions per pattern
        
        # Clean and deduplicate
        clean_actions = []
        for action in actions:
            action = action.strip()
            if len(action) > 10 and len(action) < 100:
                if action not in clean_actions:
                    clean_actions.append(action)
        
        return clean_actions[:5]  # Return top 5 actions


@dataclass
class AgentSummary:
    """Summary statistics for an agent."""
    name: str
    role: str
    total_tasks: int = 0
    completed_tasks: int = 0
    started_tasks: int = 0
    task_types: List[str] = field(default_factory=list)
    entries: List[CrewLogEntry] = field(default_factory=list)
    key_contributions: List[str] = field(default_factory=list)
    
    def get_completion_rate(self) -> float:
        """Calculate task completion rate."""
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100
    
    def get_status_emoji(self, status: str) -> str:
        """Get emoji for status."""
        status_emojis = {
            'completed': '✅',
            'started': '🔄',
            'failed': '❌',
            'pending': '⏳'
        }
        return status_emojis.get(status.lower(), '❓')


class CrewLogParser:
    """Parser for CrewAI log files."""
    
    def __init__(self):
        self.entries: List[CrewLogEntry] = []
        self.agents: Dict[str, AgentSummary] = {}
        self.parse_errors: List[str] = []
    
    def parse_json_file(self, file_content: str) -> bool:
        """Parse JSON log file content."""
        try:
            # Try to parse as JSON
            data = json.loads(file_content)
            
            if isinstance(data, list):
                for idx, item in enumerate(data):
                    try:
                        entry = CrewLogEntry(
                            timestamp=item.get('timestamp', ''),
                            task_name=item.get('task_name', ''),
                            task=item.get('task', ''),
                            agent=item.get('agent', ''),
                            status=item.get('status', ''),
                            output=item.get('output', '')
                        )
                        self.entries.append(entry)
                        
                        # Group by agent
                        agent_name = entry.get_agent_name()
                        if agent_name not in self.agents:
                            self.agents[agent_name] = AgentSummary(
                                name=agent_name,
                                role=entry.get_agent_role()
                            )
                        
                        agent_summary = self.agents[agent_name]
                        agent_summary.entries.append(entry)
                        agent_summary.total_tasks += 1
                        
                        if entry.status.lower() == 'completed':
                            agent_summary.completed_tasks += 1
                        elif entry.status.lower() == 'started':
                            agent_summary.started_tasks += 1
                        
                        if entry.task_name not in agent_summary.task_types:
                            agent_summary.task_types.append(entry.task_name)
                        
                        # Extract key contributions
                        actions = entry.extract_key_actions()
                        for action in actions:
                            if action not in agent_summary.key_contributions:
                                agent_summary.key_contributions.append(action)
                    
                    except Exception as e:
                        self.parse_errors.append(f"Error parsing entry {idx}: {str(e)}")
                
                return True
            else:
                self.parse_errors.append("Expected JSON array but got: " + str(type(data)))
                return False
                
        except json.JSONDecodeError as e:
            self.parse_errors.append(f"JSON parsing error: {str(e)}")
            return False
        except Exception as e:
            self.parse_errors.append(f"Unexpected error: {str(e)}")
            return False
    
    def get_agents_list(self) -> List[AgentSummary]:
        """Get list of all agents with their summaries."""
        return list(self.agents.values())
    
    def get_agent_by_name(self, name: str) -> Optional[AgentSummary]:
        """Get a specific agent by name."""
        return self.agents.get(name)
    
    def get_timeline(self) -> List[CrewLogEntry]:
        """Get all entries sorted by timestamp."""
        return sorted(self.entries, key=lambda x: x.get_datetime() or datetime.min)
    
    def get_interaction_graph(self) -> Dict[str, List[str]]:
        """Build an interaction graph showing agent collaborations."""
        interactions = {}
        
        # Sort entries by time
        timeline = self.get_timeline()
        
        # Track interactions between consecutive agents
        for i in range(len(timeline) - 1):
            current_agent = timeline[i].get_agent_name()
            next_agent = timeline[i + 1].get_agent_name()
            
            if current_agent != next_agent:
                if current_agent not in interactions:
                    interactions[current_agent] = []
                if next_agent not in interactions[current_agent]:
                    interactions[current_agent].append(next_agent)
        
        return interactions
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics from the log."""
        if not self.entries:
            return {}
        
        timeline = self.get_timeline()
        first_entry = timeline[0] if timeline else None
        last_entry = timeline[-1] if timeline else None
        
        total_duration = None
        if first_entry and last_entry:
            start_time = first_entry.get_datetime()
            end_time = last_entry.get_datetime()
            if start_time and end_time:
                duration = end_time - start_time
                total_duration = str(duration)
        
        return {
            'total_entries': len(self.entries),
            'total_agents': len(self.agents),
            'unique_tasks': len(set(e.task_name for e in self.entries)),
            'completed_tasks': sum(1 for e in self.entries if e.status.lower() == 'completed'),
            'started_tasks': sum(1 for e in self.entries if e.status.lower() == 'started'),
            'total_duration': total_duration,
            'first_timestamp': first_entry.get_formatted_timestamp() if first_entry else None,
            'last_timestamp': last_entry.get_formatted_timestamp() if last_entry else None,
        }
