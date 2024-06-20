import streamlit as st
import io
import contextlib
import subprocess
import tempfile

def check_for_input_function(code):
    # Check if the code contains any occurrence of 'input('
    return 'input(' in code

def run_code_subprocess(code, simulated_input=None):
    # Use a temporary file to save the code
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code.encode())
        temp_file.flush()
        temp_file_name = temp_file.name
    
    # Create an empty input stream if no simulated input provided
    input_stream = io.StringIO(simulated_input or "")

    try:
        # Run the code using subprocess and capture the output
        result = subprocess.run(["python", temp_file_name], capture_output=True, text=True, check=True, input=input_stream.getvalue())
        output = result.stdout.strip()
        error_output = result.stderr.strip()
        if error_output:
            output += "\nError Output:\n" + error_output
    except subprocess.CalledProcessError as e:
        output = f"Error: {e}"
    finally:
        # Clean up the temporary file
        temp_file.close()
        if temp_file_name:
            tempfile.unlink(temp_file_name)

    return output

def run_code_exec(code, simulated_input=None):
    # Create a string IO stream to capture the output
    output_stream = io.StringIO()
    
    # Create an empty input stream if no simulated input provided
    input_stream = io.StringIO(simulated_input or "")
    
    try:
        # Redirect stdout and stderr to the string IO stream
        with contextlib.redirect_stdout(output_stream), contextlib.redirect_stderr(output_stream):
            # Inject input function to simulate input if needed
            if check_for_input_function(code):
                exec(f"""
global input
def input(prompt=''):
    return input_stream.readline().strip()
{code}
                """)
            else:
                exec(code)
        # Get the output from the string IO stream
        output = output_stream.getvalue()
    except Exception as e:
        # If an error occurs, return the error message
        output = f"Error: {str(e)}"
    finally:
        # Close the string IO streams
        output_stream.close()
        input_stream.close()
    
    return output

def code_compiler():
    st.title("Python Code Compiler")
    
    st.write("Enter your Python code below:")
    code = st.text_area("Python Code", height=300)
    
    if check_for_input_function(code):
        st.write("Enter simulated input:")
        simulated_input = st.text_area("Simulated Input", height=100)
    else:
        simulated_input = None
    
    if st.button("Run Code"):
        # Choose which execution method based on code content
        if 'subprocess' in code:
            result = run_code_subprocess(code, simulated_input)
        else:
            result = run_code_exec(code, simulated_input)
        
        st.write("Output:")
        st.text(result)

if __name__ == "__main__":
    code_compiler()