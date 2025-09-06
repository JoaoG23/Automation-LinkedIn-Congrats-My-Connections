# LinkedIn Congratulations Automation 🎉

<img src="./assets/icon.ico" align="right">

## 1. Introduction

This project automates sending congratulations to your LinkedIn connections who have new job updates. It uses Python, Selenium, and WebDriver Manager to navigate LinkedIn's interface and automatically send congratulatory messages to connections with recent job changes.

## 2. Technologies Used 📲

- **Python 3.x**
- **Google Chrome**
- **Selenium WebDriver**
- **WebDriver Manager**
- **python-dotenv**

## 3. Installation 🛠️

### Steps to install:

1. Clone the repository:
   ```bash
   git clone https://github.com/JoaoG23/Automation-LinkedIn-Congrats-My-Connections.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Automation-LinkedIn-Congrats-My-Connections
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following content:
   ```env
   USER_LINKEDIN="your_linkedin_email@example.com"  # LinkedIn username/email
   PASSWORD_LINKEDIN="your_password"                # LinkedIn password
   ```

5. Run the automation:
   ```bash
   python __init__.py
   ```

## 4. Features ✔️

- [x] **Automatic Login**: Logs into LinkedIn using provided credentials
- [x] **Navigate to Connections**: Automatically navigates to "My Network" section
- [x] **Find Updated Connections**: Locates connections with recent job updates
- [x] **Scroll Through Connections**: Automatically scrolls through the connections list
- [x] **Send Congratulations**: Sends congratulatory messages to connections with new jobs
- [x] **Error Handling**: Comprehensive error handling and logging
- [x] **Logging System**: Detailed logging of all operations

## 5. How It Works 🔧

1. **Login Process**: The automation logs into LinkedIn using your credentials
2. **Navigation**: Navigates to the "My Network" section and clicks on "Updated connections"
3. **Scrolling**: Scrolls through the connections list to load all available connections
4. **Detection**: Identifies connections who have new job updates
5. **Congratulation Sending**: Automatically sends congratulatory messages to these connections

## 6. Project Structure 📁

```
Automation-LinkedIn-Congrats-My-Connections/
├── __init__.py                                    # Main execution file
├── connect_people/
│   ├── do_login/
│   │   └── do_login.py                           # Login functionality
│   ├── encode_message_for_url/
│   │   └── encode_message_for_url.py             # URL encoding utilities
│   ├── search_people_and_connect/
│   │   └── search_people_and_connect.py          # People search functionality
│   └── verify_connection_required_email/
│       └── verify_connection_required_email.py   # Email verification
├── send_congrats_to_connectios/
│   ├── send_congrats_to_connectios.py            # Main congratulations logic
│   └── scroll_by_limit_connections/
│       └── scroll_by_limit_connections.py        # Scrolling functionality
├── utils/
│   ├── logging/
│   │   └── log_manager/
│   │       └── log_manager.py                    # Logging system
│   └── wait_for_element_load/
│       └── wait_for_element_load.py              # Element waiting utilities
├── logs/
│   └── logs.log                                  # Application logs
├── assets/
│   └── icon.ico                                  # Project icon
├── requirements.txt                              # Python dependencies
└── README.md                                     # This file
```

## 7. Usage 👨‍💻

1. **Setup**: Fill in your LinkedIn credentials in the `.env` file
2. **Run**: Execute `python __init__.py`
3. **Monitor**: Watch the automation work and check the logs for detailed information

### Important Notes:
- The automation will automatically handle scrolling and clicking
- Each congratulation is sent with appropriate delays to avoid rate limiting
- All actions are logged for monitoring and debugging

## 8. Requirements 📋

- **LinkedIn Account**: A registered LinkedIn account is required
- **Chrome Browser**: Google Chrome must be installed
- **Internet Connection**: Stable internet connection required
- **Python 3.x**: Python 3.6 or higher

## 9. Benefits and Limitations 🛠️

### Benefits:
- **Time Saving**: Automates the tedious process of congratulating connections
- **Consistency**: Ensures you don't miss congratulating important connections
- **Professional Networking**: Helps maintain and strengthen professional relationships
- **Automated Logging**: Detailed logs for monitoring and debugging

### Limitations:
- **LinkedIn Rate Limits**: LinkedIn may restrict automated actions
- **UI Changes**: LinkedIn interface changes may require code updates
- **Internet Dependency**: Requires stable internet connection
- **Browser Dependency**: Requires Chrome browser installation

## 10. Logging 📊

The application includes a comprehensive logging system:
- **Log Location**: `logs/logs.log`
- **Log Rotation**: Automatic log rotation (5MB per file, 3 backups)
- **Log Levels**: Info and Error levels
- **Timestamp**: All logs include timestamps

## 11. Error Handling 🛡️

The automation includes robust error handling for:
- WebDriver exceptions
- Element not found errors
- Invalid selector exceptions
- Timeout exceptions
- General exceptions

## 12. Author 👨‍💻

<img style="border-radius:50%;" src="https://avatars.githubusercontent.com/u/80895578?v=4" width="100px;" alt=""/>

**Joao Guilherme** 🚀

Developed with 🤖 by Joao Guilherme 👋🏽 Contact me via:

[![Linkedin Badge](https://shields.io/badge/-Joao%20Guilherme-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/joaog123/)](https://www.linkedin.com/in/joaog123/)  
[![Email Badge](https://shields.io/badge/-joaoguilherme94@live.com-c80?style=flat-square&logo=Microsoft&logoColor=white&link=mailto:joaoguilherme94@live.com)](mailto:joaoguilherme94@live.com)

## 13. License 📄

[![License](https://shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

## 14. Disclaimer ⚠️

This automation tool is for educational and personal use only. Please ensure you comply with LinkedIn's Terms of Service and use responsibly. The authors are not responsible for any misuse of this tool.  
