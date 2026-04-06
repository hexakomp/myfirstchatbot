# LangChain with Ollama: Topic-Wise Tutorial Notes

This document provides a clean, professional, topic-wise introduction to LangChain using Ollama. It focuses on six practical topics: LangChain basics with Ollama, prompt templates, structured output, memory, chains, and routing. These topics are commonly used in introductory LangChain learning material and align with current LangChain concepts and documentation.[1][2][3]

## Setup and prerequisites

Before working through the topics, install Ollama locally, pull a model, and install the Python libraries required for LangChain, Ollama integration, and optional UI testing with Gradio. `ChatOllama` is the LangChain integration used to send chat-style requests to a locally running Ollama server.[1][4]

### Suggested installation

```bash
pip install langchain langchain-core langchain-community langchain-ollama python-dotenv gradio
```

### Start Ollama

```bash
ollama serve
```

### Pull a model

```bash
ollama pull gemma3:270m
```

## Topic 1: Ollama LangChain Basics

This topic introduces the most basic LangChain flow: create a chat model object, send messages, and return the model response. The key class here is `ChatOllama`, which provides a LangChain-compatible interface for local Ollama models.[1][4]

### Learning objectives

- Understand how LangChain connects to a local Ollama server
- Create and configure a `ChatOllama` model
- Send system and human messages to the model
- Build a minimal chatbot with Gradio

### Concept

In a basic LangChain chat application, the model receives a list of role-based messages such as `system` and `human`, and returns a generated response. This pattern is the foundation for almost every LangChain application built on chat models.[1]

### Complete example

```python
from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama
import gradio as gr

load_dotenv()

llm = ChatOllama(
    url="http://localhost:11434",
    model="gemma3:270m",
    temperature=0.7,
    api_key="ollama"
)

systemmessage = "You are a Teacher. Answer the question in a concise manner."

def chatbot_response(user_input):
    messages = [
        ("system", systemmessage),
        ("human", user_input),
    ]
    ai_msg = llm.invoke(messages).content
    return ai_msg

iface = gr.Interface(
    fn=chatbot_response,
    inputs="text",
    outputs="text",
    title="My First Chatbot"
)

iface.launch()
```

### What this code teaches

- `ChatOllama` initializes the local language model connection.[1]
- `invoke()` sends the message list to the model and returns the response object.[1]
- A Gradio interface can wrap the LangChain call into a very simple chat app.

### Practice ideas

- Change the system role from teacher to recruiter, doctor, or coding assistant
- Try different Ollama models and compare tone and speed
- Add a `temperature` change and observe response variation

## Topic 2: Prompt Templates and ChatPromptTemplate

Prompt templates make prompts reusable and easier to maintain. `ChatPromptTemplate` is designed for chat models and helps define structured prompts with variables across system and user messages.[5][6]

### Learning objectives

- Understand why prompt reuse matters
- Create prompts with variables
- Use `ChatPromptTemplate` for chat-style prompting
- Build a prompt-plus-model pipeline

### Concept

A prompt template separates prompt structure from runtime values. Instead of manually rewriting prompts for every request, placeholders such as `{topic}` can be filled dynamically at invocation time.[5][6]

### Complete example

```python
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(
    url="http://localhost:11434",
    model="gemma3:270m",
    temperature=0.7,
    api_key="ollama"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful tutor. Explain the topic in simple language."),
    ("human", "Explain {topic} in 5 bullet points.")
])

chain = prompt | llm

result = chain.invoke({"topic": "LangChain prompt templates"})
print(result.content)
```

### What this code teaches

- `ChatPromptTemplate.from_messages()` creates a reusable chat prompt.[5][6]
- Variables such as `{topic}` are replaced at runtime.
- The `|` operator forms a simple LangChain pipeline from prompt to model.

### Practice ideas

- Replace `topic` with `language`, `framework`, or `business_problem`
- Add a second variable such as `{level}` for beginner or advanced explanations
- Create separate system prompts for tutor, reviewer, and summarizer roles

## Topic 3: Structured Output with Parsers and Schemas

Structured output is used when the response must be machine-friendly rather than plain free text. LangChain supports structured output patterns through schemas and parsers, including `ResponseSchema` and `StructuredOutputParser`.[2][3]

### Learning objectives

- Understand why free-form output is difficult to automate
- Define expected fields using response schemas
- Instruct the model to return structured output
- Parse model output into a Python dictionary-like structure

