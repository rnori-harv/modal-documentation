# Modal Documentation Answering with Fine-tuning + RAG (w/ Pinecone, Langchain, Llama-2)
## Made by Rakesh Nori, powered by Modal Labs

Here is the (website)[https://rnori-harv--tgi-app.modal.run/] for Modal documentation answering

This README details my process of creating this documentation service, powered by Llama-2, openai, and langchain.

### Overview
In this repo, there are four key steps: data scraping + dataset creation, finetuning, developing RAG on finetuned model, and deploying the model. 


#### Data scraping and Dataset creation

The logic for data scraping and dataset creation can be found in `create_dataset.py` and `modal_takehome_datascraping.ipynb`. The jupyter notebook involves exploratory analysis into the webapge url, and `create_dataset.py` details actual dataset creation. I used the BeautifulSoup library to scrape all relevant documentation urls. For each webpage, I formed a document for each sub-header and the page content associated with it. Then, for each document, I queried GPT-4 to form 5 potential questions that a user could ask. For each of these questions, I paired it with the topic of the page header + sub-header (e.g. "How do I list the contents of a modal volume?" --> "modal volume modal volume ls"). I looped through all documents and repeated this process to form my dataset. Afer creating the dataset, I ran `postprocess_dataset.py` to remove duplicates and null rows.


#### Finetuning

The goal of fine-tuning was to train Llama-2 (13B) to identify the topic of the question being asked that can be queried in the documentation

For this step, I used Modal's fine-tuning [implementation](https://github.com/modal-labs/llama-finetuning) and adapted it to serve our model. I first copied the dataset into the `llama-finetuning/datasets` directory then made a script `llama-finetuning/datasets/docs_dataset.py`, which tokenizes each row of the dataset. 

#### RAG
I used Langchain + OpenAI for RAG. Most of this logic is implemented in `llama-finetuning/inference.py` under `retrieve_docs()` and `load_retrieval()`. I first created a Pinecone vectorstore with the Documents created from scraping the documentation (each document featuring header + sub-header and page content). Then, I propogate the user's question through the fine-tuned Llama model, extract the identified topic, and feed that to the vectorstore. After it returns the content, I run it through OpenAI's GPT-4 to answer the user's question.

#### Deployment
The deployment logic is also in `inference.py` in `app()`. The logic was taken from this (tutorial)[https://modal.com/docs/guide/ex/text_generation_inference#serve-the-model]. The website is deployed (here)[https://rnori-harv--tgi-app.modal.run/].
