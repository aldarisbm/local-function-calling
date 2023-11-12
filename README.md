# Local Function Calling

Welcome to the Local Function Calling repository! This Python project is designed to assist you in choosing the right
functions that can effectively respond to a specific query. Whether you're working on natural language processing, data
analysis, or any other domain that involves functions handling queries, this tool can streamline the process of
selecting the most suitable functions for your needs.

## Getting Started

To get started with the Local Function Calling project, follow these steps:

### Prerequisites

Make sure you have the following prerequisites installed:

- Python (version 3.6 or later)
- [Poetry](https://python-poetry.org/) (version 1.1.7 or later)

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/aldarisbm/local-function-calling.git
```

Navigate to the project directory:

```bash
cd local-function-calling
```

Install the required dependencies with Poetry:

```bash
poetry install
```

Create a `.env` file in the root of the project and add the following environment variables:

```dotenv
SEARCH_API_KEY=your_google_search_api_key
CX_KEY=your_google_cx_key
```

Replace `your_google_search_api_key` and `your_google_cx_key` with your
actual [Google Custom Search API](https://developers.google.com/custom-search/v1/introduction) keys.

These are needed for using google queries.

### Usage

WIP

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