### Concept

Applications often need predictable fields such as `name`, `price`, `priority`, or `summary`. A structured parser gives the model explicit output instructions and helps convert the response into data that is easier to validate and use in downstream code.[2][3]

### Complete example

```python
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

llm = ChatOllama(
    url="http://localhost:11434",
    model="gemma3:270m",
    temperature=0.0,
    api_key="ollama"
)

response_schemas = [
    ResponseSchema(name="gift", description="gift item name"),
    ResponseSchema(name="delivery_days", description="number of days for delivery"),
    ResponseSchema(name="price_value", description="price as a number")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant that returns structured output only."),
    ("human", "Suggest a gift for {person}. {format_instructions}")
])

chain = prompt | llm

response = chain.invoke({
    "person": "a 10 year old child",
    "format_instructions": format_instructions
})

parsed = output_parser.parse(response.content)
print(parsed)
```

### What this code teaches

- `ResponseSchema` defines the expected fields in the output.[3]
- `StructuredOutputParser` generates formatting guidance for the model and parses the result.[3]
- Structured output is useful when model results must be consumed by APIs, databases, or UI forms.[2]

### Practice ideas

- Create a parser for job screening results with `candidate_name`, `score`, and `remarks`
- Create a parser for meeting notes with `summary`, `action_items`, and `owner`
- Compare raw text output versus structured output for the same prompt

## Topic 4: Basic Memory Types

Memory allows a conversational application to retain context between turns. Introductory LangChain learning commonly covers buffer memory, window memory, token-based memory, and summary memory as core patterns for stateful conversation handling.

### Learning objectives

- Understand stateless versus stateful chat applications
- Learn the purpose of conversation memory
- Explore common memory strategies
- Choose the right memory style for different use cases

### Concept

Without memory, each request is treated independently. With memory, a chatbot can remember previous user questions, maintain continuity, and produce more natural multi-turn interactions.

### Complete example

This example demonstrates how to use `ConversationBufferMemory` with `ConversationChain` to create a stateful conversation where the model remembers previous interactions.

```python
from langchain_ollama import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Initialize the model
llm = ChatOllama(
    url="http://localhost:11434",
    model="gemma3:270m",
    temperature=0.7,
    api_key="ollama"
)

# Initialize memory to store history
memory = ConversationBufferMemory()

# Create a conversation chain that uses the model and memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True # Set to True to see the prompt and history in the console
)

# Turn 1
print("--- Turn 1 ---")
response1 = conversation.predict(input="Hi, my name is Alice.")
print(f"AI: {response1}")

# Turn 2 - The model will remember the name even if not explicitly provided again
print("\n--- Turn 2 ---")
response2 = conversation.predict(input="What is my name?")
print(f"AI: {response2}")
```

### Memory types to understand

- **ConversationBufferMemory**: The simplest form of memory. It stores the **entire history** of the conversation as a raw string. While accurate, it can eventually hit the model's token limit as the conversation grows very long.
- **ConversationBufferWindowMemory**: Keeps a sliding window of the **last `k` interactions** (where one interaction is a human message and an AI response). This prevents the history from growing indefinitely but loses context from older parts of the conversation.
- **ConversationTokenBufferMemory**: Similar to window memory, but uses a **token limit** instead of a turn count. It flushes the oldest messages to stay within a specific budget (e.g., 2000 tokens), making it more precise for managing model context limits.
- **ConversationSummaryMemory**: Instead of storing raw messages, it uses a language model to **summarize the conversation** as it flows. It passes the summary into the prompt. This is efficient for very long conversations where you want to keep the "gist" of the history without using too many tokens.

### Practice ideas

- Build a chatbot that remembers the user’s name
- Compare buffer memory with summary memory for long chats
- Observe how short memory windows affect follow-up questions

## Topic 5: Simple and Sequential Chains

Chains connect prompt-processing steps into a repeatable workflow. Introductory LangChain material commonly presents `LLMChain`, `SimpleSequentialChain`, and `SequentialChain` to show how single-step and multi-step pipelines are constructed.[7]

### Learning objectives

- Understand what a chain is
- Build a simple prompt-to-model workflow
- Pass output from one stage into another
- Create multi-step pipelines with multiple inputs and outputs

### Concept

