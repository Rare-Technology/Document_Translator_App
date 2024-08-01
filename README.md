## Translation  Application

The Translation application is a internal Rare tool to support the users for translating text and documents to another target language.

The app is designed such that any files uploaded to the application will be deleted once the translation is complete and the file has been downloaded. 

The application has been developed using Python on Streamlit and the deployment has been done using Docker and hosting on DigitalOcean server.

The application is currently in the Pilot testing phase.

### About the App

1. It has 2 options - text and document translation (available on the sidebar on the landing page)
2. The services automatically detects the input language (source language in the input document/text) and translates it to the target language users select.
3. For document translation, make sure to  choose a target language different from your document's language (e.g., if your document is in English, select a different target language like Portuguese).
4. The translation is supported for document types - PDF, DOCX, PPTX, and TXT (per DeepL restrictions).

### File Structure:

1. `translator.py`: contains the source code of the application
2. `Dockerfile`: Used to create the container image for deploying the applcication.
3. `configs/app.env`: contains the environment variable for DeepL API key.
4. `requirements.txt`: contains all python dependencies for running the application
5. `images/files`: has all related images being used in the application

### Overview - Development & Testing the Application 

1. For development and testing the application, clone the github repository from https://github.com/Rare-Technology/Document_Translator_App.git to your local directory.
2. In the config/app.env, make sure to enter the DeepL API Key

    The API Key can be obtained by contacting Rare's IT Team.

3. All changes to the app (functionality and UI) should only be done in the `translator.py` file, more utility files and helper functions may be added to the repo and included in the source code.
4. For testing the application locally using the command 'streamlit run translator.py' in the terminal.

    The resulting application will be available on "localhost:8501" on your web browser.

    ! Make sure the terminal is set to the current working directory where the .py file sits when running the app. !

### Future Upgrades

1. Update UI
2. Implement Logging for the app for better debugging and issue resolution
3. Update exception handling
4. To be continued....

### Current Issues

1. Chinese (Traditional) is not supported with DeepL - The app throws an error when trabslating to Chinese (Traditional)
2. To be continued....

### Encountered an Error?!

Submit a ticket at sos@rare.org describing the issue in detail and do include the error message encountered! Screenshots are welcome and much appreciated!