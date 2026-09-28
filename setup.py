from setuptools import setup, find_packages

setup(
    name="autonomous_financial_research_agent",
    version="1.0.0",
    description="ARA-1: Autonomous Financial Research Agent with Multi-Source Synthesis",
    author="Agentic AI Engineer",
    packages=find_packages(include=["agent*", "tools*", "memory*", "synthesis*", "evaluation*"]),
    python_requires=">=3.9",
    install_requires=[
        "langchain>=0.2.0",
        "langgraph>=0.1.0",
        "pydantic>=2.0.0",
        "requests>=2.31.0",
        "httpx>=0.27.0",
        "tenacity>=8.2.0",
        "rich>=13.0.0",
        "python-dotenv>=1.0.0",
    ],
)
