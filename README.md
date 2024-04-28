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

Install the required dependencies with Poetry:

```bash
make install
```

Create a `.env` file in the root of the project and add the following environment variables:

```dotenv
SEARCH_API_KEY=your_google_search_api_key
CX_KEY=your_google_cx_key

MODEL_PATH=/full/path/to/your/model
```

Instructions on how to get a Google Search Api and Google CX
Key: [HERE](https://developers.google.com/custom-search/v1/introduction)

These are only needed if you need to do google queries

### Usage

To onboard a new function to be used by the LLM, you need to:

- Add a function in the function folder
    - The functions need to be added in a specific way, with declared type hints,
      and examples such as [this example](functions/location.py)
- Add it to this `function/__init__` file [here](functions/__init__.py)
- You might want to add a few shot prompt example for your function in the [data/few_shots.json](data/few_shots.json)
  file.
- Our sample queries for our sample functions are at [evals/regular.py](evals/regular.py) but for the `caller.call` all
  you need
  is to add a list of queries.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
