# llmLookup

## Excel's vLookup, but powered by LLMs
It's just the good old Excel VLOOKUP, but powered by LLMs. Specifically ever wondered about that approximate match functionality in a VLOOKUP? Well here we go for real.

## Technical details
This code defines a function called `lookup` that performs a lookup operation between two pandas DataFrames (`df1` and `df2`). The function takes several parameters including the column names to join on (`join1` and `join2`), an optional matching context, the OpenAI model to use for text generation, and other optional parameters.

The function starts by initializing a cache dictionary to store previously generated values and some counters to keep track of API calls and cache hits. It then prepares the values from `df2` by extracting the values from the specified join column (`join2`) and splitting them into chunks of a specified size.

Next, the function iterates over each chunk of `df2` values and each row of `df1`. For each row, it checks if the value in the join column (`join1`) is already in the cache. If it is, the corresponding generated text is retrieved from the cache. Otherwise, an API call is made to the OpenAI chat completions API to generate the text.

The prompt for the API call is constructed based on the provided matching context (if any) and the current value from `df1` and the chunk of `df2` values. The generated text is then extracted from the API response and stored in the cache if it is not "N/A".

After all iterations, the function merges the modified `df1` with `df2` based on the join column (`join2`) using the `pd.merge` function.

Finally, the function returns the merged DataFrame (`dfm`) and optionally, some statistics including the number of API calls, cache hits, and the number of chunks processed.

## Function calling

Call the function as follows:

```python
from llm_lookup import lookup

result = lookup(
    table1, # Pandas dataframe, required
    table2, # Pandas dataframe, required
    column_in_table1, # string, required
    column_in_table2, # string, required
    matching_context='', # string, optional
    openai_model='gpt-3.5-turbo', # string, optional
    temperature=0.1, # float, optional
    chunk_size=50, # int, optional
    return_stats=False # bool, optional
)
```

The optional parameters allow you to adjust the lookup for more tailored needs. You can choose the additional context, model, temperature, chunk size and whether or not to return stats on the lookup calls. The model, temperature and chunk size are an interplay that strongly depend on one another and the dataset given. Worth testing on a smaller data set and finetuning to see what works best for needs.
