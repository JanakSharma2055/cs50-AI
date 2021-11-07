import os

for i in range(3):
	for j in range(3):
		my_command =f"python generate.py data/structure{i}.txt data/words{j}.txt output{i}{j}.png"
		os.system(my_command)