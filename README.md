# AI Cover Letter Generator

AI Cover Letter Generator is a Streamlit web application designed to help job seekers quickly generate personalized cover letters. It leverages the OpenAI API to create a cover letter based on the user's curriculum vitae (CV) and the job description provided. The application supports multiple languages, offering a global utility.

## Prerequisites

Before running the application, make sure you have the following prerequisites installed:

- Python 3.6 or higher
- Streamlit
- An active OpenAI API Key


You can install Streamlit using pip:

```bash
pip install streamlit
```

## Installation

Clone the AI Cover Letter Generator repository from GitHub:

```bash
git clone https://github.com/hheydaroff/ai-cover-letter-generator.git
cd ai-cover-letter-generator
```

## Setup

1. Setup virtual environment so your packages are local to this repository, and it doesn't interfere with your system wide packages. 
```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python packages
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application, use the following command in your terminal:

```bash
streamlit run app.py
```

After running the command, Streamlit will start a web server, and you'll be provided with a local URL that you can open in your web browser to use the application.

## How to Use

1. Open the application in your web browser.
2. Upload your CV in PDF, DOCX, or TXT format.
3. Paste the job description into the designated text area.
4. Select the language for the cover letter.
5. Enter your OpenAI API Key in the sidebar (kept confidential).
6. Click "Generate Cover Letter" to process and display your personalized cover letter.

## Features

- **CV Upload**: Securely upload your CV to extract relevant information.
- **Job Description Input**: Paste the job description directly into the application.
- **Multi-language Support**: Choose from a variety of languages for your cover letter.
- **OpenAI Integration**: Utilize OpenAI's API to generate a professional cover letter.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change. Make sure to update tests as appropriate.

## License

This project is open-source and available under the MIT license. See the LICENSE file for more details.
