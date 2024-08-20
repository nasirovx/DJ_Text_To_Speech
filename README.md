# Django Project for Text-to-Speech  
 
This Django project allows converting text to audio files and saving them.

## Features  

- Conversion of text to speech in multiple languages.
- Saving generated audio files with unique names. 
- Basic administrative functions through Django Admin.
 
## Installation
 
1. **Clone the repository:** 

    ```bash
    git clone git@github.com:nasirovx/DJ_Text_To_Speech.git
    cd DJ_Text_To_Speech
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv  
    ```

3. **Activate the virtual environment:**

    - On Windows: 
 
        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

7. **Open the browser and go to [http://localhost:8000/admin](http://localhost:8000/admin) to access Django Admin.**

8. **Log in using administrative credentials and start using the text-to-speech functionality.**

## Usage

1. Log in to Django Admin and navigate to the "Text to Speech" section.

2. Create a new entry by providing the text and a unique file name. Optionally, you can select the language for the speech.

3. Save the entry, and the corresponding audio file will be generated and saved in the `voice/` directory.

4. To listen to or download the generated audio, go to the detail page of the entry in Django Admin and click on the provided link.

## Contribution

Contributions are welcome! If you have ideas for improvements or new features, feel free to create an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
