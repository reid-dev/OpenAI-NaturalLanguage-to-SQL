# Dataset based on #https://www.kaggle.com/datasets/kyanyoga/sample-sales-data

# Python Imports
import os


# Third Party Imports
import pandas as pd
import openai
import dotenv

# Local Imports
import db_manager
import openai_manager

# Load the API Key form the .env file
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAPI")

if __name__ == "__main__":

    # Load the data into a Pandas DataFrame
    df = pd.read_csv("../data/sales_data_sample.csv")

    # Convert the DataFrame to a database
    db = db_manager.df_to_db(df, "Sales")

    # Create the fixed SQL prompt
    fixed_sql_prompt = openai_manager.create_table_definition_prompt(
        df, "Sales")

    # Get our user input
    user_input = openai_manager.user_query()

    # Create the final prompt
    final_prompt = openai_manager.combine_prompts(fixed_sql_prompt, user_input)

    # Send the prompt to OpenAI
    response = openai_manager.prompt_openai(final_prompt)

    # Grab the SQL query from the response
    sql_query = response["choices"][0]["text"]
    handled_sql_query = db_manager.handle_response(response)

    # Execute the query on the database
    result = db_manager.execute_sql_query(db, handled_sql_query)

    # Print the result
    print(result)
