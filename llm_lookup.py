
import pandas as pd
import openai
from credentials import openai_api_key
import tqdm


## test zone

# Read the first CSV file
df1 = pd.read_csv('/Users/mkarreth/Downloads/comp.csv')

# Read the second CSV file
df2 = pd.read_csv('/Users/mkarreth/Downloads/prod.csv')

# Set up OpenAI API credentials
openai.api_key = openai_api_key

companies = df1
website_products = df2

join1 = 'Company'
join2 = 'Website'

## actual function


def lookup(df1, df2, join1, join2, matching_context="",openai_model='gpt-3.5-turbo',temperature=0.1, chunk_size=20, return_stats=False):
    cache = {}
    cache_count = 0
    api_calls = 0
    
    df2_values = df2[join2].values.tolist()
    df2_chunks = [df2_values[i:i + chunk_size] for i in range(0, len(df2_values), chunk_size)]
    
    temp_df = df1.copy()
    progress_bar = tqdm.tqdm(total=len(df2_chunks))
    
    for chunk in df2_chunks:
        for index, row in temp_df.iterrows():
            df1_value = row[join1]
            if df1_value in cache:
                generated_text = cache[df1_value]
                cache_count += 1
            else:
                api_calls += 1
                if matching_context == "":
                    prompt = f"Using the best of your knowledge and precise data analysis skills, for the value \"{df1_value}\" of column \"{join1}\", please choose the most appropriate value from the list from column \"{join2}\" below. Return only the exact value as given with no additional text. Important, if you do not see a fitting result, return N/A. Values are: {chunk}"
                else:
                    prompt = f"{matching_context}. Using the best of your knowledge and precise data analysis skills, for the value \"{df1_value}\" of column \"{join1}\", please choose the most appropriate value from the list from column \"{join2}\" below. Return only the exact value as given with no additional text. Important, if you do not see a fitting result, return N/A. Values are: {chunk}"
                response = openai.chat.completions.create(
                    model=openai_model,
                    messages=[
                        {"role": "user",
                        "content": prompt}
                    ],
                    max_tokens=100,
                    temperature=temperature
                )
                generated_text = response.choices[0].message.content
                if generated_text != "N/A":
                    cache[df1_value] = generated_text
            
            temp_df.loc[index, join2] = generated_text
        #temp_df.drop_duplicates(inplace=True)
        progress_bar.update()
    
    progress_bar.close()
    #dfm = pd.merge(df1, temp_df, on=join1, how='left')
    dfm = pd.merge(temp_df, df2, on=join2, how='left')

    stats = {
        "API calls = ": api_calls,
        "Cache calls = ": cache_count,
        "Chunks = ": len(df2_chunks)
    }

    if return_stats:
        return dfm, stats
    else:
        return dfm