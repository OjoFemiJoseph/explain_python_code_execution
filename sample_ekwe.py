import sys
import pandas as pd
import linecache
import inspect
import openai as ai
import time
#shows how to get a free api key https://www.educative.io/answers/how-to-get-api-key-of-gpt-3
ai.api_key = ""


def generate_gpt3_response(user_text, print_output=False):
    """
    Query OpenAI GPT-3 for the specific key and get back a response
    :type user_text: str the user's text to query for
    :type print_output: boolean whether or not to print the raw output JSON
    """
    completions = ai.Completion.create(
        engine='text-davinci-003',  # Determines the quality, speed, and cost.
        temperature=0.1,            # Level of creativity in the response
        prompt=f"explain this python code \n {user_text}",           # What the user typed in
        max_tokens=100,             # Maximum tokens in the prompt AND response
        n=1,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )

    # Displaying the output can be helpful if things go wrong
    if print_output:
        print(completions)

    # Return the first choice's text
    return completions.choices[0].text

#to avoid showing loops multiple times
shown = []

def show_line(x):
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    line = linecache.getline(filename, x)
    return line


def trace_lines(frame, event, arg):
    if event != 'line':
        return
    co = frame.f_code
    func_name = co.co_name
    line_no = frame.f_lineno
    filename = co.co_filename

    code_line = show_line(line_no)
    if code_line:
        
        with open('flow.txt','a') as file:
            file.write(code_line)
        if code_line not in shown:
            print(code_line)
            shown.append(code_line)
            print(generate_gpt3_response(code_line))
            time.sleep(2)

def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':

        return
    line_no = frame.f_lineno
    filename = co.co_filename

    
    if func_name in TRACE_INTO:
    
        return trace_lines
    return
    
def sample_code():
    df = pd.DataFrame(data=[['a','b','c']],columns=['1','2','3'])
    df2 = pd.DataFrame(data=[['a','b','c']],columns=['1','4','5'])

    df.merge(df2,how='left',on='1').to_csv('sample_merge.csv',index=False)

#put your functions here
TRACE_INTO = ['sample_code']

sys.settrace(trace_calls)
#call the index/root function
sample_code()
    
