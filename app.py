import streamlit as st
import json
from pathlib import Path
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from log_parser import CrewLogParser, CrewLogEntry, AgentSummary

# Page configuration
st.set_page_config(
    page_title="CrewAI Log Visualizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""<style>
    .agent-card {
        background-color: #81c391;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #4CAF50;
    }
    .agent-card.selected {
        background-color: #81c391;
        border-left-color: #28a745;
    }
    .task-entry {
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        border: 1px solid #dee2e6;
    }
    .status-badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
    }
    .status-completed {
        background-color: #d4edda;
        color: #155724;
    }
    .status-started {
        background-color: #cce5ff;
        color: #004085;
    }
</style>""", unsafe_allow_html=True)

def load_sample_log():
    sample_path = Path("knowledge/crew_ui/sample_logs.json")
    if sample_path.exists():
        with open(sample_path, 'r') as f:
            return f.read()
    else:
        return json.dumps([
            {
                "timestamp": "2025-12-27 11:49:05",
                "task_name": "product_engineer_scrum_task",
                "task": "Take the solution design and implementation plan from the Solution Analyst and create detailed, actionable tasks for a team of engineers to implement.",
                "agent": "Technical Delivery Manager who orchestrates agents to achieve seamless delivery",
                "status": "started"
            },
            {
                "timestamp": "2025-12-27 11:52:19",
                "task_name": "product_engineer_scrum_task",
                "task": "Continuing the implementation planning and task breakdown.",
                "agent": "Technical Delivery Manager who orchestrates agents to achieve seamless delivery",
                "status": "completed",
                "output": "Task breakdown completed with 10 actionable items."
            },
            {
                "timestamp": "2025-12-27 12:11:46",
                "task_name": "codebase_helper_task",
                "task": "Answer questions about the codebase and provide deep technical analysis.",
                "agent": "Senior Python Engineer with expertise in code analysis",
                "status": "started"
            },
            {
                "timestamp": "2025-12-27 12:22:00",
                "task_name": "codebase_helper_task",
                "task": "Completed codebase analysis and documentation.",
                "agent": "Senior Python Engineer with expertise in code analysis",
                "status": "completed",
                "output": "Codebase analysis complete. Found 5 modules requiring updates."
            }
        ], indent=2)

def render_agent_card(agent, is_selected=False):
    card_class = "agent-card selected" if is_selected else "agent-card"
    completion_rate = agent.get_completion_rate()
    status_emoji = "✅" if completion_rate == 100 else "🔄" if completion_rate > 0 else "⏳"
    
    return f"""<div class="{card_class}">
        <h4>{status_emoji} {agent.name}</h4>
        <p style="color: #666; font-size: 12px;">{agent.role}</p>
        <div>📋 Tasks: {agent.total_tasks}<br>
        ✅ Completed: {agent.completed_tasks}<br>
        🔄 In Progress: {agent.started_tasks}</div>
        <div style="margin-top: 10px;">
            <div style="background-color: #e9ecef; border-radius: 4px; height: 8px;">
                <div style="background-color: #28a745; width: {completion_rate}%; height: 100%; border-radius: 4px;"></div>
            </div>
            <span style="font-size: 11px;">{completion_rate:.1f}% Complete</span>
        </div>
    </div>"""

def render_task_entry(entry):
    status_class = f"status-{entry.status.lower()}"
    return f"""<div class="task-entry">
        <div style="display: flex; justify-content: space-between;">
            <span class="status-badge {status_class}">{entry.status.upper()}</span>
            <span style="color: #6c757d; font-size: 12px;">{entry.get_formatted_timestamp()}</span>
        </div>
        <h4>{entry.task_name}</h4>
        <p>{entry.get_task_summary(300)}</p>
        {f'<div style="background-color: #1A1C24; padding: 10px; border-radius: 5px;"><p>Output: {entry.output[:2000]}</p></div>' if entry.output else ''}
    </div>"""

def main():
    if 'parser' not in st.session_state:
        st.session_state.parser = None
    if 'selected_agent' not in st.session_state:
        st.session_state.selected_agent = None
    
    st.title("🤖 CrewAI Log Visualizer")
    st.markdown("Visualize and analyze CrewAI agent interactions and task execution")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload CrewAI Log File (JSON format)", type=['json', 'txt'])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📂 Load Sample Log", use_container_width=True):
            st.session_state.parser = CrewLogParser()
            if st.session_state.parser.parse_json_file(load_sample_log()):
                st.success("Sample log loaded successfully!")
    
    if uploaded_file:
        try:
            content = uploaded_file.read().decode('utf-8')
            st.session_state.parser = CrewLogParser()
            if st.session_state.parser.parse_json_file(content):
                st.success(f"✅ Successfully loaded {uploaded_file.name}")
            else:
                st.error("Failed to parse the uploaded file")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    if st.session_state.parser and st.session_state.parser.entries:
        stats = st.session_state.parser.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Agents", stats.get('total_agents', 0))
        col2.metric("Total Tasks", stats.get('total_entries', 0))
        col3.metric("Completed", stats.get('completed_tasks', 0))
        col4.metric("Started", stats.get('started_tasks', 0))
        
        st.markdown("---")
        
        col_left, col_right = st.columns([1, 2])
        
        with col_left:
            st.markdown("### 👥 Crew Members")
            agents = st.session_state.parser.get_agents_list()
            
            for agent in agents:
                if st.button(f"{agent.name}", key=f"btn_{agent.name}", use_container_width=True):
                    st.session_state.selected_agent = agent.name
                
                is_selected = st.session_state.selected_agent == agent.name
                st.markdown(render_agent_card(agent, is_selected), unsafe_allow_html=True)
        
        with col_right:
            if st.session_state.selected_agent:
                agent = st.session_state.parser.get_agent_by_name(st.session_state.selected_agent)
                if agent:
                    st.markdown(f"### 📊 {agent.name} - Detailed View")
                    
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Total Tasks", agent.total_tasks)
                    m2.metric("Completed", agent.completed_tasks)
                    m3.metric("Completion Rate", f"{agent.get_completion_rate():.1f}%")
                    
                    st.markdown("#### Task History")
                    for entry in agent.entries:
                        st.markdown(render_task_entry(entry), unsafe_allow_html=True)
            else:
                st.info("👈 Select a crew member from the left panel to view detailed information")
                
                if agents:
                    fig = go.Figure([go.Bar(
                        x=[a.name for a in agents],
                        y=[a.total_tasks for a in agents],
                        marker_color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'][:len(agents)]
                    )])
                    fig.update_layout(
                        title="Task Distribution by Agent",
                        xaxis_title="Agent",
                        yaxis_title="Number of Tasks",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Upload a CrewAI log file or click 'Load Sample Log' to get started")
        
        with st.expander("ℹ️ How to use this tool"):
            st.markdown("""
            1. **Upload a log file**: Click the file upload button and select a JSON log file
            2. **Or load sample data**: Click 'Load Sample Log' to see example data
            3. **Explore agents**: View crew members in the left panel
            4. **Select an agent**: Click on any agent to see their detailed task history
            5. **Analyze patterns**: Review statistics and task distribution
            """)

if __name__ == "__main__":
    main()