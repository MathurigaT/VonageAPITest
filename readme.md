# `Vonage Conversation API Test Suite`

This repository has test suites to test conversation APIs of Vonage. This is implemented using `pytest` framework and python.

### Prerequisite

01. API Specification of Vonage Conversation API V-01 https://developer.vonage.com/api/conversation?theme=dark#conversation
02. Python (Refer:https://realpython.com/installing-python/)
03. Requests (`pip install requests`)
04. Pytest (`pip install pytest`)
05. `pip install pytest-html`
06. Valid JWT token (https://developer.vonage.com/jwt)

### How to run test case

01. Fill the relevant values in config.ini
02. Navigate to <home>/VonageAPITesting/Conversations directory
03. Execute command: pytest <test_file_name> --html=report.html Eg: (`pytest test_conversationRecordAPITest.py --html=report.html`)

Report will be generated in <home>/VonageAPITesting/Conversations