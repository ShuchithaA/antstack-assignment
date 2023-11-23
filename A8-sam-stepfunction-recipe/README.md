# Step function 

	Implement a step function for recipe flow
		It is a 4 ingredient recipe, with one parallel state for last two ingredients
    each stage adds an ingredient along with time taken and passes it to the next stage
    final stage calculates total time and displays ingredients in order
	

# code implementation
 5 lambda functions are present in Recipe folder
 sam template with state machine ,lambdas, role , and log resource is described
 state_machine_definition.json file has the definition of state machine defined
	