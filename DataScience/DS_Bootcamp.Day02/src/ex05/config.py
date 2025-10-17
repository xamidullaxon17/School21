num_of_steps = 3
report_template = """
Report!
We have made {total_observations} observations from tossing a coin: {tails} of them were tails and {heads} of them were heads. 
The probabilities are {tails_percentage:.2f}% and {heads_percentage:.2f}%, respectively. 
Our forecast is that in the next {num_steps} observations we will have: {predicted_tails} tails and {predicted_heads} heads.
"""
