import openai


def create_table_definition_prompt(df, table_name):
    """This function creates a definition of the table to pass to OpenAI.

    Args:
        df (DataFrame):Object used to extract the column names
        table_name (String): Name of the table we want to query against

        Returns: String containing the OpenAI prompt
    """

    prompt = '''### sqlite table, with its properties:
    #
    # {}({})
    #
    '''.format(table_name, ",".join(str(x) for x in df.columns))

    return prompt


def user_query():
    """Ask the user to input their question.

    Returns:
        String: Containing the user input. 
    """
    input = input("Tell OpenAi what you want to know about the data: ")
    return input


def combine_prompts(sql_prompt, query):
    """Combine the SQL prompt with the user query.

    Args:
        sql_prompt (String): SQL prompt
        query (String): User query

    Returns:
        String: Prompt to be submitted
    """
    fixed_query = f"### A query to answer: {query}\nSELECT"
    return sql_prompt + fixed_query


def prompt_openai(prompt):
    """Send the prompt to the API

    Args:
        prompt (String): Prompt to send

    Returns:
        String: Response
    """
    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"]
    )
    return response
