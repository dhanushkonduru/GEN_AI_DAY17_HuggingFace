import streamlit as st

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y

def calculator():
    st.title("Simple Calculator")
    
    operations = {
        "Add": add,
        "Subtract": subtract,
        "Multiply": multiply,
        "Divide": divide
    }
    
    operation = st.selectbox("Select operation:", list(operations.keys()))
    num1 = st.number_input("Enter first number:", format="%f")
    num2 = st.number_input("Enter second number:", format="%f")
    
    if st.button("Calculate"):
        result = operations[operation](num1, num2)
        st.write(f"The result is: {result}")

calculator()
