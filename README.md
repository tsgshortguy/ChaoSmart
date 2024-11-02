# ChaoSmart - PC Utility Tool

ChaoSmart is a comprehensive and visually stunning PC utility tool designed to provide users with real-time system monitoring, network information, file management, process control, registry editing, and startup management. Built with Python and PyQt5, ChaoSmart combines functionality with an interactive and modern user interface to enhance your computing experience.

## Table of Contents

- [Features](#features)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **Real-Time System Information**
  - Monitors and displays CPU, Memory, and Disk usage with interactive progress bars.
  
- **Network Information**
  - Shows your computer's hostname and IP address.
  
- **File Explorer**
  - Browse and manage your directories and files with ease. Double-click folders to navigate and files to open.
  
- **Process Manager**
  - View all running processes with details like PID, Name, and CPU usage. Terminate unwanted processes directly from the app.
  
- **Registry Editor**
  - Access and view Windows Registry keys and their values.
  
- **Startup Manager**
  - Manage applications that run at system startup. Enable or disable startup items to optimize boot times.
  
- **Interactive and Modern UI**
  - Features vibrant colors, smooth animations, progress bars, and responsive layouts for an engaging user experience.
  
- **Automatic Refresh**
  - System metrics update automatically every 3 seconds to provide up-to-date information without manual intervention.

## Usage

1. **System Info Tab**
   - View real-time CPU, Memory, and Disk usage through interactive progress bars.

2. **Network Info Tab**
   - Check your computer's hostname and IP address.

3. **File Explorer Tab**
   - Browse through your directories. Double-click folders to navigate or files to open them with their default applications.

4. **Process Manager Tab**
   - View all running processes with details like PID, Name, and CPU usage.
   - Select a process and click **"Kill Selected Process"** to terminate it. *Use this feature responsibly.*

5. **Registry Editor Tab**
   - Enter a registry key path (e.g., `HKEY_CURRENT_USER\Software`) and click **"Load Key"** to view its values.

6. **Startup Manager Tab**
   - Manage applications that run at system startup.
   - Select a startup item and click **"Enable Selected"** or **"Disable Selected"** to control its startup behavior.

7. **Refresh All Button**
   - Although system metrics auto-refresh every 3 seconds, you can manually refresh all tabs by clicking this button if needed.

## Contributing

Contributions are welcome! Follow these steps to contribute to ChaoSmart:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
