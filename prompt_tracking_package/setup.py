from setuptools import setup, find_packages

setup(
    name="prompt_tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "python-dotenv",
        "google-generativeai",
        "transformers",
        "stanza"
    ],
    entry_points={
        "console_scripts": [
            "prompt_tracker=prompt_tracker.tracker:PromptTracker"
        ]
    },
)
