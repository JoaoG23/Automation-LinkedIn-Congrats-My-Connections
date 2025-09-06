## LinkedIn New Connections Automation 🤝

<img src="./assets/icon.ico" align="right">

### 1. Introduction  

## Time: 6,5

This project automates connecting with new people on LinkedIn based on a specified job description. It uses Python, Selenium, and Webdriver Manager to navigate and interact with LinkedIn's web interface.

### 2. Technologies Used 📲  

- **Python**  
- **Google Chrome**  
- **Selenium**  
- **Webdriver Manager**  

### 3. Installation 🛠️  

### Steps to install:  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/JoaoG23/linkedin-connections-automation.git  
   ```  
2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  
3. Create a `.env` file with the following content:  
   ```env  
   DESCRIPTION="tech recruiter"  # Data searched  
   USER_LINKEDIN=""  # LinkedIn username  
   PASSWORD_LINKEDIN=""  # LinkedIn password  
   LIMIT_CONNECTIONS=30  # Maximum number of connections  
   ```  
4. Run **python __init__.py**

### 4. Features ✔️  

- [x] Access LinkedIn web page.
- [x] Log in using provided username and password.
- [x] Search for people based on a job description.
- [x] Connect with individuals:
    - [x] Navigate through pages.
    - [x] If user need one message,the app will sent it
    - [x] Send connection requests until reaching the connection limit.

### 5. Usage 👨‍💻  

1. Fill in your LinkedIn credentials and the search description in the `.env` file.  
2. Run the script:  
   ```bash  
   python __init__.py  
   ```  

### 6. Requirements  

- A registered LinkedIn account is required.

### 7. Benefits and Limitations 🛠️  

#### Benefits:  
- Automates the process of connecting with multiple people on LinkedIn.
- Saves time by avoiding manual connection requests.

#### Limitations:  
- LinkedIn's rate limits can restrict the number of connections per day.
- Internet connection is required.

### 8. Author  

 <img style="border-radius:50%;" src="https://avatars.githubusercontent.com/u/80895578?v=4" width="100px;" alt=""/>  
 <br />  
 <sub><b>Joao Guilherme</b></sub></a> <a href="https://github.com/JoaoG23/">🚀</a>  

Developed with 🤖 by Joao Guilherme 👋🏽 Contact me via:  

[![Linkedin Badge](https://shields.io/badge/-Joao%20Guilherme-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/joaog123/)](https://www.linkedin.com/in/joaog123/)  
[![Email Badge](https://shields.io/badge/-joaoguilherme94@live.com-c80?style=flat-square&logo=Microsoft&logoColor=white&link=mailto:joaoguilherme94@live.com)](mailto:joaoguilherme94@live.com)  

## 9. License 📄  

[![License](https://shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)  
