# Template for starting project quickly

This is a template for starting a project quickly. 

It follows the design idea that data,configure and codes should be seperated.
- When you are coding ,you shouldn't care where's the data and what's the data likes. You should only focus the logic of operations.
- The configure should be cross-platform,which means the code and the command should be unchanged when the project migrates from one computer to another.
- The command which runs the code should be saved,you needn't type the long command in the bash.

## structure

- shell: the command scripts
- code: the code files
- env.yaml: various variables which would pass to the shell scripts. so the shell script is independent with the environment.
- main.sh: main entry execute file.


