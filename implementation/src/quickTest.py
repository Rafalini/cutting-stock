from solutions import AmplSolver


amp = AmplSolver.AmplSolver()
amp.solve('ampl/cut.dat')

def printEntityList(variable_map):
    for entity_name, entity in variable_map:
        print(f"Entity Name: {entity_name}")
        # You can access properties or perform operations on the entity here
        # Example: Print the entity object
        print(f"Entity Object: {entity}")


ampl = amp.solver

printEntityList(ampl.getVariables())
printEntityList(ampl.getConstraints())
# printEntityList(ampl.get_parameter('Wfep'))

