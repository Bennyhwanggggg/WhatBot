# Search Module
Search Module is responsible for searching for result to queries and formulating responses to user queries. Query Module will provide the intent and user message to Response Module so it has some information on how it can find the result user is asking for. Response Module also uses the Utility Module in some situations to perform the task if required.

## Features

### Information Search

Provided the user input and the intent it is classified under, the search module will map the requirement to an relevant function or module that it is suitable for finding the answer to the query.

### Response Formulation

From the result of information search, the search module will also formulate the result to a more human readable form so that user will feel more comfortable talking to WhatBot and not be overwhelmed by too much information.
