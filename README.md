# CrewAI Execution Tracker 🤖

A Streamlit-based application for visualizing and analyzing CrewAI execution logs. This tool helps you understand how AI agents collaborate, track their task execution, and analyze interaction patterns.

## Features

- **📂 File Upload**: Upload any CrewAI JSON log file or use the sample data
- **👥 Crew Member Overview**: View all agents with their roles and task statistics
- **📊 Two-Pane Layout**: 
  - Left pane: List of crew members with completion rates
  - Right pane: Detailed task history and interactions
- **📈 Statistics Dashboard**: Track total tasks, completion rates, and execution duration
- **🔄 Timeline View**: Visualize the chronological flow of task execution
- **🎯 Interactive Selection**: Click on any crew member to see their detailed contributions
- **📋 Task Analysis**: View task descriptions, outputs, and key actions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shivomthakkar/crew_ui.git
cd crew_ui
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload a CrewAI log file (JSON format) or click "Load Sample Log" to see example data

4. Explore the visualization:
   - Select crew members from the left panel
   - View detailed task history in the right panel
   - Check the timeline tab for chronological view
   - Analyze statistics and interaction patterns

## Log File Format

The application expects JSON log files with the following structure:

```json
[
  {
    "timestamp": "2025-12-27 11:49:05",
    "task_name": "task_identifier",
    "task": "Description of the task being performed",
    "agent": "Agent name or description",
    "status": "started|completed|failed",
    "output": "Optional output or result from the task"
  }
]
```

## Project Structure

```
crew_ui/
├── app.py                 # Main Streamlit application
├── log_parser.py          # Log parsing and data processing
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── knowledge/
    └── crew_ui/
        └── sample_logs.json  # Sample log file for testing
```

## Key Components

### `app.py`
- Main Streamlit application
- Handles UI layout and interactions
- Manages session state for selected agents
- Renders visualizations and statistics

### `log_parser.py`
- Parses JSON log files
- Extracts agent information and task details
- Calculates statistics and completion rates
- Builds interaction graphs

## Features in Detail

### Agent Cards
Each crew member is displayed with:
- Name and role
- Total tasks assigned
- Completed vs in-progress tasks
- Visual completion rate indicator

### Task Entries
Detailed task information includes:
- Timestamp and duration
- Task name and description
- Current status (started/completed/failed)
- Output or results (if available)
- Extracted key actions

### Statistics Dashboard
- Total number of agents
- Overall task count
- Unique task types
- Total execution duration
- Completion rates

### Timeline View
- Chronological display of all tasks
- Color-coded by status
- Quick overview of execution flow

## Customization

The application can be customized by modifying:
- CSS styles in `app.py` for visual appearance
- Parser logic in `log_parser.py` for different log formats
- Dashboard metrics and visualizations

## Requirements

- Python 3.8+
- Streamlit 1.28.0+
- Pandas 2.0.0+
- Plotly 5.17.0+

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please open an issue on GitHub or contact the maintainers.

---

Built with ❤️ using Streamlit
