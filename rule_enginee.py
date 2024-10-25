import json

# Node class representing AST
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # Reference to another Node (left child)
        self.right = right  # Reference to another Node (right child)
        self.value = value  # Optional value for operand nodes

    def change_rule(self, new_type=None, new_value=None):
        if new_type:
            self.type = new_type
        if new_value:
            self.value = new_value

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value})"

# function to create rule
def create_rule(rule_string):
    # Parsing the rule string into an AST is complex and would typically involve a proper parser.
    # For simplicity, let's assume we are parsing a fixed format.
    def parse_expression(expression):
        expression = expression.strip()
        if expression.startswith('(') and expression.endswith(')'):
            expression = expression[1:-1].strip()

        if 'AND' in expression:
            left, right = expression.split('AND', 1)
            return Node('operator', parse_expression(left), parse_expression(right.strip()), 'AND')
        elif 'OR' in expression:
            left, right = expression.split('OR', 1)
            return Node('operator', parse_expression(left), parse_expression(right.strip()), 'OR')
        else:
            return Node('operand', value=expression.strip())

    return parse_expression(rule_string)

# Function to combine multiple ASTs into one
def combine_rules(rules):
    if not rules:
        return None
    
    root = Node('operator', value='OR')  # Start with OR as the root operator
    for rule in rules:
        rule_ast = create_rule(rule)
        if root.left is None:
            root.left = rule_ast
        else:
            # Chain together the rules
            current = root
            while current.right is not None:
                current = current.right
            current.right = rule_ast
    return root

# Function to evaluate AST against user data
def evaluate_rule(ast, data):
    if ast.type == 'operand':
        left_operand = ast.value.split(' ')
        attribute = left_operand[0]
        operator = left_operand[1]
        value = left_operand[2].strip("'")  # Remove quotes for string values

        if attribute in data:
            if operator == '>':
                return data[attribute] > int(value)
            elif operator == '<':
                return data[attribute] < int(value)
            elif operator == '=':
                return data[attribute] == value
        return False
    elif ast.type == 'operator':
        if ast.value == 'AND':
            return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
        elif ast.value == 'OR':
            return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)


# Sample rules
rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

# Creating rules
ast_rule1 = create_rule(rule1)
ast_rule2 = create_rule(rule2)

# Combining rules
combined_ast = combine_rules([rule1, rule2])

# Sample JSON data for evaluation
data = {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 3
}

# Evaluating rules
result1 = evaluate_rule(ast_rule1, data)
result2 = evaluate_rule(ast_rule2, data)
combined_result = evaluate_rule(combined_ast, data)

# Test cases
print("AST for Rule 1:", ast_rule1)
print("AST for Rule 2:", ast_rule2)
print("Combined AST:", combined_ast)
print("Result for Rule 1:", result1)
print("Result for Rule 2:", result2)
print("Result for Combined Rules:", combined_result)
 