# CrewAI Execution Tracker

A minimal, real-time web application for tracking and visualizing CrewAI crew execution. Monitor agents, tasks, and execution flow through an intuitive Streamlit dashboard.

## Features

- 🔄 **Real-time Tracking**: Auto-refreshing dashboard shows live crew execution status
- 🤖 **Multi-Agent Support**: Track multiple agents and their activities simultaneously
- 📋 **Task Management**: Monitor task progress, assignments, and outputs
- 📜 **Event Logging**: Comprehensive event log for debugging and monitoring
- 🎯 **Multi-Crew Support**: Handle multiple crews running simultaneously
- 🚀 **Auto-Launch**: UI automatically opens when crew starts
- 💡 **Minimal & Fast**: Quick POC implementation, ready to demo

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

1. **Run the example crew:**
```bash
python run_crew.py
```
This will start a demo crew with tracking and automatically open the web UI.

2. **Track your own crew:**
```python
from crew_tracker import track_crew
from crewai import Crew, Agent, Task

# Create your crew
crew = Crew(
    agents=[...],
    tasks=[...]
)

# Wrap with tracking
tracked_crew = track_crew(crew, name="My Crew")

# Run with tracking
result = tracked_crew.crew.kickoff()
```

3. **Access the dashboard:**
Open http://localhost:8501 in your browser

## Project Structure

```
crew_ui/
├── crew_tracker/
│   ├── __init__.py          # Package initialization
│   ├── models.py            # Data models for tracking
│   ├── state_manager.py     # Thread-safe state management
│   ├── event_interceptor.py # Event capture mechanism
│   └── crew_wrapper.py      # CrewAI wrapper implementation
├── streamlit_app_complete.py # Streamlit web application
├── run_crew.py              # Entry point with example
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## How It Works

1. **Wrapping**: The `CrewExecutionWrapper` wraps your CrewAI crew instance
2. **Interception**: Monkey-patches crew/agent/task methods to capture events
3. **State Management**: Thread-safe `StateManager` stores execution state
4. **Event Processing**: Background thread processes events asynchronously
5. **UI Updates**: Streamlit app polls state and auto-refreshes
6. **Visualization**: Clean dashboard shows agents, tasks, progress, and logs

## Dashboard Features

- **Overview Metrics**: Status, progress, active agents, and duration
- **Agent Cards**: Current status, thoughts, actions, and task assignments
- **Task List**: All tasks with status, assignments, and outputs
- **Event Log**: Scrollable log of all execution events
- **Auto-Refresh**: Configurable refresh interval (1-10 seconds)
- **Multi-Crew Tabs**: Switch between multiple running crews

## Future Enhancements

This is a minimal POC. Future improvements could include:

- WebSocket support for true real-time updates
- Persistent state storage (database integration)
- Advanced filtering and search capabilities
- Performance metrics and analytics
- Export functionality for logs and results
- Custom event handlers and plugins
- Configuration management
- Authentication and multi-user support
- Distributed crew tracking
- Integration with CrewAI callbacks

## Known Limitations

- In-memory state storage (lost on restart)
- Basic error handling
- No authentication or security
- Single-machine deployment only
- Limited to local network access

## License

MIT License - Feel free to use and modify as needed.

## Contributing

This is a POC project. Fork and extend as needed for your use case.# CrewAI Execution Tracker

## Overview
CrewAI Execution Tracker is a comprehensive monitoring solution for CrewAI workflows, providing real-time tracking and visualization of agent tasks and execution states.

## Features
- Real-time agent status tracking
- Detailed event logging
- Interactive Streamlit dashboard
- Easy integration with CrewAI workflows

## Prerequisites
- Python 3.9+
- CrewAI
- Streamlit

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/crew-execution-tracker.git
cd crew-execution-tracker
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venvScriptsactivate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Running the Crew
```bash
python run_crew.py
```

### Viewing Execution Dashboard
```bash
streamlit run streamlit_app.py
```

## Project Structure
- `crew_tracker/`: Core tracking modules
  - `models.py`: Pydantic data models
  - `state_manager.py`: Manages crew execution state
  - `event_interceptor.py`: Intercepts and logs crew events
  - `crew_wrapper.py`: Wraps crew execution with tracking
- `streamlit_app.py`: Interactive dashboard
- `run_crew.py`: Example crew execution script

## Contributing
Contributions are welcome! Please submit a pull request.

## License
MIT License# CrewAI Execution Tracker

## Overview
A minimal Streamlit-based web application wrapper for tracking CrewAI crew execution in real-time.

## Features
- Real-time tracking of CrewAI crew execution
- Multi-session support
- Intuitive web UI
- Automatic Streamlit launch

## Prerequisites
- Python 3.8+
- CrewAI
- Streamlit

## Installation
```bash
git clone https://github.com/shivomthakkar/crew_ui.git
cd crew_ui
pip install -r requirements.txt
```

## Quick Start
```bash
python run_crew.py
```

## Technical Architecture
- `crew_tracker/models.py`: Data models for crews, agents, tasks
- `crew_tracker/state_manager.py`: Thread-safe state management
- `crew_tracker/event_interceptor.py`: CrewAI execution event capturing
- `streamlit_app.py`: Real-time tracking Streamlit UI
- `run_crew.py`: Crew execution entry point

## TODO / Future Enhancements
- [ ] Enhanced error handling
- [ ] More granular task tracking
- [ ] Persistent state storage
- [ ] Advanced filtering and search
- [ ] Support for distributed crew execution

## Contributing
PRs welcome! Please follow standard GitHub contribution guidelines.

## License
MIT License# CrewAI Execution Tracker

## Overview
A lightweight, real-time tracking solution for CrewAI workflows.

## Features
- Real-time crew execution monitoring
- Multiple crew tracking
- Streamlit-based web interface
- Minimal performance overhead

## Prerequisites
- Python 3.9+
- Streamlit
- CrewAI

## Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`

## Configuration
Customize tracking by modifying `app.py`

## Future Enhancements
- Persistent logging
- Advanced filtering
- Export capabilities

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and development process.

## License
MIT License# crew_ui
