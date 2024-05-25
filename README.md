# llmlookup

## Excel's vlookup, but powered by LLMs
Ever wondered about that approximate match functionality in a vlookup? Well here we go for real. It's just the good old Excel vlookup, but powered by LLMs.

## Calling the lookup function

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

## Technical details (V0.0.2)

The function performs a lookup operation between two pandas dataframes (`df1` and `df2`). The function takes several parameters including the column names to join on (`join1` and `join2`), an optional matching context, the OpenAI model to use for text generation, and other optional parameters.

The function then chunks the `df2` dataframe based on the passed chunk size parameter. This ensures the OpenAI calls meet context window limits but also ensures accuracy of the results. Subsequently, the function iterates over each chunk and each row of `df1`. For each row, it checks if the value in the join column (`join1`) is already in the cache. If it is, the corresponding generated text is retrieved from the cache. Otherwise, an API call is made to the OpenAI chat completions API to generate the text. This ensures both that the results are consistent over the function processing but also saves time/money by calling the API less often.

In terms of the OpenAI API call, it's a simple prompt call. Provides the optional matching context and the current value from `df1` and the chunk of `df2` values. The generated text is then extracted from the API response and stored in the cache if it is not "N/A". The prompt is written to return only the value passed or "N/A."

After all iterations, the function merges the modified `df1` with `df2` based on the join column (`join2`). This essentially returns the expected vlookup result. This result is being returned. Optionally, some statistics including the number of API calls, cache hits, and the number of chunks processed.