A chain is a sequence of operations applied to an input. In the simplest case, the operations are just prompt preparation and model invocation. In more advanced cases, one model output becomes the input for another step, allowing summarization, transformation, question generation, and similar workflows.[7]

### Complete example: basic chain

```python
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOllama(
    url="http://localhost:11434",
    model="gemma3:270m",
    temperature=0.7,
    api_key="ollama"
)

prompt1 = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple English in 3 lines."
)

chain1 = LLMChain(llm=llm, prompt=prompt1)

result = chain1.invoke({"topic": "LangChain chains"})
print(result["text"])
```

### Complete example: sequential chain

```python
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

llm = ChatOllama(
    url="http://localhost:11434",
    model="gemma3:270m",
    temperature=0.7,
    api_key="ollama"
)

prompt1 = PromptTemplate(
    input_variables=["topic"],
    template="Write a short explanation of {topic}."
)

prompt2 = PromptTemplate(
    input_variables=["summary"],
    template="Convert this explanation into 3 interview questions: {summary}"
)

chain1 = LLMChain(llm=llm, prompt=prompt1, output_key="summary")
chain2 = LLMChain(llm=llm, prompt=prompt2, output_key="questions")

sequential_chain = SequentialChain(
    chains=[chain1, chain2],
    input_variables=["topic"],
    output_variables=["summary", "questions"]
)

result = sequential_chain.invoke({"topic": "LangChain"})
print(result)
```

### What this code teaches

- `LLMChain` wraps a prompt and model into a reusable unit.[7]
- `SequentialChain` connects multiple reusable units into a larger flow.
- Multi-step chain design is useful for summarizing, transforming, and enriching content before delivery.

### Practice ideas

- Generate a blog title and then generate a blog outline
- Summarize meeting notes and then create action items
- Explain a concept and then generate quiz questions from the explanation

## Topic 6: Router Chains for Choosing the Right Workflow

Router chains decide which prompt or workflow should handle a given input. Introductory LangChain routing examples often use multiple subject-specific prompts and direct each user query to the best-matched chain.

### Learning objectives

- Understand when one prompt is not enough
- Route user questions to specialized chains
- Design simple domain-based workflows
- Build assistants that behave differently based on question type

### Concept

A router makes a decision before the main response is generated. For example, a math question can be routed to a math-focused prompt, while a history question can be routed to a history-focused prompt. This makes responses more relevant and more maintainable than using a single generic prompt for every task.

### Complete example

```python
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOllama(
    url="http://localhost:11434",
    model="gemma3:270m",
    temperature=0.7,
    api_key="ollama"
)

math_prompt = PromptTemplate(
    input_variables=["input"],
    template="You are a math expert. Solve this clearly: {input}"
)

history_prompt = PromptTemplate(
    input_variables=["input"],
    template="You are a history expert. Answer clearly: {input}"
)

coding_prompt = PromptTemplate(
    input_variables=["input"],
    template="You are a programming expert. Explain clearly: {input}"
)

math_chain = LLMChain(llm=llm, prompt=math_prompt)
history_chain = LLMChain(llm=llm, prompt=history_prompt)
coding_chain = LLMChain(llm=llm, prompt=coding_prompt)

def route_question(question):
    q = question.lower()
    if any(word in q for word in ["sum", "multiply", "divide", "equation"]):
        return math_chain.invoke({"input": question})["text"]
    elif any(word in q for word in ["who", "when", "history", "war"]):
        return history_chain.invoke({"input": question})["text"]
    else:
        return coding_chain.invoke({"input": question})["text"]

print(route_question("What is 25 multiplied by 4?"))
```

### What this code teaches

- Different prompts can be specialized for different subjects.
- A lightweight routing function can choose the most suitable chain based on the input.
- Routing is useful when building assistants that must respond differently for support, coding, legal, academic, or business tasks.

### Practice ideas

- Route questions into sales, support, and technical categories
- Build a student assistant with science, math, and history modes
- Add a fallback chain for general-purpose questions

## Recommended learning sequence

The most practical sequence is to start with Ollama basics, then move to prompt templates, structured output, memory, chains, and finally routing. This order moves from single prompt execution toward more modular and production-oriented LangChain applications.[1][5][2]

## Closing note

These six topics form a clean foundation for learning LangChain with local models. Once these concepts are comfortable, the next natural areas are retrieval-augmented generation, document loaders, embeddings, vector stores, agents, and tool-calling workflows in the newer LangChain ecosystem.[2]